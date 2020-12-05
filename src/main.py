# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN_AUTH')
GUILD = os.getenv('SERVER_NAME')

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name==GUILD, client.guilds)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')



client.run(TOKEN)