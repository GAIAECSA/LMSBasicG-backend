from sqlalchemy.orm import Session
from app.models.quizz_response import QuizzResponse
from app.repositories import quizz_response_repo
from app.schemas.quizz_response import QuizzResponseCreate, QuizzResponseUpdate
from app.services.lesson_block_service import get_lesson_block

def create_quizz_response(db: Session, data: QuizzResponseCreate):
    existing = quizz_response_repo.get_by_enrollment_and_lesson_block(db,data.enrollment_id,data.lesson_block_id)
    if existing:
        raise Exception("Registro existente")
    quizz_response = QuizzResponse(**data.model_dump())
    return quizz_response_repo.create(db, quizz_response)

def update_quizz_response(db: Session, quizz_response_id: int, data: QuizzResponseUpdate):
    quizz_response = quizz_response_repo.get_by_id(db, quizz_response_id)
    if not quizz_response:
        raise Exception("Respuestas no encontradas")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(quizz_response, key, value)

    return quizz_response_repo.update(db, quizz_response)

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
    quizzes = quizz_response_repo.get_all_by_enrollment(
        db,
        enrollment_id
    )
    return [
        quizz
        for quizz in quizzes
        if (
            lesson_block := get_lesson_block(
                db,
                quizz.lesson_block_id
            )
        ) and lesson_block.is_required
    ]

def get_by_block(db: Session, lesson_block_id: int):
    return quizz_response_repo.get_all_by_lesson_block(db, lesson_block_id)

def get_one_by_enrollment(
    db: Session,
    enrollment_id: int
):
    quizz_response = quizz_response_repo.get_by_enrollment(
        db,
        enrollment_id
    )

    if not quizz_response:
        raise Exception("Respuestas no encontradas")

    return quizz_response