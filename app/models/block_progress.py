from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class BlockProgress(Base):
    __tablename__ = "block_progress"

    id = Column(Integer, primary_key=True)

    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"), nullable=False)

    is_completed = Column(Boolean, default=False)

    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    deleted = Column(Boolean, index=True, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    #enrollment = relationship("Enrollment", backref="progress")
    #lesson_block = relationship("LessonBlock", backref="progress")

    __table_args__ = (
        UniqueConstraint("enrollment_id", "lesson_block_id", name="uq_enrollment_block"),
    )