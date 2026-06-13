from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    func,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False, default=0)

    # Claves foráneas
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, index=True, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    course = relationship("Course", back_populates="modules")
    business = relationship("Business", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("trim(name) <> ''", name="module_name_not_blank"),
        CheckConstraint('"order" >= 0', name="module_order_non_negative"),
    )
