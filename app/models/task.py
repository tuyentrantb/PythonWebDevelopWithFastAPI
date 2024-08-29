from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from schemas import TaskStatus

class SearchTaskModel():
    def __init__(self, summary, user_id, priority, page, size) -> None:
        self.summary = summary
        self.user_id = user_id
        self.priority = priority
        self.page = page
        self.size = size

class TaskModel(BaseModel):
    summary: str
    description: Optional[str]
    status: TaskStatus = Field(default=TaskStatus.NEW)
    priority: int = Field(ge=0, le=10, default=0)
    user_id: UUID
    class Config:
        from_attributes = True

class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str | None = None
    priority: int
    user_id: UUID

    class Config:
        from_attributes = True
