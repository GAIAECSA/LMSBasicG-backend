from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class HomeworkResponse(Base):
    __tablename__ = "homework_responses"

    id = Column(Integer, primary_key=True, index=True)

    submitted_file_url = Column(String)
    submitted_filename = Column(String)
    comment = Column(Text)
    score = Column(Numeric(4, 2))
    status = Column(String)

    # Claves foráneas (con index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False, index=True)
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    enrollment = relationship("Enrollment", back_populates="homework_responses")
    lesson_block = relationship("LessonBlock", back_populates="homework_responses")
    business = relationship("Business", back_populates="homework_responses")

    __table_args__ = (
        CheckConstraint("score >= 0", name="homework_score_non_negative"),
    )
