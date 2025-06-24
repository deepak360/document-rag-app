from pydantic import BaseModel
from datetime import datetime
from typing import List

class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserFileOut(BaseModel):
    id: int
    filename: str
    path: str
    created_at: datetime

    class Config:
        orm_mode = True