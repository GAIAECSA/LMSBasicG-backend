from sqlalchemy.orm import Session

from app.models.user_privacy_policy import UserPrivacyPolicy


def create(db: Session, user_id: int, privacy_policy_id: int):
    acceptance = UserPrivacyPolicy(
        user_id=user_id, privacy_policy_id=privacy_policy_id, accepted=True
    )

    db.add(acceptance)
    db.commit()
    db.refresh(acceptance)

    return acceptance


def get_user_acceptance(db: Session, user_id: int, privacy_policy_id: int):
    return (
        db.query(UserPrivacyPolicy)
        .filter(
            UserPrivacyPolicy.user_id == user_id,
            UserPrivacyPolicy.privacy_policy_id == privacy_policy_id,
        )
        .first()
    )


from sqlalchemy.orm import joinedload


def get_by_privacy_policy_id(db: Session, privacy_policy_id: int):
    return (
        db.query(UserPrivacyPolicy)
        .options(joinedload(UserPrivacyPolicy.user))
        .filter(UserPrivacyPolicy.privacy_policy_id == privacy_policy_id)
        .all()
    )


def soft_delete_by_user(db: Session, user_id: int):
    db.query(UserPrivacyPolicy).filter(UserPrivacyPolicy.user_id == user_id).update(
        {"deleted": True}
    )
