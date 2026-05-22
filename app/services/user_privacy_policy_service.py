from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import (
    user_privacy_policy_repo,
    privacy_policy_repo,
)


def accept_privacy_policy(db: Session, user_id: int, privacy_policy_id: int):
    existing = user_privacy_policy_repo.get_user_acceptance(
        db, user_id, privacy_policy_id
    )

    if existing:
        raise HTTPException(status_code=400, detail="Privacy policy already accepted")

    privacy_policy = privacy_policy_repo.get_by_id(db, privacy_policy_id)

    if not privacy_policy:
        raise HTTPException(status_code=404, detail="Privacy policy not found")

    return user_privacy_policy_repo.create(db, user_id, privacy_policy_id)


def check_active_privacy_policy_acceptance(db: Session, user_id: int):

    privacy_policy = privacy_policy_repo.get_active(db)

    if not privacy_policy:

        raise HTTPException(status_code=404, detail="No active privacy policy found")

    acceptance = user_privacy_policy_repo.get_user_acceptance(
        db, user_id, privacy_policy.id
    )

    return {
        "accepted": acceptance is not None,
        "privacy_policy_id": privacy_policy.id,
        "version": privacy_policy.version,
    }
