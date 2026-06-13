from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    enrollments = relationship("Enrollment", back_populates="role")
    users = relationship("User", back_populates="role")

    __table_args__ = (CheckConstraint("trim(name) <> ''", name="name_not_blank"),)
