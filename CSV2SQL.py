import csv
import numpy
from SQLite3_tools import AddScore, create_connection

db_file = 'sqwordle.db'
filename = 'wordle_list.csv'

def InitSqwordleTable(conn):
    create_wordle_stats_table = '''CREATE TABLE IF NOT EXISTS wordlestats (
                                id integer PRIMARY KEY,
                                game integer,
                                word text)'''
    conn.execute(create_wordle_stats_table)

def InitWordles(conn):
    create_wordles_table = '''CREATE TABLE IF NOT EXISTS wordles (
                              game integer PRIMARY KEY,
                              word text)'''
    conn.execute(create_wordles_table)

conn = create_connection(db_file)
InitSqwordleTable(conn)
InitWordles(conn)

wordlestats = False
wordles = False

if wordlestats == True:
    with open(filename, mode='r') as wordle_stats:
            wordledex = csv.reader(wordle_stats, delimiter=',')

            for row in wordledex:
                if numpy.size(row) != 0:
                    player = str(row[0])
                    game = int(row[1])
                    score = int(row[2])
                
                AddScore(conn, game, None, player, score)

if wordles == True:
    game = 0
    with open(filename, mode='r') as wordles:
        words = csv.reader(wordles, delimiter=',')
        for row in words:
            word = row[0]
            curse = conn.cursor()
            curse.execute('''INSERT INTO wordles (game, word)
                            VALUES (?, ?)''', (game, word,))
            conn.commit()
            curse.close()
            game += 1


# Updates existing db to add words to wordlestats table
curse = conn.cursor()
for game in range(200, 400):
    try:
        curse.execute('SELECT word FROM wordles WHERE game = ?', (game,))
    except:
        continue
    else:
        data = curse.fetchall()
        word = data[0][0]
        conn.execute('UPDATE wordlestats SET word = ? WHERE game = ?', (word, game,))
        conn.commit()

curse.close()


conn.close()
