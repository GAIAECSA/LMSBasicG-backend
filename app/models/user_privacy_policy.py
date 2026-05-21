from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserPrivacyPolicy(Base):
    __tablename__ = "user_privacy_policies"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    privacy_policy_id = Column(
        Integer, ForeignKey("privacy_policies.id"), nullable=False
    )

    accepted = Column(Boolean, nullable=False, default=True)

    accepted_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="privacy_policies")

    privacy_policy = relationship("PrivacyPolicy", back_populates="user_acceptances")

    __table_args__ = (
        UniqueConstraint("user_id", "privacy_policy_id", name="uq_user_privacy_policy"),
    )
