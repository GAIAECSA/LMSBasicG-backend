from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class BlockProgress(Base):
    __tablename__ = "block_progress"

    id = Column(Integer, primary_key=True, index=True)

    # Claves foráneas (con index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False, index=True)
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    is_completed = Column(Boolean, default=False, nullable=False)
    
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    deleted = Column(Boolean, index=True, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    enrollment = relationship("Enrollment", back_populates="block_progresses")
    lesson_block = relationship("LessonBlock", back_populates="block_progresses")
    business = relationship("Business", back_populates="block_progresses")

    __table_args__ = (
        UniqueConstraint("enrollment_id", "lesson_block_id", name="uq_enrollment_block"),
    )