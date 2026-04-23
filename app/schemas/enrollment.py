from pydantic import BaseModel, field_validator
from typing import Optional
from fastapi import Form

class EnrollmentCreate(BaseModel):
    
    accepted: Optional[bool] = None
    
    student_id: int
    course_id: int
    role_id: int

    @classmethod
    def as_form(
        cls,
        accepted: Optional[bool] = Form(None),
        student_id: int = Form(...),
        course_id: int = Form(...),
        role_id: int = Form(...),
    ):
        return cls(
            accepted=accepted,
            student_id=student_id,
            course_id=course_id,
            role_id=role_id,
        )

class EnrollmentUpdate(BaseModel):
    
    accepted: Optional[bool] = None
    
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    role_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        accepted: Optional[bool] = Form(None),
        student_id: Optional[int] = Form(None),
        course_id: Optional[int] = Form(None),
        role_id: Optional[int] = Form(None),
    ):
        return cls(
            accepted=accepted,
            student_id=student_id,
            course_id=course_id,
            role_id=role_id,
        )

class EnrollmentResponse(BaseModel):
    id: int
    
    accepted: bool
    
    student_id: int
    course_id: int
    role_id: int

    class Config:
        from_attributes = True