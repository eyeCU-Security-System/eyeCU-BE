from os import path, environ

#Use singleton pattern
#Note: singleton means only one copy of the Base is created for every model class
from app.model.BaseModel import Base

#IMPORT ALL TABLES HERE FOR NOW#
from app.model.Account import Account
from app.model.Faces import Faces

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#Create database if needed based on what defined in declarative base class
baseDirectory = path.abspath(path.dirname(__file__))
db_url = environ.get('DATABASE_URL') or \
    'sqlite:///' + path.join(baseDirectory, 'eyecu.db')
engine = create_engine(db_url, connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()