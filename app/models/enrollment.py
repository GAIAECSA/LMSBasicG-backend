from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from app.db.base import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    accepted = Column(Boolean)
    comment = Column(Text)
    voucher_url = Column(String, nullable=True)
    reference_code = Column(String, nullable=True)

    # Claves foráneas
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones principales (Hacia arriba)
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    role = relationship("Role", back_populates="enrollments")
    business = relationship("Business", back_populates="enrollments")

    # Relaciones secundarias (Hacia abajo - Plurales)
    attendance = relationship("Attendance", back_populates="enrollment", cascade="all, delete-orphan")
    survey_responses = relationship("SurveyResponse", back_populates="enrollment", cascade="all, delete-orphan")
    homework_responses = relationship("HomeworkResponse", back_populates="enrollment", cascade="all, delete-orphan")
    forum_responses = relationship("ForumResponse", back_populates="enrollment", cascade="all, delete-orphan")
    quizz_responses = relationship("QuizzResponse", back_populates="enrollment", cascade="all, delete-orphan")
    block_progresses = relationship("BlockProgress", back_populates="enrollment", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "course_id",
            name="uq_user_course"
        ),
    )
