from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, CheckConstraint
from app.db.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False, default=0)
    
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)

    deleted = Column(Boolean, index=True, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("trim(name) <> ''", name="name_not_blank"),
        CheckConstraint('"order" >= 0', name="module_order_non_negative"),
    )