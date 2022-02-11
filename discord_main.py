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

    if fuu.is_command(message.content):
        if f.request_incoming_is_spam(message.author.id):
            await message.channel.send("Please wait, too many messages in too short time.")
            print(f"{message.author} is spamming")
            return
    
        print("running command: ", message.content)
        await fuu.run_command(message)

    if ucm.is_command(message.content):
        # not checking if this is spam, because everyone will be spamming from their own accounts
        await ucm.run_command(message)        

client.run(DISCORD_TOKEN)