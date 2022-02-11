from datetime import date, datetime, timedelta
from inspect import trace
import traceback

from json import dumps

from ..upel import login, get_data, parse

def pretty(d, indent=0):
    s = ""
    for key, value in d.items():
        s += "\n" + ('      ' * indent + str(key))
        if isinstance(value, dict):
            s += pretty(value, indent+1)
        else:
            if value != "-":
                s += (': \t' + str(value))
    return s

class UserConnection2Upel:
    def __init__(self, upel_login_url, upel_username, upel_password) -> None:
        self.upel_login_url = upel_login_url
        self.upel_username = upel_username
        self.upel_password = upel_password
        self.last_access = datetime(year=2000, month=1, day=1)
        self.login_upel()

    def login_upel(self):
        self.s = login.login(self.upel_login_url, self.upel_username, self.upel_password)
        self.last_access = datetime.now()

    def get_grades(self, course_id):
        if datetime.now() - self.last_access > timedelta(0, 60*10):
            self.login_upel()
        else:
            self.last_access = datetime.now()
        return parse.parse_grades(get_data.course_grades(self.s, course_id))


class UsersCredentialManager:
    def __init__(self, upel_login_url) -> None:
        self.user_connections = {} # map discord_user_id -> UserConnection2Upel
        self.upel_login_url = upel_login_url

    def is_command(self, text):
        if text[0] != "-":
            return False
        for cmd_prefix in ["login", "logout", "getgrades"]:
            if cmd_prefix == text[1:len(cmd_prefix)+1]:
                return True
        return False

    async def run_command(self, msg):
        # pass command to apropriate function
        # msg - it is an <Object>
        prefix = msg.content.split(" ")[0][1:]
        await {
            "login": self.add_account,
            "logout": self.remove_account,
            "getgrades": self.get_grades,
        }[prefix](msg)

    async def add_account(self, msg):
        split = msg.content[len("-login"):].strip().split(" ")
        username = split[0]
        password = " ".join(split[1:]) # in case there was a space (" ") in password
        try:
            u = UserConnection2Upel(self.upel_login_url, username, password)
            self.user_connections[msg.author.id] = u
            await msg.channel.send("Successfully logged in to your UPEL account.")
        except ValueError:
            await msg.channel.send("Could not log in, make sure credentials are correct.\n`-help` for more info!")

    async def remove_account(self, msg):
        if msg.author.id in self.user_connections:
            del self.user_connections[msg.author.id]
            await msg.channel.send("Credentials successfully deleted without a trace.")
            return
        await msg.channel.send("No UPEL credentials associated with your discord user were found.\n`-help` for more info!")

    async def get_grades(self, msg):
        try:
            course_id = msg.content.split(" ")[1]
            alias = {"anal":1464, "alg":1424, "wdsi":296, "pt":1477, "ask":1099}
            course_id = alias.get(course_id.lower(), course_id)
            if not str(course_id).isdigit():
                raise IndexError
        except IndexError:
            await msg.channel.send("Missing course id. Example: `-getgrades 1324` or use one of shortcuts: anal, alg, wdsi, pt, ask insted of course_id.\nExample: `-getgrades anal`\n`-help` for more info!")
            return
        try:
            grades = self.user_connections[msg.author.id].get_grades(course_id)
            lines = pretty(grades).split("\n")
            text = ""
            while len(lines)>0:
                line = lines.pop(0)
                if len(text + line) < 2000:
                    text += line + "\n"
                    continue
                await msg.channel.send(text)
                text = line + "\n"
            await msg.channel.send(text)

        except KeyError:
            await msg.channel.send("Please _DIRECT MESSAGE ME_: `-login <upel_login> <upel_password>` beffore attemting this command again.\n`-help` for more info!")
        except Exception as e:
            print(f"Exception in user.get_grades({course_id}) \n", e)
            print(traceback.format_exc())
            await msg.channel.send("Error had occured, you have probably a wrong course id.\n`-help` for more info!")

            


