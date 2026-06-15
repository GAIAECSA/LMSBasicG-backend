from sqlalchemy.orm import Session, joinedload

from app.models.user_privacy_policy import UserPrivacyPolicy

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, user_privacy_policy: UserPrivacyPolicy):
    db.add(user_privacy_policy)
    db.flush()
    return user_privacy_policy


# --- Eliminaciones (Updates/Deletes masivos) ---


# --- Consultas (Lectura) ---


def get_user_acceptance(
    db: Session, user_id: int, privacy_policy_id: int, business_id: int
):
    return (
        db.query(UserPrivacyPolicy)
        .filter(
            UserPrivacyPolicy.user_id == user_id,
            UserPrivacyPolicy.privacy_policy_id == privacy_policy_id,
            UserPrivacyPolicy.business_id == business_id,
        )
        .first()
    )


def get_by_privacy_policy_id(db: Session, privacy_policy_id: int, business_id: int):
    return (
        db.query(UserPrivacyPolicy)
        .options(joinedload(UserPrivacyPolicy.user))
        .filter(
            UserPrivacyPolicy.privacy_policy_id == privacy_policy_id,
            UserPrivacyPolicy.business_id == business_id,
        )
        .all()
    )


# Viejos
# def create(db: Session, user_id: int, privacy_policy_id: int):
#   acceptance = UserPrivacyPolicy(
#      user_id=user_id, privacy_policy_id=privacy_policy_id, accepted=True
# )

# db.add(acceptance)
# db.commit()
# db.refresh(acceptance)

# return acceptance


# def get_user_acceptance(db: Session, user_id: int, privacy_policy_id: int):
#   return (
#      db.query(UserPrivacyPolicy)
#     .filter(
#        UserPrivacyPolicy.user_id == user_id,
#       UserPrivacyPolicy.privacy_policy_id == privacy_policy_id,
#  )
# .first()
# )


# def get_by_privacy_policy_id(db: Session, privacy_policy_id: int):
#   return (
#      db.query(UserPrivacyPolicy)
#     .options(joinedload(UserPrivacyPolicy.user))
#    .filter(UserPrivacyPolicy.privacy_policy_id == privacy_policy_id)
#   .all()
# )
