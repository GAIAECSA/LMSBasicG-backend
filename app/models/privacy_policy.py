from sqlalchemy import (
    CheckConstraint,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from app.db.base import Base


class PrivacyPolicy(Base):
    __tablename__ = "privacy_policies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    version = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    mandatory = Column(Boolean, default=True, nullable=False)
    effective_date = Column(DateTime(timezone=True), nullable=False)

    # Claves foráneas
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    business = relationship("Business", back_populates="privacy_policies")
    user_acceptances = relationship("UserPrivacyPolicy", back_populates="privacy_policy",cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint(
            "business_id",
            "version",
            name="uq_business_policy_version"
        ),
        CheckConstraint(
            "trim(title) <> ''",
            name="privacy_title_not_blank"
        ),
    )
