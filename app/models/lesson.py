from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    func,
    CheckConstraint,
)
from app.db.base import Base

from sqlalchemy.orm import relationship

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False, default=0)

    # Claves foráneas
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, index=True, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    module = relationship("Module", back_populates="lessons")
    business = relationship("Business", back_populates="lessons")
    lesson_blocks = relationship("LessonBlock", back_populates="lesson", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("trim(name) <> ''", name="lesson_name_not_blank"),
        CheckConstraint('"order" >= 0', name="lesson_order_non_negative"),
    )
