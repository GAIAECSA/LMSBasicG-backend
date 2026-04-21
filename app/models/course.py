from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Numeric, func, Enum, CheckConstraint
from app.db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10,2), nullable=False, default=0)
    is_free = Column(Boolean, nullable=False, default=False)
    level = Column(Enum("PRINCIPIANTE", "INTERMEDIO", "AVANZADO", name="course_level"),nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    open_enrollment = Column(Boolean, nullable=False, default=False)
    duration_hours = Column(Integer, nullable=False, default=0)
    total_lessons = Column(Integer, nullable=False, default=0)


    image_url = Column(String)
    discount_price = Column(Numeric(10,2))
    currency = Column(String, default="USD")
    published_at = Column(DateTime(timezone=True))
    rating = Column(Numeric(2,1))
    total_students = Column(Integer, default=0)

    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=False)


    deleted = Column(Boolean, index=True, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("trim(name) <> ''", name="name_not_blank"),
        CheckConstraint("trim(description) <> ''", name="description_not_blank"),
        CheckConstraint("price >= 0", name="price_positive"),
        CheckConstraint("duration_hours >= 0", name="duration_non_negative"),
        CheckConstraint("total_lessons >= 0", name="lessons_non_negative"),
    )