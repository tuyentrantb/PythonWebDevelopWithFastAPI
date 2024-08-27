from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from schemas import TaskStatus
from models import UserViewModel

class SearchTaskModel():
    def __init__(self, summary, user_id, priority, page, size) -> None:
        self.summary = summary
        self.user_id = user_id
        self.priority = priority
        self.page = page
        self.size = size

class TaksModel(BaseModel):
    summary: str
    description: Optional[str]
    status: TaskStatus = Field(default=TaskStatus.NEW)
    priority: int = Field(ge=0, le=10, default=0)
    user_id: UUID
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Task 1",
                "description": "Description for Task 1",
                "status": "NEW",
                "priority": 1
            }
        }

class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str | None = None
    priority: int
    user_id: UUID
    user: UserViewModel

    class Config:
        from_attributes = True
