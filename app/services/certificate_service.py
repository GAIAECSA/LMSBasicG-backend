from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.certificate import Certificate
from app.repositories import certificate_repo
from app.schemas.certificate import CertificateCreate, CertificateUpdate
from app.utils.file_upload import save_certificate
import uuid
import os

def create_certificate(db: Session, data: CertificateCreate, file: UploadFile | None):

    existing = certificate_repo.get_by_user_and_course(db,data.user_id,data.course_id)
    if existing:
        raise Exception("El registro ya existe")

    certificate_code = f"CERT-{uuid.uuid4().hex[:10].upper()}"

    file_url = None
    if file:
        file_url = save_certificate(file)

    certificate = Certificate(
        **data.model_dump(exclude={"certificate_code", "file_url"}),
        certificate_code=certificate_code,
        file_url=file_url
    )

    return certificate_repo.create(db, certificate)

def update_certificate(db: Session, certificate_id: int, data: CertificateUpdate, file: UploadFile | None):
    
    certificate = certificate_repo.get_by_id(db, certificate_id)
    if not certificate:
        raise Exception("Certificado no encontrado")

    update_data = data.model_dump(exclude_unset=True)

    old_file_path = None

    if file:
        if certificate.file_url:
            old_file_path = certificate.file_url.lstrip("/")

        new_file_url = save_certificate(file)
        update_data["file_url"] = new_file_url

    for key, value in update_data.items():
        setattr(certificate, key, value)

    updated = certificate_repo.update(db, certificate)

    if file and old_file_path and os.path.exists(old_file_path):
        try:
            os.remove(old_file_path)
        except Exception:
            pass

    return updated

def delete_certificate(db: Session, certificate_id: int):
    certificate = certificate_repo.get_by_id(db, certificate_id)
    if not certificate:
        raise Exception("Certificado no encontrado")

    certificate.deleted = True
    return certificate_repo.update(db, certificate)


def get_certificate(db: Session, certificate_id: int):
    certificate = certificate_repo.get_by_id(db, certificate_id)
    if not certificate or certificate.deleted:
        raise Exception("Certificado no encontrado")
    return certificate

def get_certificate_by_code(db: Session, code: str):
    certificate = certificate_repo.get_by_code(db, code)
    if not certificate or certificate.deleted:
        raise Exception("Certificado no encontrado")
    return certificate

def get_all_certificates(db: Session):
    return certificate_repo.get_all(db)

def verify_certificate(db: Session, code: str):
    certificate = certificate_repo.get_by_code(db, code)

    if not certificate or certificate.deleted:
        raise Exception("Certificado no válido")

    if not certificate.is_valid:
        raise Exception("Certificado inválido")

    return certificate
