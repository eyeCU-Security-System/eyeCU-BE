from sqlalchemy import *
from app.model.BaseModel import Base

class Device(Base):
    __tablename__ = 'devices'
    
    id = Column(Integer, primary_key = True)
    type = Column(String(32), index = True, nullable = False, unique = False)
    name = Column(String(32), index = True, nullable = False, unique = False)
    secret = Column(String(32), index = True, nullable = False, unique = True)
    state = Column(String(12), index = True, nullable = False, unique = False)
    status = Column(String(12), index = True, nullable = False, unique = False)
    
    def __repr__(self):
        return f"<Device {self.type}:{self.id}>"
    
    # def save(self):
    #     session.add(self)
    #     session.commit()
        
    # def delete(self):
    #     session.delete(self)
    #     session.commit()
        
    def update(self, type, name, secret, state, status):
        self.type = type
        self.name = name
        self.secret = secret
        self.state = state
        self.status = status    
