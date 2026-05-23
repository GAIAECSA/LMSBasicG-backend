from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
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


def calculate_final_grade_average(
    db: Session,
    user_id: int,
    course_id: int,
) -> float:

    responses = (
        db.query(HomeworkResponse)
        .join(
            LessonBlock,
            LessonBlock.id == HomeworkResponse.lesson_block_id,
        )
        .filter(
            HomeworkResponse.user_id == user_id,
            HomeworkResponse.course_id == course_id,
            LessonBlock.is_required == True,
            HomeworkResponse.grade.isnot(None),
        )
        .all()
    )

    if not responses:
        return 0

    total = sum(r.grade for r in responses)

    return round(total / len(responses), 2)
