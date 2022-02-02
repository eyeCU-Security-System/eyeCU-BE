from sqlalchemy import *
from app.model.BaseModel import Base

class Permission(Base):
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key = True)
    type = Column(String(12), index = True, nullable = False, unique = False)
    status = Column(String(12), index = True, nullable = False, unique = False)
    entry_count = Column(Integer, index = False, nullable = False, unique = False)
    device_id = Column(Integer, ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"<Permission {self.type}:{self.member_id}:{self.device_id}>"
    
    # def save(self):
    #     session.add(self)
    #     session.commit()
        
    # def delete(self):
    #     session.delete(self)
    #     session.commit()
        
    def update(self, type, status, entry_count, device_id, member_id):
        self.type = type
        self.entry_count = entry_count
        self.device_id = device_id
        self.status = status
        self.member_id = member_id