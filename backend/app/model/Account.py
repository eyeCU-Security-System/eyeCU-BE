from sqlalchemy import *
from app.model.BaseModel import Base

'''
user info table
CREATE TABLE Accounts(
    id INTEGER NOT NULL AUTOINCREMENT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);
'''
class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key = True)
    username = Column(String(64), index = True, nullable = False, unique = True)
    password = Column(String(64), index = True, nullable = False, unique = False)
    email = Column(String(64), index = True, nullable = False, unique = False)
   
    
    def __repr__(self):
        return f"<User {self.username}>"
    

    def update(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        
    
        

# create database. In case needed to remake database, delete current eyecu.db
# and run code below and then check to see if db is created then comment out
#db.create_all()
#db.session.commit()