# Additional functions for Sqeordle
import random
import numpy
from sqlite3 import Error
from SQLite3_tools import AddScore, create_connection

def InitSqwordleTable(conn):
    create_wordle_stats_table = '''CREATE TABLE IF NOT EXISTS wordlestats (
                                id integer PRIMARY KEY,
                                game integer,
                                word text)'''
    conn.execute(create_wordle_stats_table)

def RecordStats(db_file, player, game, score):
    # Record stats using SQL
    conn = create_connection(db_file)
    InitSqwordleTable(conn)
    AddScore(conn, game, None, player, score)
    conn.close()

def ReadStats(db_file, player):

    # tot_games; tot_score; worst_game; best_game
    conn = create_connection(db_file)
    curse = conn.cursor()
    query = 'SELECT u' + player + ' FROM wordlestats'
    try:
        scores = [score[0] for score in curse.execute(query)]
    except Error as e:
        print(e) # Should output this to error log
        sendString = 'No stats for <@' + str(player) + '>'
    else:
        
        tot_games = numpy.size(scores)
        avg = format(numpy.mean(scores), '.2f')
        if max(scores) == 7:
            worst_game = 'DNF'
        else:
            worst_game = max(scores)
        best_game =  min(scores)
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

    conn = create_connection(db_file)
    curse = conn.cursor()
    
    cols = conn.execute('SELECT * FROM wordlestats')
    players = [description[0] for description in cols.description]

    curse.execute('SELECT * FROM wordlestats WHERE game=?', (game,))
    row = curse.fetchall()
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
            
            total_players = total_players + 1
            total_attempts = total_attempts + score

            if score < low_score:
                low_score = score
                daily_winners.clear()
                daily_winners.append(player)
            elif score == low_score:
                daily_winners.append(player)
    
    return total_players, total_attempts, low_score, daily_winners

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
