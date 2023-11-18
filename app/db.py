import sqlite3
import csv
#import geo

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
    neighbors_header = ("(Username TEXT,Password TEXT)")
    create_table("userInfo",neighbors_header)
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.close()
    db.commit()
    
   