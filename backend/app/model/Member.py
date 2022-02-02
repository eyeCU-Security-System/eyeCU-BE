from sqlalchemy import *
from app.model.BaseModel import Base

class Member(Base):
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(32), index = True, nullable = False, unique = False)
    role = Column(String(15), index = True, nullable = False, unique = False)
    state = Column(String(12), index = True, nullable = False, unique = False)
    status = Column(String(12), index = True, nullable = False, unique = False)
    
    def __repr__(self):
        return f"<Member {self.role}:{self.id}>"
    
    # def save(self):
    #     session.add(self)
    #     session.commit()
        
    # def delete(self):
    #     session.delete(self)
    #     session.commit()
        
    def update(self, type, name, role, state, status):
        self.type = type
        self.name = name
        self.role = role
        self.state = state
        self.status = status