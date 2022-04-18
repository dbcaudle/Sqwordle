import csv
import numpy
from SQLite3_tools import AddScore, create_connection

db_file = 'sqwordle.db'
filename = ''

def InitSqwordleTable(conn):
    create_wordle_stats_table = '''CREATE TABLE IF NOT EXISTS wordlestats (
                                id integer PRIMARY KEY,
                                game integer,
                                word text)'''
    conn.execute(create_wordle_stats_table)

conn = create_connection(db_file)
InitSqwordleTable(conn)

with open(filename, mode='r') as wordle_stats:
        wordledex = csv.reader(wordle_stats, delimiter=',')

        for row in wordledex:
            if numpy.size(row) != 0:
                player = str(row[0])
                game = int(row[1])
                score = int(row[2])
            
            AddScore(conn, game, None, player, score)

conn.close()