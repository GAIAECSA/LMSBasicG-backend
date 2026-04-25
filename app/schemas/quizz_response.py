from pydantic import BaseModel, field_validator
from typing import Optional

class QuizzResponseCreate(BaseModel):

    enrollment_id: int
    lesson_block_id: int
    quizz: str
    response: str
    score: Optional[int] = None
    is_passed: Optional[bool] = None

class QuizzResponseUpdate(BaseModel):

    response: Optional[str] = None
    score: Optional[int] = None
    is_passed: Optional[bool] = None

from datetime import datetime


class QuizzResponseResponse(BaseModel):
    id: int

    enrollment_id: int
    lesson_block_id: int

    quizz: str
    response: str

    score: Optional[int]
    is_passed: Optional[bool]

    created_at: datetime

    class Config:
        orm_mode = True