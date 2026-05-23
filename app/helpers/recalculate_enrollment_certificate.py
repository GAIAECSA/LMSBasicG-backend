from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment

from app.repositories.quizz_response_repo import (
    get_all_by_enrollment as QUI_get_by_enrollment,
)

from app.repositories.homework_response_repo import (
    get_all_by_enrollment as HW_get_by_enrollment,
)

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
        enrollment_id=enrollment.id,
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
    enrollment_id: int,
) -> float:

    total_score = 0
    total_items = 0

    quiz_responses = QUI_get_by_enrollment(
        db=db,
        enrollment_id=enrollment_id,
    )

    for response in quiz_responses:

        if response.score is None:
            continue

        block = response.lesson_block

        if block and not block.counts_toward_grade:
            continue

        total_score += float(response.score)
        total_items += 1

    homework_responses = HW_get_by_enrollment(
        db=db,
        enrollment_id=enrollment_id,
    )

    for response in homework_responses:

        if response.score is None:
            continue

        block = response.lesson_block

        if block and not block.counts_toward_grade:
            continue

        total_score += float(response.score)
        total_items += 1

    if total_items == 0:
        return 0

    return round(total_score / total_items, 2)
