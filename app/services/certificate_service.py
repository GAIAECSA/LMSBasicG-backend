from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.certificate import Certificate
from app.repositories import certificate_repo
from app.schemas.certificate import CertificateCreate, CertificateUpdate
from app.utils.file_upload import save_certificate
from app.repositories.enrollment_repo import get_existing_enrollment
from app.services.quizz_response_service import get_by_enrollment
import uuid
import os
import logging

logger = logging.getLogger(__name__)

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

def update_certificate(
    db: Session,
    certificate_id: int,
    data: CertificateUpdate,
    file: UploadFile | None
):

    certificate = certificate_repo.get_by_id(db, certificate_id)

    if not certificate:
        raise Exception("Certificado no encontrado")

    update_data = data.model_dump(exclude_unset=True)

    logger.info(f"Update data recibido: {update_data}")

    # Calcular promedio si no viene final_grade
    # o viene como None
    if update_data.get("final_grade") is None:

        avg = calculate_final_grade_average(
            db,
            certificate.user_id,
            certificate.course_id
        )

        logger.info(f"Promedio calculado: {avg}")

        if avg is not None:
            update_data["final_grade"] = avg

    old_file_path = None

    if file:

        if certificate.file_url:
            old_file_path = certificate.file_url.lstrip("/")

        new_file_url = save_certificate(file)

        update_data["file_url"] = new_file_url

    # Aplicar cambios al modelo
    for key, value in update_data.items():
        setattr(certificate, key, value)

    logger.info(
        f"Datos finales a guardar: "
        f"is_valid={certificate.is_valid}, "
        f"final_grade={certificate.final_grade}, "
        f"file_url={certificate.file_url}"
    )

    updated = certificate_repo.update(db, certificate)

    # Eliminar archivo anterior si hubo reemplazo
    if file and old_file_path and os.path.exists(old_file_path):

        try:
            os.remove(old_file_path)

        except Exception as e:
            logger.warning(f"No se pudo eliminar archivo viejo: {e}")

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

def get_certificates_by_user(db: Session, user_id: int):
    certificates = certificate_repo.get_all_by_user(db, user_id)
    return certificates

def get_all_certificates(db: Session):
    return certificate_repo.get_all(db)

def verify_certificate(db: Session, code: str):
    certificate = certificate_repo.get_by_code(db, code)

    if not certificate or certificate.deleted:
        raise Exception("Certificado no válido")

    if not certificate.is_valid:
        raise Exception("Certificado inválido")

    return certificate

def calculate_final_grade_average(
    db: Session,
    user_id: int,
    course_id: int
) -> float | None:

    logger.info(
        f"[AVG] Iniciando cálculo "
        f"user_id={user_id}, course_id={course_id}"
    )

    enrollment = get_existing_enrollment(
        db,
        user_id,
        course_id
    )

    logger.info(f"[AVG] Enrollment encontrado: {enrollment}")

    if not enrollment:
        logger.warning("[AVG] No existe enrollment")
        return None

    result = get_by_enrollment(db, enrollment.id)

    logger.info(f"[AVG] Result encontrado: {result}")

    if not result:
        logger.warning("[AVG] No existe result")
        return None

    logger.info(f"[AVG] Scores raw: {result.score}")

    if not result.score:
        logger.warning("[AVG] Result no tiene scores")
        return None

    grades = [
        r.grade
        for r in result.score
        if r.grade is not None
    ]

    logger.info(f"[AVG] Grades filtrados: {grades}")

    if not grades:
        logger.warning("[AVG] No hay notas válidas")
        return None

    avg = sum(grades) / len(grades)

    logger.info(f"[AVG] Promedio final calculado: {avg}")

    return avg