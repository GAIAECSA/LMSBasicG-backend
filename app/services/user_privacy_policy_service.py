from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user_privacy_policy import UserPrivacyPolicy
from app.repositories import privacy_policy_repo, user_privacy_policy_repo

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class UserPrivacyAcceptedAlreadyExist(Exception):
    pass


class UserPrivacyAcceptedNotFound(Exception):
    pass


class PrivacyPolicyNotFound(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def accept_privacy_policy(
    db: Session, user_id: int, privacy_policy_id: int, business_id: int
):
    with db.begin():
        existing = user_privacy_policy_repo.get_user_acceptance(
            db, user_id, privacy_policy_id, business_id
        )

        if existing:
            raise UserPrivacyAcceptedAlreadyExist("Ya existe un registro favorable")

        privacy_policy = privacy_policy_repo.get_by_id(
            db, privacy_policy_id, business_id
        )

        if not privacy_policy:
            raise PrivacyPolicyNotFound("No existe la politica")

        new_acceptance = UserPrivacyPolicy(
            user_id=user_id,
            privacy_policy_id=privacy_policy_id,
            business_id=business_id,
        )

        return user_privacy_policy_repo.create(db, new_acceptance)


def check_active_privacy_policy_acceptance(db: Session, user_id: int, business_id: int):

    privacy_policy = privacy_policy_repo.get_active(db, business_id)

    if not privacy_policy:
        raise PrivacyPolicyNotFound("No existe la politica")

    acceptance = user_privacy_policy_repo.get_user_acceptance(
        db, user_id, privacy_policy.id, business_id
    )

    return {
        "accepted": acceptance is not None,
        "privacy_policy_id": privacy_policy.id,
        "version": privacy_policy.version,
    }


def get_accepted_privacy_policies(
    db: Session, privacy_policy_id: int, business_id: int
):

    users_privacy_policy = user_privacy_policy_repo.get_by_privacy_policy_id(
        db, privacy_policy_id, business_id
    )

    if not users_privacy_policy:
        raise UserPrivacyAcceptedNotFound("No existen politicas aceptadas")

    return [
        {
            "id": item.id,
            "user_id": item.user_id,
            "fullname": (f"{item.user.firstname} " f"{item.user.lastname}"),
            "accepted": item.accepted,
            "accepted_at": item.accepted_at,
        }
        for item in users_privacy_policy
    ]


"""
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


def get_accepted_privacy_policies(
    db: Session,
    privacy_policy_id: int,
):

    users_privacy_policy = user_privacy_policy_repo.get_by_privacy_policy_id(
        db,
        privacy_policy_id,
    )

    if not users_privacy_policy:
        raise HTTPException(
            status_code=404,
            detail="Privacy policy not found",
        )

    return [
        {
            "id": item.id,
            "user_id": item.user_id,
            "fullname": (f"{item.user.firstname} " f"{item.user.lastname}"),
            "accepted": item.accepted,
            "accepted_at": item.accepted_at,
        }
        for item in users_privacy_policy
    ]
"""
