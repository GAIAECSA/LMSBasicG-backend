# repositories/mdt_certificate_repo.py

from sqlalchemy.orm import Session

from app.models.mdt_certificate import MdtCertificate

from app.schemas.mdt_certificate import (
    MdtCertificateCreate,
    MdtCertificateUpdate,
)


def create(
    db: Session,
    data: MdtCertificateCreate,
    file_url: str,
    file_name: str,
):
    certificate = MdtCertificate(
        course_id=data.course_id,
        file_url=file_url,
        file_name=file_name,
        id_number=data.id_number,
        certificate_type=data.certificate_type,
    )

    db.add(certificate)

    db.flush()
    db.refresh(certificate)

    return certificate


def get_by_id(
    db: Session,
    certificate_id: int,
):
    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.id == certificate_id,
            MdtCertificate.deleted == False,
        )
        .first()
    )


def get_by_course_id(
    db: Session,
    course_id: int,
):
    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.course_id == course_id,
            MdtCertificate.deleted == False,
        )
        .order_by(MdtCertificate.created_at.desc())
        .all()
    )


def get_by_id_number(
    db: Session,
    id_number: str,
):
    return (
        db.query(MdtCertificate)
        .filter(
            MdtCertificate.id_number == id_number,
            MdtCertificate.deleted == False,
        )
        .order_by(MdtCertificate.created_at.desc())
        .all()
    )

def update(
    db: Session,
    certificate: MdtCertificate,
    data: MdtCertificateUpdate,
):
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(certificate, key, value)

    db.flush()
    db.refresh(certificate)

    return certificate


def soft_delete(
    db: Session,
    certificate: MdtCertificate,
):
    certificate.deleted = True

    db.flush()
