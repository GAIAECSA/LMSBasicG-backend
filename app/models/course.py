from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False, default=0)
    is_free = Column(Boolean, nullable=False, default=False)
    level = Column(Enum("PRINCIPIANTE", "INTERMEDIO", "AVANZADO", name="course_level"), nullable=False)
    is_published = Column(Boolean, nullable=False, default=True)
    open_enrollment = Column(Boolean, nullable=False, default=False)
    duration_hours = Column(Integer, nullable=False, default=0)
    total_lessons = Column(Integer, nullable=False, default=0)
    is_mdt = Column(Boolean, nullable=False, default=False)
    image_url = Column(String)
    discount_price = Column(Numeric(10, 2))
    currency = Column(String, default="USD")
    published_at = Column(DateTime(timezone=True))
    rating = Column(Numeric(2, 1))
    total_students = Column(Integer, default=0)
    init_date = Column(Date, nullable=True)    # En MDT para no permitir matriculas
    finish_date = Column(Date, nullable=True)  # En MDT para no permitir cambios
    deleted = Column(Boolean, index=True, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Claves foráneas
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=False)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    # Relaciones
    business = relationship("Business", back_populates="courses") # Singular
    subcategory = relationship("Subcategory", back_populates="courses") # Singular
    course_attendances = relationship("CourseAttendance", back_populates="course", cascade="all, delete-orphan") # Plural
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan") # Plural
    lesson_blocks = relationship("LessonBlock",back_populates="course")
    mdt_certificates = relationship("MdtCertificate", back_populates="course") # Plural
    certificate_templates = relationship("CertificateTemplate", back_populates="course", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("trim(name) <> ''", name="name_not_blank"),
        CheckConstraint("trim(description) <> ''", name="description_not_blank"),
        CheckConstraint("price >= 0", name="price_positive"),
        CheckConstraint("duration_hours >= 0", name="duration_non_negative"),
        CheckConstraint("total_lessons >= 0", name="lessons_non_negative"),
    )