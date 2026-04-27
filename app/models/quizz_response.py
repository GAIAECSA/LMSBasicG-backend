from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class QuizzResponse(Base):
    __tablename__ = "quizz_response"

    id = Column(Integer, primary_key=True)

    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"))

    quizz = Column(JSONB, nullable=False)
    response = Column(JSONB, nullable=False)

    score = Column(Numeric(4, 2), nullable=False)
    is_passed = Column(Boolean)

    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    enrollment = relationship("Enrollment", backref="progress")
    lesson_block = relationship("LessonBlock", backref="progress")