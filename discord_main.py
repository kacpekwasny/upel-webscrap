import asyncio
import discord

from datetime import timedelta


from secrets import DISCORD_TOKEN, USERNAME, PASSWORD
from constatns import LOGIN_URL

from lib.discord.follow_user_online import FollowUpelUser
from lib.discord.firewall import Firewall
from lib.discord.user_upel_connection import UsersCredentialManager



fuu = FollowUpelUser(LOGIN_URL, USERNAME, PASSWORD)
ucm = UsersCredentialManager(LOGIN_URL)
f = Firewall(10, timedelta(0,60))

client = discord.Client()




@client.event
async def on_ready():
    print("Connected with: ", [guild.name for guild in client.guilds])
    asyncio.create_task(fuu.watch_loop())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"{message.author}: {message.content}")

    if "-help" == message.content[:5]:
        await message.channel.send(
"""
You can follow UPEL users to be notified on this chat/channel when they become online / offline.
Do this by entering a command: `-follow wxyz` where `wxyz` is the `...profile.php?id=wxyz` in url in the UPEL profile page.
To unfollow execute command: `-unfollow wxyz`
To find out about followed users and ther last time online: `-followed`.

You also can get your grades from UPEL, your username and password will not be saved, only kept in RAM, you can allways delete them by executing: `-logout`.
But first to log in execute command: `-login <UPEL_LOGIN> <UPEL_PASSWORD>`
_WARNING!!! LOG IN BY SENDING A PRIVATE MESSAGE TO THE BOT!!! DO NOT EXPOSE YOUR CREDENTIALS!_

If you see a message indicating success then you can proceed with the next step:
`-getgrades <anal/alg/wdsi/pt/ask>` example: `-getgrades pt`.
or `-getgrades wxyz` example: `-getgrades 1477` beacuse 1477 is the course id of Podstawy Telekomunikacji.
The id can be found in the URL the same way as id of UPEL profile id.
"""
        )

    if fuu.is_command(message.content):
        if f.request_incoming_is_spam(message.author.id):
            await message.channel.send("Please wait, too many messages in too short time.")
            print(f"{message.author} is spamming")
            return
    
        if not "-login" in message.content:
            print("running command: ", message.content)
        else:
            print("running command:  -login **** ****")
        await fuu.run_command(message)
        return

    if ucm.is_command(message.content):
        # not checking if this is spam, because everyone will be spamming from their own accounts
        await ucm.run_command(message)
        return

client.run(DISCORD_TOKEN)