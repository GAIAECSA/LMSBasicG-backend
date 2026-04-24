from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, CheckConstraint, JSON
from app.db.base import Base

class LessonBlockType(Base):
    __tablename__ = "lesson_block_types"

    id = Column(Integer, primary_key=True, index=True)

    key = Column(String, unique=True, nullable=False) 
    name = Column(String, nullable=False)      

    description = Column(String)
    icon = Column(String)
    content_type = Column(String)

    config = Column(JSON)

    is_active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("trim(name) <> ''", name="name_not_blank"),
        CheckConstraint("trim(key) <> ''", name="key_not_blank"),
    )
