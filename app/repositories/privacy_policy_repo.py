from sqlalchemy.orm import Session

from app.models.privacy_policy import PrivacyPolicy
from app.schemas.privacy_policy import (
    PrivacyPolicyCreate,
    PrivacyPolicyUpdate,
)


def create(db: Session, data: PrivacyPolicyCreate):
    privacy_policy = PrivacyPolicy(**data.model_dump())

    db.add(privacy_policy)
    db.commit()
    db.refresh(privacy_policy)

    return privacy_policy


def get_all(db: Session):
    return db.query(PrivacyPolicy).filter(PrivacyPolicy.deleted == False).all()


def get_by_id(db: Session, privacy_policy_id: int):
    return (
        db.query(PrivacyPolicy)
        .filter(PrivacyPolicy.id == privacy_policy_id, PrivacyPolicy.deleted == False)
        .first()
    )


def get_active_policy(db: Session):
    return (
        db.query(PrivacyPolicy)
        .filter(PrivacyPolicy.is_active == True, PrivacyPolicy.deleted == False)
        .order_by(PrivacyPolicy.effective_date.desc())
        .first()
    )


def update(db: Session, privacy_policy: PrivacyPolicy, data: PrivacyPolicyUpdate):
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(privacy_policy, key, value)

    db.commit()
    db.refresh(privacy_policy)

    return privacy_policy


def delete(db: Session, privacy_policy: PrivacyPolicy):
    privacy_policy.deleted = True

    db.commit()

    return privacy_policy
