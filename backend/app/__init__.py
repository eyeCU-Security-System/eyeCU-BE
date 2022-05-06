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
from flask_cors import CORS
#code snippet for importing database data model 
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from app import database
#from app.services import AccountService
from flask_socketio import SocketIO



webapp = Flask(__name__)
#app.secret_key = "iwanttodie"

#visit http://127.0.0.1:5000/docs to view Flask APIs
#like GET and POST functions
api = Api(webapp, doc='/docs')
webapp.config.from_object(Config)
CORS(webapp)
#socketio = SocketIO(webapp,cors_allowed_origins="*",  logger=True, engineio_logger=True)
socketio = SocketIO(webapp,cors_allowed_origins="*", async_mode="threading")


db = SQLAlchemy(webapp)
migrate = Migrate(webapp, db)
manager = Manager(webapp)
manager.add_command('db', MigrateCommand)
jwt = JWTManager(webapp)

# def connect_db():
#     sql = sqlite3.connect('.\database\eyecu.db')
#     #sql.row_factory = sqlite3.Row
    
#     print('db connected successfully')
#     return sql

# def get_db():
#     #if no connection to db has been made
#     if not hasattr(g, 'sqlite3'):
#         g.sqlite3_db = connect_db()
        
#     print("db queried successfully")
#     return g.sqlite3_db


# #close db connection when a request is done
# @webapp.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite3'):
#         g.sqlite3.close()


#imported after declaring so attributes has chance to be created first
from app import routes
from app.model.Account import Account
from app.model.Faces import Faces


@webapp.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Account": Account,
        "Faces": Faces
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
        "email":fields.String(),
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


userFace_model = api.model(
    "Face",
    {
        "picture_file": fields.String(),
    }
)


#----------model {serializer} end-----------------#
