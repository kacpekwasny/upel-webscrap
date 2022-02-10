import asyncio
import discord
from secrets import DISCORD_TOKEN, USERNAME, PASSWORD
from constatns import LOGIN_URL

from lib.discord.follow_user_online import FollowUpelUser

import threading


fuu = FollowUpelUser(LOGIN_URL, USERNAME, PASSWORD)
client = discord.Client()


@client.event
async def on_ready():
    print("Connected with: ", [guild.name for guild in client.guilds])
    t = threading.Thread(target=fuu.watch_loop)
    t.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"{message.author}: {message.content}")

    if not fuu.is_command(message.content):
        return

    print("running command: ", message.content)
    fuu.run_command(message)


client.run(DISCORD_TOKEN)