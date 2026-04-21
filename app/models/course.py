from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Numeric, func
from app.db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    image_url = Column(String)
    price = Column(Numeric(10,2), nullable=False)
    discount_price = Column(Numeric(10,2))
    is_free = Column(Boolean, default=False)
    currency = Column(String, default="USD")

    level = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    instructor_id = Column(Integer, ForeignKey("users.id"))

    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))

    rating = Column(Numeric(2,1))
    total_students = Column(Integer, default=0)

    duration_minutes = Column(Integer)
    total_lessons = Column(Integer)

    deleted = Column(Boolean, index=True, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())