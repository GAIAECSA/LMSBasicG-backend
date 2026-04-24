from pydantic import BaseModel, field_validator
from typing import Optional
from fastapi import Form
from app.schemas.user import UserBasicResponse
from app.schemas.course import CourseBasicResponse
from app.schemas.role import RoleBasicResponse

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
    
    user_id: Optional[int] = None
    course_id: Optional[int] = None
    role_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        accepted: Optional[bool] = Form(None),
        reference_code: Optional[str] = Form(None),
        comment: Optional[str] = Form(None),
        user_id: Optional[int] = Form(None),
        course_id: Optional[int] = Form(None),
        role_id: Optional[int] = Form(None),
    ):
        return cls(
            accepted=accepted,
            reference_code=reference_code,
            comment=comment,
            user_id=user_id,
            course_id=course_id,
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