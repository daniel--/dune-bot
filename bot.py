import discord

from all_games import all_games
from report import report

client = discord.Client()




@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    tokens = message.content.split()
    action = tokens[0]
    tokens = tokens[1:]

    if action == '$report':
        reply = report(message, tokens)

        await message.channel.send(reply)
    elif action == '$games':
        reply = all_games()
        await message.channel.send(reply)


client.run('')
