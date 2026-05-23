from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import Form
from pydantic import BaseModel, Field


class HomeworkResponseCreate(BaseModel):
    enrollment_id: int = Field(..., gt=0)

    lesson_block_id: int = Field(..., gt=0)

    comment: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        enrollment_id: int = Form(...),
        lesson_block_id: int = Form(...),
        comment: Optional[str] = Form(None),
    ):
        return cls(
            enrollment_id=enrollment_id,
            lesson_block_id=lesson_block_id,
            comment=comment,
        )


class HomeworkResponseUpdate(BaseModel):
    comment: Optional[str] = None

    status: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        comment: Optional[str] = Form(None),
        status: Optional[str] = Form(None),
    ):
        return cls(
            comment=comment,
            status=status,
        )


class HomeworkResponseGrade(BaseModel):
    score: Decimal = Field(..., ge=0, le=10)

    comment: Optional[str] = None

    status: Optional[str] = "reviewed"

    @classmethod
    def as_form(
        cls,
        score: Decimal = Form(...),
        comment: Optional[str] = Form(None),
        status: Optional[str] = Form("reviewed"),
    ):
        return cls(
            score=score,
            comment=comment,
            status=status,
        )


class HomeworkResponseResponse(BaseModel):
    id: int

    enrollment_id: int

    lesson_block_id: int

    submitted_file_url: Optional[str] = None

    submitted_filename: Optional[str] = None

    comment: Optional[str] = None

    score: Optional[Decimal] = None

    status: Optional[str] = None

    deleted: bool

    created_at: datetime

    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
