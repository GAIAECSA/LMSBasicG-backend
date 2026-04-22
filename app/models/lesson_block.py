from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, CheckConstraint, ForeignKey, JSON
from app.db.base import Base

class LessonBlock(Base):
    __tablename__ = "lesson_block_types"

    id = Column(Integer, primary_key=True, index=True)

    order = Column(Integer, nullable=False, default=0)
    content = Column(JSON, nullable=False)

    lesson_block_type_id = Column(Integer, ForeignKey("lesson_block_types.id"), nullable=False)
    reference_id = Column(Integer)

    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("trim(name) <> ''", name="name_not_blank"),
    )