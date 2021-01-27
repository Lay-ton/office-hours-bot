import os

import discord
import redditstockscan as rscan
import helpers
import keys
import asyncio

TOKEN = keys.DISCORDTOKEN

client = discord.Client()


commands = [
    '!help: Lists all commands I can perform.\n',
    '!scanstocks: Scans for tickers on a specified subreddit. Parameters: \{subreddit\}\n'
]

answer = asyncio.Future()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = (message.content).split(' ')
    if command[0] == '!scanstocks':
        postTypes = ["hot", "top", "controversial", "new", "rising"]
        times = ["hour", "day", "week", "month", "year", "all"]

        subreddit = "wallstreetbets"
        postType = "hot"
        time = "day"
        comments = False
        desc = False
        size = 100

        if len(command) == 1:
            subreddit = "wallstreetbets"
            comments = True
            desc = True
        elif len(command) == 2:
            subreddit = command[1]
            comments = True
            desc = True
        else:
            for item in command[2:]:
                if item in postTypes:
                    postType = item
                elif item in times:
                    time = item
                elif item == 'comments':
                    comments = True
                elif item == 'desc':
                    desc = True
                elif helpers.RepInt(item):
                    size = int(item)

        # answer.set_result(rscan.runRedditScanner(
        #     subreddit, postType, time, comments, desc, size))

        # while not answer.result():
        #     print("Sleeping")
        #     await asyncio.sleep(10)

        answer = rscan.runRedditScanner(
            subreddit, postType, time, comments, desc, size)
        for response in answer:
            await message.channel.send(response)
    elif command[0] == '!help':

        response = ""
        for item in commands:
            response += item
        await message.channel.send(response)

client.run(TOKEN)
