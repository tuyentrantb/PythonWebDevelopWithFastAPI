from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    company_id: Optional[UUID]

class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    company_id: UUID | None = None
    class Config:
        from_attributes = True

class UserViewModel(UserBaseModel):
    is_admin: bool
