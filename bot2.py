import os

import discord
from googlesearch import search

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'hi':
        response = 'hey'
        await message.channel.send(response)

    message_text = message.content
    message_words = message_text.split()
    print(message_words)
    # search_engine, search_query = message_text.split()
    if len(message_words) > 1 and message_words[0] == '!google':
        # search on google
        query = message_words[1:]
        query = ' '.join(query)

        for j in search(query, stop=5, pause=1):
            response = j
            await message.channel.send(response)
        if 'game' in query:
            # persist the search on file system
            with open('search_history.txt', 'a') as f:
                f.write(query+'\n')

    if message_words[0] == '!recent':
        # read from file
        match_keyword = message_words[1]
        with open('search_history.txt', 'r') as f:
            search_history = f.readlines()
            number_of_words_found = 0
            for search_item in reversed(search_history):
                if number_of_words_found >= 2:
                    break
                if match_keyword in search_item:
                    await message.channel.send(search_item)
                    number_of_words_found += 1
open('search_history.txt', 'a').close()
client.run(token)
