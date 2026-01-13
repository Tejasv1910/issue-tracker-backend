from pydantic import BaseModel
from typing import List

class LabelCreate(BaseModel):
    name: str

class LabelAssign(BaseModel):
    labels: List[str]
