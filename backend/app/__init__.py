'''initializes flask and another connections/dependancies'''
from flask import Flask, g
import sqlite3

app = Flask(__name__)
app.secret_key = "iwanttodie"


def connect_db():
    sql = sqlite3.connect('.\database\eyecu.db')
    sql.row_factory = sqlite3.Row
    
    print('db connected successfully')
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
        
    print("retrieved from db successfully")
    return g.sqlite3_db



#imported after declaring so attributes has chance to be created first
from app import routes
