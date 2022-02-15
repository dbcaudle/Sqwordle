# sqwordle.py
import random
import discord
import re

from discord.ext import commands
from dotenv import dotenv_values
from numpy import average

from SqwordleFunctions import *

temp = dotenv_values(".env") 
TOKEN = temp['DISCORD_TOKEN']

bot=commands.Bot(command_prefix='!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='wordle-gun',  help='Displays team stats for the specified Wordle')
async def wordle_stats(ctx, *, game_number = ''):

    if len(game_number) == 0:
        await ctx.send('Try again with game number. (!wordle-gun 230)')
        return

    total_attempts = 0
    total_players = 0
    low_score = 99
    daily_winners = []

    messages = await ctx.channel.history(limit=400).flatten()
    for msg in messages:
        if msg.author == bot.user: #self
            continue
        
        checkMsg = 'Wordle ' + game_number
        if checkMsg in msg.content:

            #for user_id in total_players:
            #    if msg.author.id == user_id:
            #        break
            MsgHeader = msg.content[:14]
            lhs, rhs = MsgHeader.split('/')
            tries_taken = lhs[-1]
            if tries_taken == 'X':
                tries_taken = 7
            else:
                tries_taken = int(tries_taken)
                if tries_taken < low_score:
                    low_score = tries_taken
                    daily_winners.clear()
                    daily_winners.append(msg.author.id)
                elif tries_taken == low_score:
                    daily_winners.append(msg.author.id)

            total_attempts = total_attempts + tries_taken
            total_players = total_players + 1
    
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

@bot.command(name='wordle-dex',  help='Displays wordledex entry for the player')
async def wordle_stats(ctx, *, user = ''):
    guild_id = ctx.message.channel.guild.id

    # Get user id
    if len(user) == 0:
        player_id = ctx.message.author.id
    elif not user.startswith('<@!'):
        await ctx.send('Invalid user handle!')
        return
    else:
        player_id = ''
        # Iterate over characters in user
        for ch in user:
            if ch.isdigit():
                player_id += ch

    filename = 'wordle_stats_' + str(guild_id) + '.csv'
    sendString = ReadStats(filename, int(player_id))
    await ctx.send(sendString)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if re.search("Wordle \d\d\d \d/\d", message.content): # Will fail when Wordle # == 1000
        guild_id = message.channel.guild.id

        lhs, rhs = message.content.split('/')
        game_number = lhs[7:10]
        tries_taken = lhs[-1]
        if tries_taken == 'X':
            tries_taken = 7
        else:
            tries_taken = int(tries_taken)

        # Record stats
        filename = 'wordle_stats_' + str(guild_id) + '.csv'
        RecordStats(filename, message.author.id, game_number, tries_taken)
        # Add checkmark
        await message.add_reaction('\U00002705')


bot.run(TOKEN)
