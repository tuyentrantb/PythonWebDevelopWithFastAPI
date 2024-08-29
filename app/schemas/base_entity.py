import uuid
from sqlalchemy import Column, Uuid, Time

class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)
