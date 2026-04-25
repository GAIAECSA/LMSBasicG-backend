from pydantic import BaseModel
from typing import Optional
from app.schemas.enrollment import EnrollmentBasicResponse

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

    lesson_block_id: int

    quizz: str
    response: str

    score: Optional[int]
    is_passed: Optional[bool]

    created_at: datetime
    enrollment: EnrollmentBasicResponse

    class Config:
        orm_mode = True