from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import date, time


class CourseAttendanceCreate(BaseModel):
    course_id: int
    day: date
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def validate_hours(self):
        if self.end_time <= self.start_time:
            raise ValueError("La hora de fin debe ser mayor a la hora de inicio")
        return self


class CourseAttendanceUpdate(BaseModel):
    course_id: Optional[int] = None
    day: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

    @model_validator(mode="after")
    def validate_hours(self):
        if (
            self.start_time is not None and
            self.end_time is not None and
            self.end_time <= self.start_time
        ):
            raise ValueError("La hora de fin debe ser mayor a la hora de inicio")
        return self


class CourseAttendanceResponse(BaseModel):
    id: int
    course_id: int
    day: date
    start_time: time
    end_time: time

    class Config:
        from_attributes = True