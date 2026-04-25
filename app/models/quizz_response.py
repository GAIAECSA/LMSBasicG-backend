from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class QuizzResponse(Base):
    __tablename__ = "quizz_attempts"

    id = Column(Integer, primary_key=True)

    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"))

    quizz = Column(JSONB, nullable=False)
    response = Column(JSONB, nullable=False)

    score = Column(Integer)
    is_passed = Column(Boolean)

    created_at = Column(DateTime, server_default=func.now())