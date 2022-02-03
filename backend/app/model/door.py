
# from app import *


# '''
# user info table
# CREATE TABLE door_status(
#     is_locked NUMBER(1)
# );
# '''
# class Door(db.Model):
#     __tablename__ = 'door_status'
    
#     is_locked = db.Column(db.Boolean, unique = False, default = True)
    
#     def __repr__(self):
#         return f"<User {self.OCStatus}>"
    
#     def save(self):
#         db.session.add(self)
#         db.session.commit()
        
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
        
#     def update(self, is_locked):
#         self.is_locked = is_locked
    
        

# # create database. In case needed to remake database, delete current eyecu.db
# # and run code below and then check to see if db is created then comment out
# db.create_all()
# db.session.commit()