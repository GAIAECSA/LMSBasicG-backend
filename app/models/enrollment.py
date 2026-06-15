from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,          # Importado para el índice parcial
    Integer,
    String,
    Text,
    func,
    text,           # Importado para la condición SQL
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    accepted = Column(Boolean)
    comment = Column(Text)
    voucher_url = Column(String, nullable=True)
    reference_code = Column(String, nullable=True)

    # Claves foráneas
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones principales (Hacia arriba)
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    role = relationship("Role", back_populates="enrollments")
    business = relationship("Business", back_populates="enrollments")

    # Relaciones secundarias (Hacia abajo - Plurales)
    attendance = relationship("Attendance", back_populates="enrollment", cascade="all, delete-orphan")
    survey_responses = relationship("SurveyResponse", back_populates="enrollment", cascade="all, delete-orphan")
    homework_responses = relationship("HomeworkResponse", back_populates="enrollment", cascade="all, delete-orphan")
    forum_responses = relationship("ForumResponse", back_populates="enrollment", cascade="all, delete-orphan")
    quizz_responses = relationship("QuizzResponse", back_populates="enrollment", cascade="all, delete-orphan")
    block_progresses = relationship("BlockProgress", back_populates="enrollment", cascade="all, delete-orphan")

    __table_args__ = (
        # --- NUEVO ÍNDICE PARCIAL ---
        # Solo permite 1 registro activo para el mismo usuario, curso y negocio.
        # Permite múltiples registros eliminados (deleted = true).
        Index(
            "ix_uq_active_enrollment_user_course_bus",
            "user_id",
            "course_id",
            "business_id",
            unique=True,
            postgresql_where=text("deleted = false")
        ),
    )