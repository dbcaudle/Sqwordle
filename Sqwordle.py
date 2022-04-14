# sqwordle.py
import random
import re

import asyncio
import discord
from discord.ext import commands
from dotenv import dotenv_values

from SqwordleFunctions import *
from SQLite3_tools import *

temp = dotenv_values(".env") 
TOKEN = temp['DISCORD_TOKEN']

db_file = 'Data\\sqwordle.db'

intents = discord.Intents.default()
intents.members=True
bot=commands.Bot(command_prefix='!', intents=intents)

##### 99 Command #####
@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
        'Love, it sustains you. It\'s like oatmeal.',
        'Good to see you. But if you\'re here, who\'s guarding Hades?'
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

##### Bubble Command #####
@bot.command(name='bubble',  help='Displays server stats for the specified Wordle')
async def wordle_stats(ctx, *, game_number = ''):

    if len(game_number) == 0:
        await ctx.send('Try again with game number. (!bubble 230)')
        return


    # Get row from sql
    total_players, total_attempts, low_score, daily_winners = GameStats(db_file, int(game_number))
    if total_players == 0:
        await ctx.send('No players for Wordle ' + str(game_number))
    else:
        
        winner_list = ''
        for winners in daily_winners:
            if len(winner_list) == 0:
                winner_list = '<@' + str(winners) + '>'
            else:
                winner_list = winner_list + ', <@' + str(winners) + '>'

        average_attempts = total_attempts / total_players
        average_attempts = format(average_attempts, '.2f')

        sendString = ('Wordle Game ' + str(game_number) + '\n' +
                      'Total Players: ' + str(total_players) + '\n' +
                      'Total Guesses: ' + str(total_attempts) + '\n' +
                      'Average Score: ' + str(average_attempts) + '\n\n' +
                      'Congratulations to ' + winner_list + ' with a score of ' + 
                      str(low_score))
        
        await ctx.send(sendString)

##### Dex Command #####
@bot.command(name='dex',  help='Displays wordledex entry for the player')
async def wordle_stats(ctx, *, user = ''):
    guild_id = ctx.message.channel.guild.id

    # Get user id
    if len(user) == 0:
        player_id = str(ctx.message.author.id)
    elif not user.startswith('<@'):
        await ctx.send('Invalid user handle!')
        return
    else:
        player_id = ''
        # Iterate over characters in user
        for ch in user:
            if ch.isdigit():
                player_id += ch

    sendString = ReadStats(db_file, player_id)
    await ctx.send(sendString)

##### Listen for Wordle Score Event #####
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if re.search("Wordle \d\d\d \d/\d", message.content) or re.search("Wordle \d\d\d X/\d", message.content): # Will fail when Wordle # == 1000
        guild_id = message.channel.guild.id

        lhs, rhs = message.content.split('/')
        game_number = lhs[7:10]
        tries_taken = lhs[-1]
        if tries_taken == 'X':
            tries_taken = 7
        else:
            tries_taken = int(tries_taken)

        # Record stats using SQL
        RecordStats(db_file, str(message.author.id), int(game_number), tries_taken)
        
        # Add checkmark
        await message.add_reaction('\U00002705')
    
    # on_message by default disables bot commands. This forces bot to look for commands
    await bot.process_commands(message)

##### Timed Questions #####
async def my_background_task(channel_id):
    
    greeting = [ 
        'Hey',
        'So',
        'I was curious'
        ]
    prompt = [
        'what music are you listening to this week?',
        'how\'s the job treating you?',
        'what\'s one good thing that happened to you this week?',
        'watch any good shows recently?',
        'if I gave you $1m to spend frivolously, what would you buy?',
        'where do you want to go on your next vacation?',
    ]

    await bot.wait_until_ready()

    channel = bot.get_channel(id=channel_id) # replace with channel_id
    while not bot.is_closed():
        
        user_id = bot.user
        while user_id == bot.user:
            user_id = random.choice(channel.guild.members)

        user = ' <@' + str(user_id.id) + '>,'
        
        response = random.choice(greeting) + user + random.choice(prompt)
        await channel.send(response)

        # Random question every 1-5 days.
        days = random.randint(1,5) * random.randint(79200, 93600) #seconds in a day

        await asyncio.sleep(days)

##### Start Questions Command #####
@bot.command(name='IChooseYou', help='Initiates random questions every few days.')
async def startchat(ctx):
    channel_id = ctx.channel.id
    bot.loop.create_task(my_background_task(channel_id))


bot.run(TOKEN)