import enum
from sqlalchemy import Column, String, Enum, SmallInteger, ForeignKey, Uuid
from schemas.base_entity import BaseEntity
from database import Base

class TaskStatus(enum.Enum):
    NEW = 'N'
    INPROGRESS = 'I'
    COMPLETE = 'C'
    
class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    summary = Column(String)
    description = Column(String)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.NEW)
    priority = Column(SmallInteger, nullable=False, default=0)
    user_id = Column(Uuid, ForeignKey("users.id"))
