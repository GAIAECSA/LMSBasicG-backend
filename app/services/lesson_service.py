from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.repositories import lesson_repo
from app.schemas.lesson import LessonCreate, LessonUpdate

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