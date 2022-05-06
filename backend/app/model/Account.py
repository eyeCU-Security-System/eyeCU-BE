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
    username = Column(String(64), index = True, nullable = False, unique = False)
    password = Column(String(64), index = True, nullable = False, unique = False)
    email = Column(String(64), index = True, nullable = False, unique = True)
   
    
    def __repr__(self):
        return f"<User {self.username}>"
    

    def update(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        
    
        
