from typing import Optional

from fastapi import Form
from pydantic import BaseModel, field_validator

from app.schemas.course import CourseBasicResponse
from app.schemas.role import RoleBasicResponse
from app.schemas.user import UserBasicResponse, UserCreate


class EnrollmentCreate(BaseModel):

    accepted: Optional[bool] = None
    reference_code: Optional[str] = None
    comment: Optional[str] = None

    user_id: int
    course_id: int
    role_id: int

    @classmethod
    def as_form(
        cls,
        accepted: Optional[bool] = Form(None),
        reference_code: Optional[str] = Form(None),
        comment: Optional[str] = Form(None),
        user_id: int = Form(...),
        course_id: int = Form(...),
        role_id: int = Form(...),
    ):
        return cls(
            accepted=accepted,
            reference_code=reference_code,
            comment=comment,
            user_id=user_id,
            course_id=course_id,
            role_id=role_id,
        )


class EnrollmentUpdate(BaseModel):

    accepted: Optional[bool] = None
    comment: Optional[str] = None
    reference_code: Optional[str] = None

    role_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        accepted: Optional[bool] = Form(None),
        reference_code: Optional[str] = Form(None),
        comment: Optional[str] = Form(None),
        role_id: Optional[int] = Form(None),
    ):
        return cls(
            accepted=accepted,
            reference_code=reference_code,
            comment=comment,
            role_id=role_id,
        )


class EnrollmentResponse(BaseModel):
    id: int
    accepted: Optional[bool]
    reference_code: Optional[str] = None
    comment: Optional[str] = None
    voucher_url: Optional[str] = None

    user: UserBasicResponse
    course: CourseBasicResponse
    role: RoleBasicResponse

    class Config:
        from_attributes = True


class EnrollmentBasicResponse(BaseModel):
    id: int
    role_id: int
    user: UserBasicResponse

    class Config:
        from_attributes = True


class MassiveEnrollmentCreate(BaseModel):
    course_id: int
    users: list[UserCreate]


class MassiveEnrollmentResult(BaseModel):
    created: list[dict]
    skipped: list[dict]
    failed: list[dict]
    summary: dict
