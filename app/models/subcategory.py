from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, CheckConstraint
from app.db.base import Base

class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("trim(name) <> ''", name="name_not_blank"),
    )