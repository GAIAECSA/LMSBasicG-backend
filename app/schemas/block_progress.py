from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BlockProgressCreate(BaseModel):
    enrollment_id: int
    lesson_block_id: int

    is_completed: Optional[bool] = False

    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class BlockProgressUpdate(BaseModel):
    is_completed: Optional[bool] = None
    attempts: Optional[int] = None

    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class BlockProgressResponse(BaseModel):
    id: int
    enrollment_id: int
    lesson_block_id: int
    is_completed: bool


    class Config:
        orm_mode = True

    