from sqlalchemy import *
#import variable Base instantiated from BaseModel.py file as a base class
# Note: base class is a class with pre-implemented functions to interact with database 
from app.model.BaseModel import Base

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key = True)
    username = Column(String(64), index = True, nullable = False, unique = True)
    password = Column(String(64), index = True, nullable = False, unique = False)
    phone = Column(String(12), index = True, nullable = False, unique = False)
    email = Column(String(32), index = True, nullable = False, unique = False)
    
    def __repr__(self):
        return f"<Account {self.username}>"
        
    def update(self, username, password, phone, email):
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email

