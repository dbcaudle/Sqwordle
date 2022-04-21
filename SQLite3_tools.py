import sqlite3
from sqlite3 import Error

# Connect to Sqwordle Database
#class SQliteIF:
def create_connection(db_file):
    """ create a database connection to the Sqwordle database
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        WriteLog(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        WriteLog(e)

def add_row(conn, row_sql):
    """ create a row from the row_sql statement
    :param conn: Connection object
    :param row_sql: a INSERT INTO statement
    :return:
    """
    try:
        conn.execute(row_sql)
    except Error as e:
        WriteLog(e)

def CheckGame(conn, game, word):
    curse = conn.cursor()
    # Does the game already exist in the table?
    curse.execute('SELECT game FROM wordlestats WHERE game = ?', (game,))
    data = curse.fetchall()
    curse.close()
    if not data:
        WriteLog('Game not found. Adding new row')
        conn.execute('INSERT INTO wordlestats (game, word) VALUES (?, ?)', (game, word,))
        conn.commit()
    else:
        WriteLog('Game already exists')

def AddPlayer(conn, player):

    add_table_cmd = 'ALTER TABLE wordlestats ADD COLUMN u' + player + ' integer'
    conn.execute(add_table_cmd)

    # Checks to see if the new column was actually created
    # see if this actually works
    try:
        curse = conn.cursor()
        curse.execute('Select u' + player + ' from wordlestats')
        curse.close()
    except:
        return False
    else:
        WriteLog('New column added for ' + player)
        return True
        
def AddScore(conn, game, word, player, score):
    # Checks for existing game and add if necessary
    CheckGame(conn, game, word)
        
    # Get player column (Does it currently exist?)
    curse = conn.cursor()
    data = curse.execute('Select * from wordlestats')
    pexist = False
    # Search column names for player
    for col in data.description:
        if col[0] == 'u'+ player:
            pexist = True
            sql_cmd = 'UPDATE wordlestats SET u' + player + '=' + str(score) + ' WHERE game = ' + str(game)
            curse.execute(sql_cmd)
            #curse.execute('''UPDATE wordlestats SET ? = ? WHERE game = ?''', ('player1', 6, 238,))
            #curse.execute('''UPDATE wordlestats SET player1 = 6 WHERE game = 238''')
            conn.commit()
            curse.close()
    if pexist == False:
        bPlayerAdded = AddPlayer(conn, player)
        if bPlayerAdded == True:
            AddScore(conn, game, word, player, score)
        else:
            WriteLog('Could not add score. Player does not exist.')
    else:
        WriteLog('Score updated')
    
def WriteLog(s):
    with open('OutputLog.txt', 'a') as ofile:
        ofile.write(s + '\n')
