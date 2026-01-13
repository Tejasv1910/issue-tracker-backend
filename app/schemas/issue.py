from pydantic import BaseModel
from typing import Optional
from typing import List

class IssueCreate(BaseModel):
    title: str
    description: str | None = None


class IssueResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    version: int

    class Config:
        orm_mode = True

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    version: int

class BulkStatusUpdate(BaseModel):
    issue_ids: List[int]
    status: str