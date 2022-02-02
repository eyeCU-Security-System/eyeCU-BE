from os import path, environ

#Use singleton pattern
#Note: singleton means only one copy of the Base is created for every model class
from app.model.BaseModel import Base
from app.model import Account, Member, Device, Permission

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#Create database if needed based on what defined in declarative base class
baseDirectory = path.abspath(path.dirname(__file__))
db_url = environ.get('DATABASE_URL') or \
    'sqlite:///' + path.join(baseDirectory, 'eyecu.db')
engine = create_engine(db_url)

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()