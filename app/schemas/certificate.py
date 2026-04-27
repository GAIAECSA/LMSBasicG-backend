from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
from fastapi import Form
from app.utils.file_upload import save_lesson_file


class CertificateCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    course_id: int = Field(..., gt=0)

    @classmethod
    def as_form(
        cls,
        user_id: int = Form(...),
        course_id: int = Form(...),
    ):
        return cls(
            user_id=user_id,
            course_id=course_id,
        )

class CertificateUpdate(BaseModel):
    is_valid: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        is_valid: Optional[bool] = Form(None),
    ):
        return cls(
            is_valid=is_valid,
        )

class CertificateResponse(BaseModel):
    id: int

    user_id: int
    course_id: int

    student_name: str
    course_name: str
    final_grade: Decimal

    certificate_code: str
    file_url: Optional[str]

    is_valid: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }