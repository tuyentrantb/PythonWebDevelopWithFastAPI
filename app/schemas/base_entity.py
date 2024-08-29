import uuid
from sqlalchemy import Column, Uuid, Time

class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
