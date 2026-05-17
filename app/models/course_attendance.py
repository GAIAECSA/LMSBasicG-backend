from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean, Date, Time
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class CourseAttendance(Base):
    __tablename__ = "course_attendance"

    id = Column(Integer, primary_key=True, index=True)

    day = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )