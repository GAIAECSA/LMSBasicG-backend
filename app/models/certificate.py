from sqlalchemy import CheckConstraint, Column, Integer, ForeignKey, DateTime, String, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    final_grade = Column(Numeric(4, 2))
    course_name = Column(String)
    student_name = Column(String)
    certificate_code = Column(String, unique=True, nullable=False, index=True)
    file_url = Column(String, nullable=True)

    # Claves foráneas
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    is_valid = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, index=True, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) # Faltaba en tu código

    # Relaciones
    user = relationship("User", back_populates="certificates")
    course = relationship("Course", back_populates="certificates")
    business = relationship("Business", back_populates="certificates")

    __table_args__ = (
        CheckConstraint("final_grade >= 0", name="grade_non_negative"),
        CheckConstraint("trim(certificate_code) <> ''", name="certificate_code_not_blank"),
    )