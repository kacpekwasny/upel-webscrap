# from discord.channel import DMChannel, TextChannel
from ..upel import login, get_data, parse
from time import sleep 
import asyncio


class UpelUser:
    def __init__(self, username, id_) -> None:        
        self.username = username
        self.id = id_
        self.last_login_string = ""
        self.last_login_secs = 0
        self.channels_following = [] # channel objects that follow this user and are waiting for an update
        self.previous_status_is_online = False

    def update_last_login(self, time_string):
        self.last_login_string = time_string
        self.last_login_secs = parse.string2secs(time_string)
        new_status_is_online = self.last_login_secs < 5*60
        if self.previous_status_is_online != new_status_is_online:
            status = "online ✅" if new_status_is_online else "offline ❌"
            for ch in self.channels_following:
                asyncio.run(ch.send(f"{self.username} has gone {status}!"))
        self.previous_status_is_online = new_status_is_online


class FollowUpelUser:
    def __init__(self, upel_login_url, upel_username, upel_password) -> None:
        self.followed_users = [] # UpelUsers that are currently followed
        self.s = login.login(upel_login_url, upel_username, upel_password)
        self.watch_loop_on = True

    def is_command(self, text):
        for cmd_prefix in ["follow", "unfollow"]:
            if cmd_prefix == text[1:len(cmd_prefix)+1]:
                return True
        return False

    def run_command(self, msg):
        # pass command to apropriate function
        # msg - it is an <Object>
        prefix = msg.content.split(" ")[0][1:]
        {
            "follow": self.follow,
            "unfollow": self.unfollow,
        }[prefix](msg)

    def follow(self, msg):
        # identifier has to be the id from URL
        identifier = msg.content.split(" ")[1]
        if not identifier.isdigit():
            asyncio.run(msg.channel.send("Command example: '!follow 7837' where the number is an 'id' that is in URL of user profile."))
            return

        for u in self.followed_users:
            if str(u.id)==identifier:
                if msg.channel in u.channels_following:
                    asyncio.run(msg.channel.send(f"User {u.username} with id: {u.id} is allready being followed."))
                    return
                u.channels_following.append(msg.channel)
                asyncio.run(msg.channel.send(f"Successfully followed user: {u.username}"))
                return
        
        # this user has not been followed before
        try:
            profile_data = get_data.get_user_profile_data(self.s, identifier)
        except:
            asyncio.run(msg.channel.send("User with such id doesn't exist."))
            return
        
        user = UpelUser(profile_data["username"], identifier)
        user.update_last_login(profile_data["since_last_login"])
        user.channels_following.append(msg.channel)
        self.followed_users.append(user)
        asyncio.run(msg.channel.send(f"Successfully followed user: {user.username}"))

    def unfollow(self, msg):
        identifier = msg.content.split(" ")[1]
        for user in self.followed_users:
            if user.username == identifier or identifier == str(user.id):
                user.channels_following.remove(msg.channel)
                asyncio.run(msg.channel.send("Successfully stopped following user."))
        print(f"Number of users that are currently followed: {len(self.followed_users)}")

    def watch_loop(self):
        while self.watch_loop_on:
            print("Users being followed: ", [ f"{u.username} : {u.last_login_string}" for u in self.followed_users])
            for u in self.followed_users:
                time_str = get_data.time_since_last_login(self.s, u.id)
                u.update_last_login(time_str)
                sleep(10)
            sleep(1)
    



