'''initializes flask and another connections/dependancies'''
from flask import Flask, g
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restx import Api, Resource, fields
import sqlalchemy
from config import Config
from flask_jwt_extended import JWTManager


app = Flask(__name__)
#app.secret_key = "iwanttodie"
api = Api(app, doc='/docs')
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
jwt = JWTManager(app)


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
from app import routes, models, form
from app.models import User


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User
    }
    
    
#----------model {serializer}-----------------#

'''
this model is the json structure
required for passing data to register users
'''
userReg_model = api.model(
    "Register",
    {
        "username":fields.String(),
        "password":fields.String(),
        "firstName":fields.String(),
        "lastName":fields.String()
    }
)    


'''
this model is the json structure
required for passing data to login users
'''
userLogin_model = api.model(
    "Login",
    {
        "username":fields.String(),
        "password":fields.String()
    }
)


#----------model {serializer} end-----------------#