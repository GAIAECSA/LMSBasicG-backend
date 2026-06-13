from sqlalchemy import (
    CheckConstraint,
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    Numeric,
)

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base


class QuizzResponse(Base):
    __tablename__ = "quizz_responses" # Corregido a plural

    id = Column(Integer, primary_key=True, index=True)
    quizz = Column(JSONB, nullable=False)
    response = Column(JSONB, nullable=False)
    score = Column(Numeric(4, 2), nullable=False)
    is_passed = Column(Boolean, nullable=False)

    # Claves foráneas
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False, index=True)
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    enrollment = relationship("Enrollment", back_populates="quizz_responses")
    lesson_block = relationship("LessonBlock", back_populates="quizz_responses")
    business = relationship("Business", back_populates="quizz_responses")

    __table_args__ = (
        CheckConstraint("score >= 0", name="quizz_score_non_negative"),
    )