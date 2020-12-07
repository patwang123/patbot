# bot.py
from collections import Counter
import os



import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN_AUTH')
GUILD = os.getenv('SERVER_NAME')

client = discord.Client()

stored_messages = {}

"""
On-startup
"""
@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name==GUILD, client.guilds)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

"""
Called when a member joins the server
"""
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'HELLO {member.name} NICE TO MEET YOU')

"""
Main processor for messages sent in the discord channel
"""
@client.event
async def on_message(message):
    if message.author == client.user: #don't do self-messages
        return
    
    tokenized_messages = store_message(message)

    await message.channel.send(message.content)
    if message.content[0] == '!':
        if tokenized_messages[0].lower() == '!talk':
            await message.channel.send('HELLO IM PATBOT AND THIS IS AN AUTOMESSAGE FOR !TALK')
        else:
            raise discord.DiscordException
    elif message.content[0] == '?':
        if tokenized_messages[0].lower() == '?topwords':
            await message.channel.send(
                            get_top_words(
                                stored_messages[message.author],5))
        else:
            raise discord.DiscordException

"""
stores the message into the stored_messages dictionary to be called on with ?topwords
"""
def store_message(message):
    message.content = message.content.strip(' ')
    tokenized_messages = message.content.split(' ')
    if message.author in stored_messages:
        user = stored_messages[message.author]
        for word in tokenized_messages:
            if word in user:
                user[word] += 1
            else:
                user[word] = 1
    else:
        stored_messages[message.author] = dict.fromkeys(tokenized_messages, 1)
    return tokenized_messages\

"""
gives the top words of the dictionary given
"""
def get_top_words(words,size):
    return Counter(words).most_common(size)

"""
Discord Exception handler
"""
@client.event
async def on_error(event, *args, **kwargs):
    with open('error.log','a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)
