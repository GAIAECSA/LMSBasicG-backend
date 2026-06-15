from sqlalchemy.orm import Session

from app.models.certificate_template import CertificateTemplate

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(
    db: Session, certificate_template: CertificateTemplate
) -> CertificateTemplate:
    db.add(certificate_template)
    db.flush()
    return certificate_template


# --- Eliminaciones (Updates/Deletes masivos) ---
def delete_soft_by_course(db: Session, course_id: int, business_id: int) -> None:
    db.query(CertificateTemplate).filter(
        CertificateTemplate.course_id == course_id,
        CertificateTemplate.business_id == business_id,
    ).update({"deleted": True}, synchronize_session=False)


# --- Consultas (Lectura) ---


def get_by_id(db: Session, certificate_template_id: int, business_id: int):
    return (
        db.query(CertificateTemplate)
        .filter(
            CertificateTemplate.id == certificate_template_id,
            CertificateTemplate.business_id == business_id,
            CertificateTemplate.deleted == False,
        )
        .first()
    )


def get_all(db: Session, business_id: int):
    return (
        db.query(CertificateTemplate)
        .filter(
            CertificateTemplate.business_id == business_id,
            CertificateTemplate.deleted == False,
        )
        .all()
    )


def get_by_course(db: Session, course_id: int, business_id: int):
    return (
        db.query(CertificateTemplate)
        .filter(
            CertificateTemplate.course_id == course_id,
            CertificateTemplate.business_id == business_id,
            CertificateTemplate.deleted == False,
        )
        .first()
    )


# Viejos
# def create(db: Session, certificate_template: CertificateTemplate):
#   db.add(certificate_template)
#  db.commit()
# db.refresh(certificate_template)
# return certificate_template


# def update(db: Session, certificate_template: CertificateTemplate):
#   db.merge(certificate_template)
#  db.commit()
# db.refresh(certificate_template)
# return certificate_template


# def delete(db: Session, certificate_template: CertificateTemplate):
#   certificate_template.deleted = True
#  db.merge(certificate_template)
# db.commit()
# return certificate_template


# def get_by_id(db: Session, certificate_template_id: int):
# return (
# db.query(CertificateTemplate)
#  .filter(
#       CertificateTemplate.id == certificate_template_id,
#        CertificateTemplate.deleted == False,
#     )
#      .first()
#   )


# def get_all(db: Session):
# return (
#   db.query(CertificateTemplate).filter(CertificateTemplate.deleted == False).all()
# )


# def get_by_course(db: Session, course_id: int):
#   return (
#      db.query(CertificateTemplate)
#     .filter(
#        CertificateTemplate.course_id == course_id,
#       CertificateTemplate.deleted == False,
#  )
# .first()
# )
