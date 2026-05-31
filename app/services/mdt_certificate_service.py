# services/mdt_certificate_service.py

import re

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.mdt_certificate import MdtCertificate
from app.repositories import mdt_certificate_repo
from app.schemas.mdt_certificate import (
    MdtBulkCertificateCreate,
    MdtCertificateCreate,
    MdtCertificateUpdate,
)
from app.utils.file_upload import save_certificate_mdt

ID_NUMBER_REGEX = r"\d{10}"


def create_certificate(
    db: Session,
    data: MdtCertificateCreate,
    file: UploadFile,
):

    if not file:
        raise Exception("El archivo es requerido")

    saved_file = save_certificate_mdt(file)

    certificate_data = data.model_dump()

    certificate_data.update(
        {
            "file_url": saved_file["file_url"],
            "file_name": saved_file["filename"],
        }
    )

    certificate = MdtCertificate(**certificate_data)

    certificate = mdt_certificate_repo.create(
        db=db,
        certificate=certificate,
    )

    db.commit()

    return certificate


def create_certificates_bulk(
    db: Session,
    data: MdtBulkCertificateCreate,
    files: list[UploadFile],
):

    if not files:
        raise Exception("Debe enviar archivos")

    certificates = []
    errors = []

    base_data = data.model_dump()

    for index, file in enumerate(files):

        try:

            match = re.search(
                ID_NUMBER_REGEX,
                file.filename,
            )

            if not match:
                raise Exception(
                    "No se encontró una cédula válida en el nombre del archivo"
                )

            id_number = match.group()

            saved_file = save_certificate_mdt(file)

            certificate_data = {
                **base_data,
                "id_number": id_number,
                "file_url": saved_file["file_url"],
                "file_name": saved_file["filename"],
            }

            certificate = MdtCertificate(**certificate_data)

            certificates.append(certificate)

        except Exception as e:

            errors.append(
                {
                    "file": file.filename,
                    "index": index,
                    "error": str(e),
                }
            )

    if certificates:

        mdt_certificate_repo.create_bulk(
            db=db,
            certificates=certificates,
        )

        db.commit()

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

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(certificate, key, value)

    certificate = mdt_certificate_repo.update(
        db,
        certificate,
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


def get_certificate_by_id_and_course(
    db: Session, id_number: str, course_id: int, certificate_type: str
):
    # 1. Buscar el certificado único usando los tres criterios
    certificate = mdt_certificate_repo.get_by_id_and_course(
        db=db,
        id_number=id_number,
        course_id=course_id,
        certificate_type=certificate_type,  # <-- Nuevo argumento
    )

    # 2. Validar existencia
    if not certificate:
        raise ValueError(
            "No se encontró ningún certificado que coincida con el documento, curso y tipo especificados."
        )

    # 3. Marcar como visitado e impactar la base de datos
    certificate.mark_as_visited()
    db.commit()
    db.refresh(certificate)

    return certificate
