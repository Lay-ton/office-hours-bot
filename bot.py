import os

import discord

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


commands = {
    '!help': 'Lists all commands I can perform.',
    '!scanstocks': 'Scans for tickers on a specified subreddit. Parameters: \{subreddit\} '
}


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
        comments = "n"
        desc = "n"

        if len(command) == 1:
            subreddit = "wallstreetbets"
            postType = "hot"
            time = "day"
            comments = "y"
            desc = "y"
        elif len(command) == 2:
            subreddit = command[1]
            postType = "hot"
            time = "day"
            comments = "y"
            desc = "y"
        else:
            for item in command[2:]:
                if item in postTypes:
                    postType = item
                elif item in times:
                    time = item
                elif item == 'comments':
                    comments = "y"
                elif item == 'desc':
                    desc = "y"

        await message.channel.send(response)
    elif command[0] == '!help':
        await message.channel.send(response)

client.run(TOKEN)
