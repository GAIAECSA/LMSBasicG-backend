from sqlalchemy import CheckConstraint, Column, Integer, Boolean, DateTime, ForeignKey, func, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    survey = Column(JSONB)
    response = Column(JSONB)
    score = Column(Numeric)

    # Claves foráneas
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False, index=True)
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    enrollment = relationship("Enrollment", back_populates="survey_responses")
    lesson_block = relationship("LessonBlock", back_populates="survey_responses")
    business = relationship("Business", back_populates="survey_responses")

    __table_args__ = (
        CheckConstraint("score >= 0", name="survey_score_non_negative"),
    )