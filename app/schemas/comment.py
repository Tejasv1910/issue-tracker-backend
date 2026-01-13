from pydantic import BaseModel, Field

class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1)
