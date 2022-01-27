'''initializes flask and another connections/dependancies'''
from flask import Flask, g
import sqlite3

app = Flask(__name__)
app.secret_key = "iwanttodie"


def connect_db():
    sql = sqlite3.connect('.\database\eyecu.db')
    #sql.row_factory = sqlite3.Row
    
    print('db connected successfully')
    return sql

def get_db():
    #if no connection to db has been made
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
        
    print("db queried successfully")
    return g.sqlite3_db


#close db connection when a request is done
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3'):
        g.sqlite3.close()


#imported after declaring so attributes has chance to be created first
from app import routes
