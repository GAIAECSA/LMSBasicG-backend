from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base


class LessonBlock(Base):
    __tablename__ = "lesson_blocks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(JSONB, nullable=False)
    counts_toward_grade = Column(Boolean, default=True, nullable=False)
    completion_type = Column(String)
    completion_value = Column(Integer)
    order = Column(Integer, default=0)
    default = Column(Boolean, default=False, nullable=False)
    date_available = Column(DateTime(timezone=True))

    # Claves foráneas
    lesson_id = Column(Integer, ForeignKey("lessons.id"), index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), default=None, index=True)
    block_type_id = Column(Integer, ForeignKey("lesson_block_types.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    is_active = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    lesson = relationship("Lesson", back_populates="lesson_blocks")
    course = relationship("Course",back_populates="lesson_blocks",foreign_keys=[course_id])
    business = relationship("Business", back_populates="lesson_blocks")
    lesson_block_type = relationship("LessonBlockType")
    
    survey_responses = relationship("SurveyResponse", back_populates="lesson_block")
    homework_responses = relationship("HomeworkResponse", back_populates="lesson_block")
    forum_responses = relationship("ForumResponse", back_populates="lesson_block")
    quizz_responses = relationship("QuizzResponse", back_populates="lesson_block")
    block_progresses = relationship("BlockProgress", back_populates="lesson_block", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("content <> '{}'::jsonb", name="content_not_empty"),
        CheckConstraint('"order" >= 0', name="lesson_block_order_non_negative"),
    )