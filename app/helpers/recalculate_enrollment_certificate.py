from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.repositories import (
    certificate_repo,
    homework_response_repo,
    quizz_response_repo,
)


def recalculate_enrollment_certificate_MOOC(
    db: Session, enrollment: Enrollment, business_id: int
):

    final_grade = calculate_final_grade_average(
        db=db, enrollment_id=enrollment.id, business_id=business_id
    )

    certificate = certificate_repo.get_by_user_and_course(
        db=db,
        user_id=enrollment.user_id,
        course_id=enrollment.course_id,
        business_id=business_id,
    )

    if not certificate:
        return

    if certificate.final_grade != final_grade:
        certificate.final_grade = final_grade


def calculate_final_grade_average(
    db: Session, enrollment_id: int, business_id: int
) -> float:

    total_score = 0
    total_items = 0

    quiz_responses = quizz_response_repo.get_all_by_enrollment_count_towards_grade(
        db=db, enrollment_id=enrollment_id, business_id=business_id
    )

    for response in quiz_responses:

        if response.score is not None:
            total_score += float(response.score)

        total_items += 1

    homework_responses = (
        homework_response_repo.get_all_by_enrollment_count_towards_grade(
            db=db,
            enrollment_id=enrollment_id,
        )
    )

    for response in homework_responses:

        if response.score is not None:
            total_score += float(response.score)

        total_items += 1

    if total_items == 0:
        return 0

    return round(total_score / total_items, 2)
