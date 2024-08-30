from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from schemas import CompanyMode

class SearchCompanyModel():
    def __init__(self, name, page, size) -> None:
        self.name = name
        self.page = page
        self.size = size

class CompanyModel(BaseModel):
    name: str
    description: Optional[str]
    rating: int = Field(ge=0, le=5, default=0)
    mode: CompanyMode = Field(default=CompanyMode.DRAFT)
    class Config:
        from_attributes = True

class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    rating: int

    class Config:
        from_attributes = True
