from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True)

    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"), nullable=False)

    survey = Column(JSONB)
    response = Column(JSONB)
    score = Column(Numeric)

    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    enrollment = relationship("Enrollment", back_populates="survey_responses")
    lesson_block = relationship("LessonBlock", back_populates="survey_responses")