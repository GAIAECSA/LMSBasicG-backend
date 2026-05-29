from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, AliasPath

from app.schemas.enrollment import EnrollmentBasicResponse

# ======================================
# BASE
# ======================================

class AttendanceBase(BaseModel):
    enrollment_id: int
    course_attendance_id: int
    attendance_state: str = "PENDIENTE"


# ======================================
# CREATE
# ======================================

class AttendanceCreate(AttendanceBase):
    pass


# ======================================
# UPDATE
# ======================================

class AttendanceUpdate(BaseModel):
    enrollment_id: Optional[int] = None
    course_attendance_id: Optional[int] = None
    attendance_state: Optional[str] = None
    deleted: Optional[bool] = None


# ======================================
# RESPONSE
# ======================================

class AttendanceResponse(AttendanceBase):
    id: int
    deleted: bool
    attendance_state: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    role_id: int = Field(validation_alias=AliasPath('enrollment', 'role_id'))
    
    model_config = ConfigDict(from_attributes=True)


# ======================================
# RESPONSE WITH ENROLLMENT
# ======================================

class AttendanceWithEnrollmentResponse(AttendanceResponse):
    enrollment: EnrollmentBasicResponse
