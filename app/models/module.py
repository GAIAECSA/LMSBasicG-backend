from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, CheckConstraint
from app.db.base import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    deleted = Column(Boolean, index=True, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("trim(name) <> ''", name="module_name_not_blank"),
        CheckConstraint("trim(description) <> ''", name="module_description_not_blank"),
        CheckConstraint("order >= 0", name="module_order_non_negative"),
    )