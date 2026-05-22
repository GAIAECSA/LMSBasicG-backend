# services/mdt_certificate_service.py

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories import mdt_certificate_repo

from app.schemas.mdt_certificate import (
    MdtCertificateCreate,
    MdtCertificateUpdate,
)

from app.utils.file_upload import save_certificate_mdt


def create_certificate(
    db: Session,
    data: MdtCertificateCreate,
    file: UploadFile,
):
    if not file:
        raise Exception("El archivo es requerido")

    file_url = save_certificate_mdt(file)

    certificate = mdt_certificate_repo.create(
        db=db,
        data=data,
        file_url=file_url,
        file_name=file.filename,
    )

    db.commit()

    return certificate


def create_certificates_bulk(
    db: Session,
    data: MdtCertificateCreate,
    files: list[UploadFile],
):
    if not files:
        raise Exception("Debe enviar archivos")

    certificates = []
    errors = []

    for index, file in enumerate(files):

        try:

            file_url = save_certificate_mdt(file)

            certificate = mdt_certificate_repo.create(
                db=db,
                data=data,
                file_url=file_url,
                file_name=file.filename,
            )

            db.commit()

            db.refresh(certificate)

            certificates.append(certificate)

        except Exception as e:

            db.rollback()

            errors.append(
                {
                    "file": file.filename,
                    "index": index,
                    "error": str(e),
                }
            )

    return {
        "success_count": len(certificates),
        "error_count": len(errors),
        "certificates": certificates,
        "errors": errors,
    }


def get_certificate_by_id(
    db: Session,
    certificate_id: int,
):
    certificate = mdt_certificate_repo.get_by_id(
        db,
        certificate_id,
    )

    if not certificate:
        raise Exception("Certificado no encontrado")

    return certificate


def get_certificates_by_course_id(
    db: Session,
    course_id: int,
):
    return mdt_certificate_repo.get_by_course_id(
        db,
        course_id,
    )


def get_certificates_by_id_number(
    db: Session,
    id_number: str,
):
    return mdt_certificate_repo.get_by_id_number(
        db,
        id_number,
    )


def update_certificate(
    db: Session,
    certificate_id: int,
    data: MdtCertificateUpdate,
):
    certificate = get_certificate_by_id(
        db,
        certificate_id,
    )

    certificate = mdt_certificate_repo.update(
        db,
        certificate,
        data,
    )

    db.commit()

    return certificate


def delete_certificate(
    db: Session,
    certificate_id: int,
):
    certificate = get_certificate_by_id(
        db,
        certificate_id,
    )

    mdt_certificate_repo.soft_delete(
        db,
        certificate,
    )

    db.commit()
