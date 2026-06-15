from sqlalchemy.orm import Session

from app.models.certificate import Certificate

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================


# --- Crear ---
def create(db: Session, certificate_template: Certificate) -> Certificate:
    db.add(certificate_template)
    db.flush()
    return certificate_template


# --- Eliminaciones (Updates/Deletes masivos) ---
def delete_soft_by_course(db: Session, course_id: int, business_id: int):
    db.query(Certificate).filter(
        Certificate.course_id == course_id, Certificate.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_user(db: Session, user_id: int, business_id: int):
    db.query(Certificate).filter(
        Certificate.user_id == user_id, Certificate.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


# --- Consultas (Lectura) ---


def get_by_id(db: Session, certificate_id: int, business_id: int):
    return (
        db.query(Certificate)
        .filter(
            Certificate.id == certificate_id,
            Certificate.business_id == business_id,
            Certificate.deleted == False,
        )
        .first()
    )


def get_by_code(db: Session, code: str, business_id: int):
    return (
        db.query(Certificate)
        .filter(
            Certificate.certificate_code == code,
            Certificate.business_id == business_id,
            Certificate.deleted == False,
        )
        .first()
    )


def get_by_user_and_course(db: Session, user_id: int, course_id: int, business_id: int):
    return (
        db.query(Certificate)
        .filter(
            Certificate.user_id == user_id,
            Certificate.course_id == course_id,
            Certificate.business_id == business_id,
            Certificate.deleted == False,
        )
        .first()
    )


def get_all(db: Session, business_id: int):
    return (
        db.query(Certificate)
        .filter(Certificate.business_id == business_id, Certificate.deleted == False)
        .order_by(Certificate.created_at.desc())
        .all()
    )


def get_all_by_user(db: Session, user_id: int, business_id: int):
    return (
        db.query(Certificate)
        .filter(
            Certificate.user_id == user_id,
            Certificate.business_id == business_id,
            Certificate.deleted == False,
        )
        .order_by(Certificate.created_at.desc())
        .all()
    )


def get_all_by_course(db: Session, course_id: int, business_id: int):
    return (
        db.query(Certificate)
        .filter(
            Certificate.course_id == course_id,
            Certificate.business_id == business_id,
            Certificate.deleted == False,
        )
        .order_by(Certificate.created_at.desc())
        .all()
    )


# Viejo


# def delete(db: Session, certificate: Certificate):
#   certificate.deleted = True
#  db.merge(certificate)
# db.commit()
# return certificate


# def soft_delete_by_user(db: Session, user_id: int):
#   db.query(Certificate).filter(Certificate.user_id == user_id).update(
#      {"deleted": True}
# )


# def get_by_id(db: Session, certificate_id: int):
#   return (
#      db.query(Certificate)
#     .filter(Certificate.id == certificate_id, Certificate.deleted == False)
#    .first()
# )


# def get_by_code(db: Session, code: str):
#   return (
#      db.query(Certificate)
#     .filter(Certificate.certificate_code == code, Certificate.deleted == False)
#    .first()
# )


# def get_by_user_and_course(db: Session, user_id: int, course_id: int):
#   return (
#      db.query(Certificate)
#     .filter(
#        Certificate.user_id == user_id,
#       Certificate.course_id == course_id,
#      Certificate.deleted == False,
# )
# .first()
# )


# def get_all(db: Session):
#   return (
#      db.query(Certificate)
#     .filter(Certificate.deleted == False)
#    .order_by(Certificate.created_at.desc())
#   .all()
# )


# def get_all_by_user(db: Session, user_id: int):
#   return (
#      db.query(Certificate)
#     .filter(Certificate.user_id == user_id, Certificate.deleted == False)
#    .order_by(Certificate.created_at.desc())
#   .all()
# )


# def get_all_by_course(db: Session, course_id: int):
#   return (
#      db.query(Certificate)
#     .filter(Certificate.course_id == course_id, Certificate.deleted == False)
#    .order_by(Certificate.created_at.desc())
#   .all()
# )


# Metodos compuestos


# def create(db: Session, certificate: Certificate):
#   db.add(certificate)
#  db.flush()
# return certificate


# def update(db: Session, certificate: Certificate):
#   db.add(certificate)
#  db.flush()
# db.refresh(certificate)
# return certificate
