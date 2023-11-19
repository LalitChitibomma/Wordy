import sqlite3
import csv

DB_FILE = "database.db"

def query(sql, extra = None):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    if extra is None:
        res = c.execute(sql)
    else:
        res = c.execute(sql, extra)
    db.commit()
    db.close()
    return res

def get_table_contents(tableName):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT * from {tableName}")
    out = res.fetchall()
    db.commit()
    db.close()
    return out

def create_table(name, header):
    query(f"CREATE TABLE IF NOT EXISTS {name} {header}")

def add_account(username, password):
    if not(check_username(username)):
        query("INSERT INTO userInfo VALUES (?, ?)", (username, password))
    else:
        return -1

def add_game_content(gameid, term, deftn):
    query("INSERT INTO game_info VALUES (?, ?, ?)", (gameid, term, deftn))
   
def get_gameid_content(id):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    temp = c.execute(f"SELECT * from game_info WHERE (Game_id = {id});")
    info = temp.fetchall()
    db.close()
    return info


def check_username(username):
    accounts = get_table_contents("userInfo")
    for account in accounts:
        if account[0] == username:
            return True
    return False

#return true if username and password are in db, false if one isn't
def verify_account(username, password):
    accounts = get_table_contents("userInfo")
    for account in accounts:
        if account[0] == username and account[1] == password:
            return True
    return False

def setup():
    user_header = ("(Username TEXT,Password TEXT)")
    create_table("userInfo",user_header)
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.close()
    db.commit()

    game_table = ("(Game_id INTEGER, Words TEXT, Def TEXT)")
    create_table("game_info",game_table)
    db_2 = sqlite3.connect(DB_FILE, check_same_thread=False)
    c_2 = db_2.cursor()
    c_2.close()
    db_2.commit()
    
   