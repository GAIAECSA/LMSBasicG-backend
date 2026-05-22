from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.models.certificate import Certificate
from app.models.enrollment import Enrollment
from app.repositories import (
    attendance_repo,
    course_attendance_repo,
    enrollment_repo,
    certificate_repo,
)
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate
from fastapi import UploadFile
from app.utils.file_upload import save_course_voucher
from app.services.certificate_service import create_certificate
from app.schemas.certificate import CertificateCreate
import os
import uuid


def create_enrollment(
    db: Session, data: EnrollmentCreate, image: UploadFile | None = None
):

    with db.begin():

        existing = enrollment_repo.get_existing_enrollment(
            db, data.course_id, data.user_id
        )

        if existing:
            if existing.accepted is None:
                raise Exception("Matrícula en revisión")
            elif existing.accepted is True:
                raise Exception("Ya estás matriculado en este curso")
            elif existing.accepted is False:
                raise Exception("Tu solicitud de matrícula no fue aprobada.")

        voucher_url = save_course_voucher(image) if image else None

        enrollment = Enrollment(**data.model_dump(), voucher_url=voucher_url)
        enrollment = enrollment_repo.create_flush(db, enrollment)

        role = enrollment.role
        code = f"CERT-{uuid.uuid4().hex[:10].upper()}"

        if role.id == 4:
            certificate_repo.create(
                db,
                Certificate(
                    user_id=data.user_id,
                    course_id=data.course_id,
                    certificate_code=code,
                ),
            )

        course_attendances = course_attendance_repo.get_by_course(db, data.course_id)

        if course_attendances:
            attendances = [
                Attendance(
                    enrollment_id=enrollment.id,
                    course_attendance_id=ca.id,
                    attendance_state="PENDIENTE",
                )
                for ca in course_attendances
            ]

            attendance_repo.create_many(db, attendances)

        return enrollment


def update_enrollment(
    db: Session,
    enrollment_id: int,
    data: EnrollmentUpdate,
    image: UploadFile | None = None,
):
    enrollment = enrollment_repo.get_by_id(db, enrollment_id)
    if not enrollment:
        raise Exception("Inscripción no encontrada")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(enrollment, key, value)

    if image:
        if enrollment.voucher_url:
            old_path = enrollment.voucher_url.lstrip("/")
            if os.path.exists(old_path):
                os.remove(old_path)

        enrollment.voucher_url = save_course_voucher(image)

    return enrollment_repo.update(db, enrollment)


def delete_enrollment(db: Session, enrollment_id: int):
    enrollment = enrollment_repo.get_by_id(db, enrollment_id)
    if not enrollment:
        raise Exception("Inscripción no encontrada")

    return enrollment_repo.delete(db, enrollment)


def get_enrollment(db: Session, enrollment_id: int):
    enrollment = enrollment_repo.get_by_id(db, enrollment_id)
    if not enrollment:
        raise Exception("Inscripción no encontrada")
    return enrollment


def get_enrollments_by_course_and_role(db: Session, course_id: int, role_id: int):
    return enrollment_repo.get_all_by_course_id_and_role_id(db, course_id, role_id)


def get_enrollments_by_user(db: Session, user_id: int):
    return enrollment_repo.get_all_by_user(db, user_id)


def get_enrollments_by_role(db: Session, role_id: int):
    return enrollment_repo.get_all_by_role(db, role_id)


def get_enrollment_by_user_and_course(db: Session, user_id: int, course_id: int):
    enrollment = enrollment_repo.get_existing_enrollment(db, course_id, user_id)
    if not enrollment:
        raise Exception("Inscripción no encontrada")
    return enrollment
