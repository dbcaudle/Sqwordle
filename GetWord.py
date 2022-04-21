# Gets Wordle word for specified game

# Pull list from wordle_list.csv

import sqlite3

from pyparsing import Word

db_file = 'sqwordle.db'

def GetWord(game):
    conn = sqlite3.connect(db_file)
    curse = conn.cursor()

    curse.execute('''SELECT word from wordles
                     WHERE game = ?''', (game,))
    word = curse.fetchone()
    curse.close()
    conn.close()

    return word[0]

selected_word = GetWord(0)
print(selected_word)