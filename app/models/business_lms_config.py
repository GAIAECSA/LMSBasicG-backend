from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class BusinessLmsConfig(Base):
    __tablename__ = "business_lms_configs"

    id = Column(Integer, primary_key=True)

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
    )

    lms_config_id = Column(
        Integer,
        ForeignKey("lms_configs.id"),
        nullable=False,
    )

    config = Column(JSONB, nullable=False)

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

    business = relationship(
        "Business",
        back_populates="lms_configs",
    )

    lms_config = relationship(
        "LmsConfig",
        back_populates="business_configs",
    )
w