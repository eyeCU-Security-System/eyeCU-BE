from sqlalchemy import *
from app.model.BaseModel import Base

'''
Faces info table
CREATE TABLE Faces(
    id INTEGER NOT NULL AUTOINCREMENT PRIMARY KEY,
    picture TEXT NOT NULL 
    user_id FK Account.id
);
'''

class Faces(Base):
    __tablename__='faces'
    
    id = Column(Integer, primary_key=True)
    picture_file = Column(String(64), nullable=False, default='account_face.jpeg')
    face_name = Column(String(64), nullable=False)
    mimetype = Column(String(64), nullable=False)
    user_id = Column(Integer, ForeignKey('accounts.id'))
    
