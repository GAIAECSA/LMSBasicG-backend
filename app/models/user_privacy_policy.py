from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserPrivacyPolicy(Base):
    __tablename__ = "user_privacy_policies"

    id = Column(Integer, primary_key=True, index=True)
    accepted = Column(Boolean, nullable=False, default=True)
    accepted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Claves foráneas
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    privacy_policy_id = Column(Integer, ForeignKey("privacy_policies.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    user = relationship("User", back_populates="privacy_policies")
    privacy_policy = relationship("PrivacyPolicy", back_populates="user_acceptances")
    business = relationship("Business", back_populates="user_privacy_policies")

    __table_args__ = (
        UniqueConstraint("user_id", "privacy_policy_id", name="uq_user_privacy_policy"),
    )