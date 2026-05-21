from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Any


class SurveyResponseBase(BaseModel):
    enrollment_id: int
    lesson_block_id: int
    survey: dict[str, Any] | None = None
    response: dict[str, Any] | None = None
    score: Decimal | None = None


class SurveyResponseCreate(SurveyResponseBase):
    pass


class SurveyResponseUpdate(BaseModel):
    survey: dict[str, Any] | None = None
    response: dict[str, Any] | None = None
    score: Decimal | None = None
    deleted: bool | None = None


class SurveyResponseResponse(SurveyResponseBase):
    id: int
    deleted: bool
    created_at: datetime

    class Config:
        from_attributes = True