from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
from app.repositories import enrollment_repo
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate
from fastapi import UploadFile
from app.utils.file_upload import save_course_voucher
import os

def create_enrollment(db: Session, data: EnrollmentCreate, image: UploadFile | None = None):
    voucher_url = None
    if image:
        voucher_url = save_course_voucher(image)
        
    enrollment = Enrollment(**data.model_dump(), voucher_url=voucher_url) 
    return enrollment_repo.create(db, enrollment)

def update_enrollment(db: Session,enrollment_id: int,data: EnrollmentUpdate,image: UploadFile | None = None):
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