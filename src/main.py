# bot.py
from collections import Counter
import os


from discord.ext import tasks, commands
import discord
from dotenv import load_dotenv
import asyncio

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

    await guild.channels[0].send('hey whats up i am patbot nice to meet you')

"""
Called when a member joins the server
"""
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'HELLO {member.name} NICE TO MEET YOU')

async def timer_status(ctx, username):
    while True:
        #do something
        await asyncio.sleep(10)

@client.command()
async def timer_status(ctx, username):
    client.loop.create_task(status(ctx,username))

"""
Main processor for messages sent in the discord channel
"""
@client.event
async def on_message(message):
    if message.author == client.user: #don't do self-messages
        return
    
    tokenized_messages = store_message(message)

    await message.channel.send(message.content)

    """
    Standard text functions (!):
    !talk - sends a preset message
    !echo - echoes what the user says after it

    Storage functions (?):
    ?topwords - sends the topwords of the current user
    """
    if message.content[0] == '!':
        command = tokenized_messages[0].lower()
        if command == '!talk':
            await message.channel.send('HELLO IM PATBOT AND THIS IS AN AUTOMESSAGE FOR !TALK')
        elif command == '!echo':
            await message.channel.send(' '.join(tokenized_messages[1:]))
        else:
            raise discord.DiscordException

    elif message.content[0] == '?':
        if tokenized_messages[0].lower() == '?topwords':
            top_words = get_top_words(stored_messages[message.author], 5)
            max_length = max([len(word) for word,count in top_words])
            formatted_words = '\n'.join([f'{word}' + ' ' * (max_length - len(word) + 1) + f'| {count}' for word, count in top_words])
            await message.channel.send(f'**{message.author}\'s top words:**\n```{formatted_words}\n```')
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
    return tokenized_messages

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
