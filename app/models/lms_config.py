from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class LmsConfig(Base):
    __tablename__ = "lms_configs"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    description = Column(String)

    is_active = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, index=True, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    business_configs = relationship(
        "BusinessLmsConfig",
        back_populates="lms_config",
        cascade="all, delete-orphan",
    )
