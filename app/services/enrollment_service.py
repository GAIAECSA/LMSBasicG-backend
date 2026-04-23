from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
from app.repositories import enrollment_repo
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate

def create_enrollment(db: Session, data: EnrollmentCreate):
    enrollment = Enrollment(**data.model_dump()) 
    return enrollment_repo.create(db, enrollment)

def update_enrollment(db: Session, enrollment_id: int, data: EnrollmentUpdate):
    enrollment = enrollment_repo.get_by_id(db, enrollment_id)
    if not enrollment:
        raise Exception("Inscripción no encontrada")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(enrollment, key, value)

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