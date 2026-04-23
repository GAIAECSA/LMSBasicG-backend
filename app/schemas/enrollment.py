from pydantic import BaseModel, field_validator
from typing import Optional

class EnrollmentCreate(BaseModel):
    
    accepted: Optional[bool] = None
    
    student_id: int
    course_id: int
    role_id: int

class EnrollmentUpdate(BaseModel):
    
    accepted: Optional[bool] = None
    
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    role_id: Optional[int] = None

class EnrollmentResponse(BaseModel):
    id: int
    
    accepted: bool
    
    student_id: int
    course_id: int
    role_id: int

    class Config:
        from_attributes = True