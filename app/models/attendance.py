from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    
    attendance_state = Column(Enum("PRESENTE", "PENDIENTE", "AUSENTE", name="attendance_state"),nullable=False,default="PENDIENTE",)

    # Claves foráneas (con index=True para rendimiento)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False, index=True)
    course_attendance_id = Column(Integer, ForeignKey("course_attendances.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    enrollment = relationship("Enrollment",back_populates="attendance")
    course_attendance = relationship("CourseAttendance",back_populates="attendance")
    business = relationship("Business",back_populates="attendances")

    __table_args__ = (
        UniqueConstraint(
            "enrollment_id",
            "course_attendance_id",
            name="uq_attendance_student_session",
        ),
    )