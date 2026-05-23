from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
from app.services.certificate_service import calculate_final_grade_average
from app.repositories.certificate_repo import (
    get_by_user_and_course as CER_get_by_user_and_course,
    update as CER_update,
)


def recalculate_enrollment_certificate(
    db: Session,
    enrollment: Enrollment,
):

    course = enrollment.course

    if not course or course.is_mdt:
        return

    final_grade = calculate_final_grade_average(
        db=db,
        user_id=enrollment.user_id,
        course_id=enrollment.course_id,
    )

    certificate = CER_get_by_user_and_course(
        db=db,
        user_id=enrollment.user_id,
        course_id=enrollment.course_id,
    )

    if not certificate:
        return

    certificate.final_grade = final_grade

    CER_update(
        db=db,
        certificate=certificate,
    )
