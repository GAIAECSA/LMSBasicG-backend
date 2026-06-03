# services/mdt_certificate_service.py

import os
import re

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.helpers import blind_index
from app.models.mdt_certificate import MdtCertificate
from app.repositories import mdt_certificate_repo
from app.schemas.mdt_certificate import (MdtBulkCertificateCreate,
                                         MdtCertificateCreate,
                                         MdtCertificateUpdate)
from app.utils.file_upload import save_certificate_mdt

ID_NUMBER_REGEX = r"\d{10}"


def create_certificate(
    db: Session,
    data: MdtCertificateCreate,
    file: UploadFile,
):
    if not file:
        raise Exception("El archivo es requerido")

    certificate_data = data.model_dump()

    id_number_hash = blind_index.generate_blind_index(certificate_data["id_number"])

    certificate_data["id_number_hash"] = id_number_hash

    with db.begin():

        existing_certificate = mdt_certificate_repo.get_by_id_number_hash_and_course(
            db,
            id_number_hash,
            certificate_data["course_id"],
            certificate_data["certificate_type"],
        )

        saved_file = save_certificate_mdt(file)

        if existing_certificate:

            if existing_certificate.file_url:
                try:
                    file_path = existing_certificate.file_url.lstrip("/")

                    if os.path.exists(file_path):
                        os.remove(file_path)

                except Exception:
                    pass

            certificate_data.update(
                {
                    "file_url": saved_file["file_url"],
                    "file_name": saved_file["filename"],
                }
            )

            return mdt_certificate_repo.update(
                db=db,
                certificate=existing_certificate,
                data=certificate_data,
            )

        certificate_data.update(
            {
                "file_url": saved_file["file_url"],
                "file_name": saved_file["filename"],
            }
        )

        certificate = MdtCertificate(
            **certificate_data,
        )

        return mdt_certificate_repo.create(
            db=db,
            certificate=certificate,
        )


def create_certificates_bulk(
    db: Session,
    data: MdtBulkCertificateCreate,
    files: list[UploadFile],
):
    if not files:
        raise Exception("Debe enviar archivos")

    created = []
    errors = []

    base_data = data.model_dump()

    with db.begin():

        for index, file in enumerate(files):

            try:

                with db.begin_nested():

                    match = re.search(
                        ID_NUMBER_REGEX,
                        file.filename,
                    )

                    if not match:
                        raise Exception(
                            "No se encontró una cédula válida en el nombre del archivo"
                        )

                    id_number = match.group()

                    id_number_hash = blind_index.generate_blind_index(
                        id_number
                    )

                    existing_certificate = (
                        mdt_certificate_repo.get_by_id_number_hash_and_course(
                            db,
                            id_number_hash,
                            base_data["course_id"],
                            base_data["certificate_type"],
                        )
                    )

                    saved_file = save_certificate_mdt(file)

                    if existing_certificate:

                        if existing_certificate.file_url:
                            try:
                                file_path = existing_certificate.file_url.lstrip("/")

                                if os.path.exists(file_path):
                                    os.remove(file_path)

                            except Exception:
                                pass

                        existing_certificate.id_number = id_number
                        existing_certificate.id_number_hash = id_number_hash
                        existing_certificate.file_url = saved_file["file_url"]
                        existing_certificate.file_name = saved_file["filename"]

                        certificate = mdt_certificate_repo.update(
                            db=db,
                            certificate=existing_certificate,
                        )

                    else:

                        certificate = MdtCertificate(
                            **base_data,
                            id_number=id_number,
                            id_number_hash=id_number_hash,
                            file_url=saved_file["file_url"],
                            file_name=saved_file["filename"],
                        )

                        certificate = mdt_certificate_repo.create(
                            db=db,
                            certificate=certificate,
                        )

                    created.append(
                        {
                            "id": certificate.id,
                            "file": file.filename,
                            "id_number": id_number,
                        }
                    )

            except Exception as e:

                errors.append(
                    {
                        "file": file.filename,
                        "index": index,
                        "error": str(e),
                    }
                )

    return {
        "success_count": len(created),
        "error_count": len(errors),
        "certificates": created,
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
    id_number_hash = blind_index.generate_blind_index(id_number)
    return mdt_certificate_repo.get_by_id_number_hash(
        db,
        id_number_hash,
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


def get_certificate_by_id_number_and_course(
    db: Session, id_number: str, course_id: int, certificate_type: str
):

    id_number_hash = blind_index.generate_blind_index(id_number)
    certificate = mdt_certificate_repo.get_by_id_number_hash_and_course(
        db=db,
        id_number_hash=id_number_hash,
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
