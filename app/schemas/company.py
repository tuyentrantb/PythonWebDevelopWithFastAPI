import enum
from sqlalchemy import Column, String, Enum, SmallInteger
from sqlalchemy.orm import relationship
from schemas.base_entity import BaseEntity
from database import Base

class CompanyMode(enum.Enum):
    DRAFT = 'D'
    PUBLISHED = 'P'
    
class Company(BaseEntity, Base):
    __tablename__ = "companies"

    name = Column(String)
    description = Column(String)
    rating = Column(SmallInteger, nullable=False, default=0)
    mode = Column(Enum(CompanyMode), nullable=False, default=CompanyMode.DRAFT)
    
    users = relationship("User", back_populates="company")