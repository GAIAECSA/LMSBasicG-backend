from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Time,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class CourseAttendance(Base):
    __tablename__ = "course_attendances"

    id = Column(Integer, primary_key=True, index=True)

    day = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Claves foráneas (con index=True para rendimiento)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    course = relationship("Course",back_populates="course_attendances")
    business = relationship("Business",back_populates="course_attendances",)
    attendance = relationship("Attendance",back_populates="course_attendance",cascade="all, delete-orphan")