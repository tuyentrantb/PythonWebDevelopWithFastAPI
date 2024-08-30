from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from models import UserBaseModel
from schemas import TaskStatus

class SearchTaskModel():
    def __init__(self, summary, description, priority, user_id, page, size) -> None:
        self.summary = summary
        self.description = description
        self.priority = priority
        self.user_id = user_id
        self.page = page
        self.size = size

class TaskModel(BaseModel):
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
                "status": "N",
                "priority": 4,
                "user_id": ""
            }
        }

class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str | None = None
    priority: int
    user_id: UUID

    class Config:
        from_attributes = True
