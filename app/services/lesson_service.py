from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.repositories import (
    block_progress_repo,
    forum_response_repo,
    homework_response_repo,
    lesson_block_repo,
    lesson_repo,
    quizz_response_repo,
    survey_response_repo,
)
from app.schemas.lesson import LessonCreate, LessonUpdate

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class LessonNotFoundError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def create_lesson(db: Session, data: LessonCreate, business_id: int):
    with db.begin():

        lesson = Lesson(**data.model_dump(), business_id=business_id)
        return lesson_repo.create(db, lesson)


def update_lesson(db: Session, lesson_id: int, data: LessonUpdate, business_id: int):
    with db.begin():
        lesson = lesson_repo.get_by_id(db, lesson_id, business_id)
        if not lesson:
            raise LessonNotFoundError("Lección no encontrada")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(lesson, key, value)

        return lesson


def delete_lesson(db: Session, lesson_id: int, business_id: int):
    with db.begin():
        lesson = lesson_repo.get_by_id(db, lesson_id, business_id)
        if not lesson:
            raise LessonNotFoundError("Lección no encontrada")
        cascade_steps = [
            # Blocks
            homework_response_repo.delete_soft_by_lesson(),
            forum_response_repo.delete_soft_by_lesson(),
            survey_response_repo.delete_soft_by_lesson(),
            quizz_response_repo.delete_soft_by_lesson(),
            # Navigation
            lesson_block_repo.delete_soft_by_lesson(),
            # Progress
            block_progress_repo.delete_soft_by_lesson(),
        ]
        for step in cascade_steps:
            step(db, lesson_id, business_id)
        return lesson_repo.delete_soft_by_id(db, lesson_id, business_id)


def get_lesson(db: Session, lesson_id: int, business_id: int):
    lesson = lesson_repo.get_by_id(db, lesson_id, business_id)
    if not lesson:
        raise LessonNotFoundError("Lección no encontrada")
    return lesson


def get_lessons_by_module(db: Session, module_id: int, business_id: int):
    return lesson_repo.get_by_module_id(db, module_id, business_id)


"""
def create_lesson(db: Session, data: LessonCreate):
    lesson = Lesson(**data.model_dump())
    return lesson_repo.create(db, lesson)


def update_lesson(db: Session, lesson_id: int, data: LessonUpdate):
    lesson = lesson_repo.get_by_id(db, lesson_id)
    if not lesson:
        raise Exception("Lección no encontrada")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(lesson, key, value)

    return lesson_repo.update(db, lesson)


def delete_lesson(db: Session, lesson_id: int):
    lesson = lesson_repo.get_by_id(db, lesson_id)
    if not lesson:
        raise Exception("Lección no encontrada")
    return lesson_repo.delete(db, lesson)


def get_lesson(db: Session, lesson_id: int):
    return lesson_repo.get_by_id(db, lesson_id)


def get_lessons_by_module(db: Session, module_id: int):
    return lesson_repo.get_by_module_id(db, module_id)
"""
