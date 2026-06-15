from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255))
    phone = Column(String(50))
    is_active = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones (Plurales porque un Business tiene MUCHOS de estos elementos)
    lms_configs = relationship("BusinessLmsConfig", back_populates="business", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="business", cascade="all, delete-orphan")
    subcategories = relationship("Subcategory", back_populates="business", cascade="all, delete-orphan")
    courses = relationship("Course", back_populates="business", cascade="all, delete-orphan")
    users = relationship("User", back_populates="business", cascade="all, delete-orphan")
    modules = relationship("Module", back_populates="business", cascade="all, delete-orphan")
    lessons = relationship("Lesson", back_populates="business", cascade="all, delete-orphan")
    lesson_blocks = relationship("LessonBlock", back_populates="business", cascade="all, delete-orphan")
    certificate_templates = relationship("CertificateTemplate", back_populates="business", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="business", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="business", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="business", cascade="all, delete-orphan")
    course_attendances = relationship("CourseAttendance", back_populates="business", cascade="all, delete-orphan")
    forum_responses = relationship("ForumResponse", back_populates="business", cascade="all, delete-orphan")
    homework_responses = relationship("HomeworkResponse", back_populates="business", cascade="all, delete-orphan")
    mdt_certificates = relationship("MdtCertificate", back_populates="business", cascade="all, delete-orphan")
    privacy_policies = relationship("PrivacyPolicy", back_populates="business", cascade="all, delete-orphan")
    user_privacy_policies = relationship("UserPrivacyPolicy", back_populates="business", cascade="all, delete-orphan")
    quizz_responses = relationship("QuizzResponse", back_populates="business", cascade="all, delete-orphan")
    survey_responses = relationship("SurveyResponse", back_populates="business", cascade="all, delete-orphan")
    block_progresses = relationship("BlockProgress", back_populates="business", cascade="all, delete-orphan")