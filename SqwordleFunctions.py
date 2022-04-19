# Additional functions for Sqeordle
import csv
import random
import numpy
from sqlite3 import Error
from SQLite3_tools import *

def InitSqwordleTable(conn):
    create_wordle_stats_table = '''CREATE TABLE IF NOT EXISTS wordlestats (
                                id integer PRIMARY KEY,
                                game integer,
                                word text)'''
    conn.execute(create_wordle_stats_table)

def RecordStats(filename, db_file, player, game_number, score):
    # Record stats using SQL
    try:
        conn = create_connection(db_file)
        InitSqwordleTable(conn)
        AddScore(conn, int(game_number), None, str(player), score)
        conn.close()
    except Error as e:
        WriteError(e)

######################################################################
    with open(filename, mode='a+') as wordle_stats:
        wordledex = csv.writer(wordle_stats, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #gamechecker = csv.reader(wordle_stats, delimiter=',')
        #for row in gamechecker: # Doesn't seem to be working
        #    # Checks to see if Sqwordle has already recorded that game for the player
        #    if (row == []) or (int(row[0]) != player):
        #        continue
        #    elif (row[1] == game_number):
        #        # It's assumed that the first check will confirm the player id.
        #        return
        #    else:
        #        continue
        # If it makes it this far, we will add the game to the stats.
        wordledex.writerow([player, game_number, score])
#####################################################################

def ReadStats(filename, db_file, player):

    #########################################################
    tot_score = 0
    tot_games = 0
    worst_game = 0
    best_game = 9
    lost_games = 0

    with open(filename, mode='r') as wordle_stats:
        wordledex = csv.reader(wordle_stats, delimiter=',')

        for row in wordledex:
            if (row == []) or (int(row[0]) != player):
                continue
            else:
                if int(row[2]) == 7:
                    lost_games = lost_games + 1
                else:
                    if int(row[2]) > worst_game:
                        worst_game = int(row[2])
                    if int(row[2]) < best_game:
                        best_game = int(row[2])
                
                tot_score = tot_score + int(row[2])
                tot_games = tot_games + 1
    
    try:
        conn = create_connection(db_file)
        curse = conn.cursor()
        query = 'SELECT u' + str(player) + ' FROM wordlestats'
        scores = [score[0] for score in curse.execute(query)]
        curse.close()
    except Error as e:
        WriteError(e)
    

    if tot_games == 0:
        #####################################################################
        sendString = 'No stats for <@' + str(player) + '>'
    else:
        #################################################################
        avg = format(tot_score / tot_games, '.2f')
        #################################################################
        scores = list(filter(None, scores))
        tot_games = numpy.size(scores)

        avg_db = format(numpy.nanmean(scores), '.2f')
        if max(scores) == 7:
            worst_game_db = 'DNF'
        else:
            worst_game_db = max(scores)
        best_game_db =  min(scores)
        # Find number of failed games

        dex_entry = Wordledex_Entry(player)

        sendString = ('Wordle Stats for ' + '<@' + str(player) + '>:' + '\n' +
                      'Games Played: ' + str(tot_games) + '\n' +
                      'Average Score: ' + str(avg) + '\n' +
                      'Best Game: ' + str(best_game) + '\n' +
                      'Worst Game: ' + str(worst_game) + '\n\n' +
                      dex_entry)
    
    return sendString

def GameStats(db_file, game, guild_members):

    total_players = 0
    total_attempts = 0
    low_score = 99
    daily_winners = []

    try:
        conn = create_connection(db_file)
        cols = conn.execute('SELECT * FROM wordlestats')
        players = [description[0] for description in cols.description]
        curse = conn.cursor()
        curse.execute('SELECT * FROM wordlestats WHERE game=?', (game,))
        row = curse.fetchall()
    except Error as e:
        WriteError(e)
        return 0,0,0,0

    if len(row) == 0:
        return 0, 0, 0, 0

    for iScore in range(len(row[0])):
        if iScore >= 3:
            # Check if player is in guild
            player = players[iScore][1:len(players[iScore])]
            member_count = guild_members.count(int(player))
            if member_count == 0:
                continue

            score = row[0][iScore]
            if score == None:
                continue
            
            total_players = total_players + 1
            total_attempts = total_attempts + score

            if score < low_score:
                low_score = score
                daily_winners.clear()
                daily_winners.append(player)
            elif score == low_score:
                daily_winners.append(player)
    
    return total_players, total_attempts, low_score, daily_winners

def WriteError(s):
    with open('ErrorLog.txt', 'a') as efile:
        efile.write(str(s) + '\n###########################\n')

def Wordledex_Entry(playerID):
    player = '<@' + str(playerID) + '>'

    # Add to SQL table
    entry = random.randint(1,20)
    if entry == 1:
        dex_entry = player + '\'s body temperature is approximately 18,000 degrees F.'
    elif entry == 2:
        dex_entry = player + ' feeds on soil. After it has eaten a large mountain, it will fall asleep so it can grow.'
    elif entry == 3:
        dex_entry = player + '\'s droppings are hot, so people used to put them in their clothes to keep themselves warm.'
    elif entry == 4:
        dex_entry = 'It happened one morning - A boy with extrasensory powers awoke in bed transformed into ' + player + '.'
    elif entry == 5:
        dex_entry = 'The spirits ' + player + ' absorbs fuel its baleful fire. It hangs around hospitals waiting for people to pass on.'
    elif entry == 6:
        dex_entry = player + ' has the habit of hugging its companions. Many friends have left this world after their spines were squashed by its hug.'
    elif entry == 7:
        dex_entry = player + '\'s brain is very small. It is so dense, while on a run it forgets why it started running in the first place. It apparently remembers sometimes if it demolishes something.'
    elif entry == 8:
        dex_entry = player + ' is virtually worthless in terms of both power and speed. It is the most weak and pathetic player in the world.'
    elif entry == 9:
        dex_entry = 'If a child it has made friends with is bullied, ' + player + ' will find the bully\'s house and burn it to the ground.'
    elif entry == 10:
        dex_entry = player + ' is born asleep, and dies asleep. All its movements are apparently no more than the result of it tossing and turning in its dreams.'
    elif entry == 11:
        dex_entry = player + ' has a dream of one day soaring in the sky. In doomed efforts to fly, this player hurls itself off cliffs. As a result of its dives, its head has grown tough and as hard as tempered steel.'
    elif entry == 12:
        dex_entry = player + ' spins string not only from its rear but also from its mouth. It is hard to tell which end is which.'
    elif entry == 13:
        dex_entry = player + ' threatens any attackers by fiercely jingling their keys at them.'
    elif entry == 14:
        dex_entry = 'While guarding its weak points with its pincers, ' + player + ' looks for an opening and unleashes punches. When it loses, it foams at the mouth and faints.'
    elif entry == 15:
        dex_entry = player + '\'s tackle is forceful enough to flip a 50-ton tank. It shields its allies from danger with its own body.'
    elif entry == 16:
        dex_entry = player + ' freezes hikers who have come to climb snowy mountains and carries them back to its home. It only goes after men it thinks are handsome.'
    elif entry == 17:
        dex_entry = 'To protect its friends, ' + player + ' will expend all its psychic power to create a small black hole.'
    elif entry == 18:
        dex_entry = player + ' can clear a 30-story building in a single leap.'
    elif entry == 19:
        dex_entry = 'For some reason, ' + player + ' likes to land on people\'s heads softly and act like it\'s a hat.'
    elif entry == 20:
        dex_entry = 'If ' + player + ' bonds with a person, it will gently envelop the friend with its soft wings, then hum.'

    return dex_entry
