from sqlalchemy.orm import Session

from app.models.privacy_policy import PrivacyPolicy


def create(db: Session, privacy_policy: PrivacyPolicy):

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


def get_active(db: Session):
    return (
        db.query(PrivacyPolicy)
        .filter(PrivacyPolicy.is_active == True, PrivacyPolicy.deleted == False)
        .order_by(PrivacyPolicy.effective_date.desc())
        .first()
    )


def update(db: Session, privacy_policy: PrivacyPolicy):

    db.commit()

    db.refresh(privacy_policy)

    return privacy_policy


def delete(db: Session, privacy_policy: PrivacyPolicy):

    privacy_policy.deleted = True

    db.commit()

    db.refresh(privacy_policy)

    return privacy_policy


def get_by_version(db: Session, version: str) -> PrivacyPolicy | None:

    return (
        db.query(PrivacyPolicy)
        .filter(PrivacyPolicy.version == version, PrivacyPolicy.deleted == False)
        .first()
    )
