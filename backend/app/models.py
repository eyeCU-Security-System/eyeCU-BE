from app import *


'''
user info table
CREATE TABLE User(
    id INTEGER NOT NULL AUTOINCREMENT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL
);
'''
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, nullable = False, unique = True)
    password = db.Column(db.String(64), index = True, nullable = False, unique = False)
    firstName = db.Column(db.String(64), index = True, nullable = False, unique = False)
    lastName = db.Column(db.String(64), index = True, nullable = False, unique = False)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self, username, password, firstName, lastName):
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        
    
        

# create database. In case needed to remake database, delete current eyecu.db
# and run code below and then check to see if db is created then comment out
#db.create_all()
#db.session.commit()