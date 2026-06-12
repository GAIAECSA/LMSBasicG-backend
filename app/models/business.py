from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False)

    domain = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(String(255))
    phone = Column(String(50))

    is_active = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    lms_configs = relationship(
        "BusinessLmsConfig",
        back_populates="business",
        cascade="all, delete-orphan",
    )
