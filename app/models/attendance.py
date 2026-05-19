from sqlalchemy import (Column,Integer,Boolean,DateTime,ForeignKey,Enum,UniqueConstraint,func)
from sqlalchemy.orm import relationship
from app.db.base import Base

class Attendance(Base):
    __tablename__ = "attendance"

    __table_args__ = (
        UniqueConstraint(
            "enrollment_id",
            "course_attendance_id",
            name="uq_attendance_student_session"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer,ForeignKey("enrollments.id"),nullable=False)
    course_attendance_id = Column(Integer,ForeignKey("course_attendance.id"),nullable=False)
    attendance_state = Column(Enum("PRESENTE","PENDIENTE","FALTA",name="attendance_state"),nullable=False,default="PENDIENTE")

    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())

    enrollment = relationship("Enrollment",back_populates="attendances")
    course_attendance = relationship("CourseAttendance",back_populates="attendances")