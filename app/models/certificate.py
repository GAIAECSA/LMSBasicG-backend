from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean, Numeric
from sqlalchemy.sql import func
from app.db.base import Base

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    final_grade = Column(Numeric(4, 2), nullable=False)
    course_name = Column(String, nullable=False)
    student_name = Column(String, nullable=False)

    certificate_code = Column(String, unique=True, nullable=False, index=True)
    file_url = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("certificate_templates.id"), nullable=True)

    is_valid = Column(Boolean, default=True)
    deleted = Column(Boolean, index=True, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())