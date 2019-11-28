import discord
from googlesearch import search

import app_settings
from db_utils import create_table_if_not_exists, insert_into_search_history, filter_from_search_history

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
    if len(message_words) > 1 and message_words[0] == '!google':
        # search on google
        query = message_words[1:]
        query = ' '.join(query)

        for j in search(query, stop=5, pause=1):
            response = j
            await message.channel.send(response)
        # persist the search in DB
        insert_into_search_history(query)

    if message_words[0] == '!recent':
        # read from file
        match_keyword = message_words[1]

        top_two_results = filter_from_search_history(match_keyword)
        print(top_two_results)
        for result in top_two_results:
            await message.channel.send(result[0])

create_table_if_not_exists()
client.run(app_settings.DISCORD_TOKEN)
