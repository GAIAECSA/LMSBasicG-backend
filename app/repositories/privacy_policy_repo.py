from sqlalchemy.orm import Session

from app.models.privacy_policy import PrivacyPolicy

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================


# --- Crear ---
def create(
    db: Session,
    privacy_policy: PrivacyPolicy,
):
    db.add(privacy_policy)
    db.flush()
    return privacy_policy


# --- Eliminaciones (Updates/Deletes masivos) ---


def deactivate(db: Session, business_id: int):
    db.query(PrivacyPolicy).filter(
        PrivacyPolicy.is_active == True,
        PrivacyPolicy.business_id == business_id,
        PrivacyPolicy.deleted == False,
    ).update({"is_active": False}, synchronize_session=False)


# --- Consultas (Lectura) ---


def get_by_id(db: Session, privacy_policy_id: int, business_id: int):
    return (
        db.query(PrivacyPolicy)
        .filter(
            PrivacyPolicy.id == privacy_policy_id,
            PrivacyPolicy.business_id == business_id,
            PrivacyPolicy.deleted == False,
        )
        .first()
    )


def get_all(db: Session, business_id: int):
    return (
        db.query(PrivacyPolicy)
        .filter(
            PrivacyPolicy.business_id == business_id, PrivacyPolicy.deleted == False
        )
        .all()
    )


def get_active(db: Session, business_id: int):
    return (
        db.query(PrivacyPolicy)
        .filter(
            PrivacyPolicy.is_active == True,
            PrivacyPolicy.business_id == business_id,
            PrivacyPolicy.deleted == False,
        )
        .order_by(PrivacyPolicy.effective_date.desc())
        .first()
    )


def get_by_version(db: Session, version: str, business_id: int) -> PrivacyPolicy | None:

    return (
        db.query(PrivacyPolicy)
        .filter(
            PrivacyPolicy.version == version,
            PrivacyPolicy.business_id == business_id,
            PrivacyPolicy.deleted == False,
        )
        .first()
    )


# Viejos
# def get_all(db: Session):
#   return db.query(PrivacyPolicy).filter(PrivacyPolicy.deleted == False).all()


# def get_by_id(db: Session, privacy_policy_id: int):
#   return (
#      db.query(PrivacyPolicy)
#     .filter(PrivacyPolicy.id == privacy_policy_id, PrivacyPolicy.deleted == False)
#    .first()
# )


# def get_active(db: Session):
#   return (
#      db.query(PrivacyPolicy)
#     .filter(PrivacyPolicy.is_active == True, PrivacyPolicy.deleted == False)
#    .order_by(PrivacyPolicy.effective_date.desc())
#   .first()
# )


# def delete(db: Session, privacy_policy: PrivacyPolicy):

#   privacy_policy.deleted = True

#  db.commit()

# db.refresh(privacy_policy)

# return privacy_policy


# def get_by_version(db: Session, version: str) -> PrivacyPolicy | None:

#   return (
#      db.query(PrivacyPolicy)
#     .filter(PrivacyPolicy.version == version, PrivacyPolicy.deleted == False)
#    .first()
# )


# def find_active(db: Session):

#   return (
#      db.query(PrivacyPolicy)
#     .filter(PrivacyPolicy.is_active == True, PrivacyPolicy.deleted == False)
#    .order_by(PrivacyPolicy.effective_date.desc())
#   .all()
# )


# def create(
#   db: Session,
#  privacy_policy: PrivacyPolicy,
# ):

#   db.add(privacy_policy)
#
#   db.flush()
#  db.refresh(privacy_policy)

# return privacy_policy


# def update(
#   db: Session,
#  privacy_policy: PrivacyPolicy,
# ):

#   db.flush()
#  db.refresh(privacy_policy)

# return privacy_policy
