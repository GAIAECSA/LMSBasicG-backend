# repositories/mdt_certificate_repo.py

from sqlalchemy.orm import Session

from app.models.mdt_certificate import MdtCertificate

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(
    db: Session,
    certificate: MdtCertificate,
) -> MdtCertificate:

    db.add(certificate)
    db.flush()

    return certificate


def create_bulk(db: Session, certificate: list[MdtCertificate]):
    db.add_all(certificate)
    db.flush()
    return certificate


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(db: Session, certificate_id: int, business_id: int):
    db.query(MdtCertificate).filter(
        MdtCertificate.id == certificate_id, MdtCertificate.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_course(db: Session, course_id: int, business_id: int):
    db.query(MdtCertificate).filter(
        MdtCertificate.course_id == course_id, MdtCertificate.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


# --- Consultas (Lectura) ---


def get_by_id(
    db: Session,
    certificate_id: int,
    business_id: int,
) -> MdtCertificate | None:
    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.id == certificate_id,
            MdtCertificate.business_id == business_id,
            MdtCertificate.deleted.is_(False),
        )
        .first()
    )


def get_by_course_id(
    db: Session,
    course_id: int,
    business_id: int,
) -> list[MdtCertificate]:
    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.course_id == course_id,
            MdtCertificate.business_id == business_id,
            MdtCertificate.deleted.is_(False),
        )
        .order_by(MdtCertificate.created_at.desc())
        .all()
    )


def get_by_id_number_hash(
    db: Session,
    id_number_hash: str,
    business_id: int,
) -> list[MdtCertificate]:
    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.id_number_hash == id_number_hash,
            MdtCertificate.business_id == business_id,
            MdtCertificate.deleted.is_(False),
        )
        .order_by(MdtCertificate.created_at.desc())
        .all()
    )


def get_by_id_number_hash_and_course(
    db: Session,
    id_number_hash: str,
    course_id: int,
    certificate_type: str,
    business_id: int,
) -> MdtCertificate | None:
    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.id_number_hash == id_number_hash,
            MdtCertificate.course_id == course_id,
            MdtCertificate.certificate_type == certificate_type,
            MdtCertificate.business_id == business_id,
            MdtCertificate.deleted.is_(False),
        )
        .first()
    )


# Viejo
"""def create(
    db: Session,
    certificate: MdtCertificate,
) -> MdtCertificate:

    db.add(certificate)
    db.flush()
    db.refresh(certificate)

    return certificate


def create_bulk(
    db: Session,
    certificates: list[MdtCertificate],
) -> list[MdtCertificate]:

    db.add_all(certificates)
    db.flush()

    for certificate in certificates:
        db.refresh(certificate)

    return certificates


def get_by_id(
    db: Session,
    certificate_id: int,
) -> MdtCertificate | None:

    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.id == certificate_id,
            MdtCertificate.deleted.is_(False),
        )
        .first()
    )


def get_by_course_id(
    db: Session,
    course_id: int,
) -> list[MdtCertificate]:

    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.course_id == course_id,
            MdtCertificate.deleted.is_(False),
        )
        .order_by(MdtCertificate.created_at.desc())
        .all()
    )


def get_by_id_number_hash(
    db: Session,
    id_number_hash: str,
) -> list[MdtCertificate]:

    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.id_number_hash == id_number_hash,
            MdtCertificate.deleted.is_(False),
        )
        .order_by(MdtCertificate.created_at.desc())
        .all()
    )


def update(
    db: Session,
    certificate: MdtCertificate,
) -> MdtCertificate:

    db.flush()
    db.refresh(certificate)

    return certificate


def soft_delete(
    db: Session,
    certificate: MdtCertificate,
) -> MdtCertificate:

    certificate.deleted = True

    db.flush()
    db.refresh(certificate)

    return certificate


def get_by_id_number_hash_and_course(
    db: Session,
    id_number_hash: str,
    course_id: int,
    certificate_type: str,
) -> MdtCertificate | None:
    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.id_number_hash == id_number_hash,
            MdtCertificate.course_id == course_id,
            MdtCertificate.certificate_type == certificate_type,
            MdtCertificate.deleted.is_(False),
        )
        .first()
    )
"""
