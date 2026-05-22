from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.enrollment import EnrollmentBasicResponse
from decimal import Decimal
from datetime import datetime


class QuizzResponseCreate(BaseModel):

    enrollment_id: int
    lesson_block_id: int
    quizz: str
    response: str

    score: Optional[Decimal] = None
    is_passed: Optional[bool] = None


class QuizzResponseUpdate(BaseModel):

    response: Optional[str] = None
    score: Optional[Decimal] = None
    is_passed: Optional[bool] = None


class QuizzResponseResponse(BaseModel):
    id: int

    lesson_block_id: int

    quizz: str
    response: str

    score: Optional[Decimal] = None
    is_passed: Optional[bool] = None

    created_at: datetime

    enrollment: EnrollmentBasicResponse

    model_config = ConfigDict(from_attributes=True)
