from sqlalchemy.orm import Session
from app.models.quizz_response import QuizzResponse
from app.repositories import quizz_response_repo
from app.schemas.quizz_response import QuizzResponseCreate, QuizzResponseUpdate
from app.repositories.lesson_block_repo import get_by_id as LES_BLO_get_by_id
from app.repositories.certificate_repo import (
    get_by_user_and_course as CER_get_by_user_and_course,
    update as CER_update,
)


def create_quizz_response(db: Session, data: QuizzResponseCreate):
    existing = quizz_response_repo.get_by_enrollment_and_lesson_block(
        db, data.enrollment_id, data.lesson_block_id
    )
    if existing:
        raise Exception("Registro existente")
    quizz_response = QuizzResponse(**data.model_dump())
    return quizz_response_repo.create(db, quizz_response)


def update_quizz_response(
    db: Session, quizz_response_id: int, data: QuizzResponseUpdate
):
    quizz_response = quizz_response_repo.get_by_id(db, quizz_response_id)
    if not quizz_response:
        raise Exception("Respuestas no encontradas")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(quizz_response, key, value)

    response = quizz_response_repo.update(db, quizz_response)

    if update_data.get("score") is not None or update_data.get("is_passed") is not None:
        enrollment_id = quizz_response.enrollment_id
        quizzes = get_by_enrollment(db, enrollment_id)
        final_grade = calculate_final_grade_average(quizzes)
        certificate = CER_get_by_user_and_course(
            db, quizz_response.enrollment.user_id, quizz_response.enrollment.course_id
        )
        if certificate:
            certificate.final_grade = final_grade
            CER_update(db, certificate)

    return response


def delete_quizz_response(db: Session, quizz_response_id: int):
    quizz_response = quizz_response_repo.get_by_id(db, quizz_response_id)
    if not quizz_response:
        raise Exception("Respuestas no encontradas")

    return quizz_response_repo.delete(db, quizz_response)


def get_quizz_response(db: Session, quizz_response_id: int):
    quizz_response = quizz_response_repo.get_by_id(db, quizz_response_id)
    if not quizz_response:
        raise Exception("Respuestas no encontradas")
    return quizz_response


def get_by_enrollment(db: Session, enrollment_id: int):
    quizzes = quizz_response_repo.get_all_by_enrollment(db, enrollment_id)
    return [
        quizz
        for quizz in quizzes
        if (lesson_block := LES_BLO_get_by_id(db, quizz.lesson_block_id))
        and lesson_block.is_required
    ]


def get_by_block(db: Session, lesson_block_id: int):
    return quizz_response_repo.get_all_by_lesson_block(db, lesson_block_id)


def get_one_by_enrollment(db: Session, enrollment_id: int):
    quizz_response = quizz_response_repo.get_by_enrollment(db, enrollment_id)

    if not quizz_response:
        raise Exception("Respuestas no encontradas")

    return quizz_response


# Auxiliares


def calculate_final_grade_average(quizz_responses: list[QuizzResponse]) -> float | None:
    if not quizz_responses:
        return None

    total_score = sum(
        quizz_response.score
        for quizz_response in quizz_responses
        if quizz_response.score is not None
    )
    count = sum(
        1 for quizz_response in quizz_responses if quizz_response.score is not None
    )

    if count == 0:
        return None

    return total_score / count
