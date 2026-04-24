from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base

class LessonBlock(Base):
    __tablename__ = "lesson_blocks"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(JSONB, nullable=False)

    is_required = Column(Boolean, default=True)
    completion_type = Column(String)
    completion_value = Column(Integer)
    order = Column(Integer, default=0)

    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    block_type_id = Column(Integer, ForeignKey("lesson_block_types.id"), nullable=False)

    is_active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    lesson_block_type= relationship("LessonBlockType")

    __table_args__ = (
        CheckConstraint("content <> '{}'::jsonb", name="content_not_empty"),
    )   

