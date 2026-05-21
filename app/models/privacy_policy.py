from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class PrivacyPolicy(Base):
    __tablename__ = "privacy_policies"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    version = Column(String, nullable=False, unique=True)

    pdf_url = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    mandatory = Column(Boolean, default=True)

    effective_date = Column(DateTime(timezone=True), nullable=False)

    deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_acceptances = relationship(
        "UserPrivacyPolicy", back_populates="privacy_policy"
    )
