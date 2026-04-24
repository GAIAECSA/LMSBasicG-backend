from sqlalchemy.orm import Session
from app.repositories import lesson_block_repo
from app.models.lesson_block import LessonBlock
from app.schemas.lesson_block import LessonBlockCreate, LessonBlockUpdate
from fastapi import UploadFile
from app.utils.file_upload import save_lesson_file
import os

def create_lesson_block(db: Session, data: LessonBlockCreate, file: UploadFile | None = None):
    content = {}

    if file:
        file_data = save_lesson_file(file)

        content = {
            "file_url": file_data["file_url"],
            "filename": file_data["filename"]
        }
    
    elif data.content:
        content = data.content

    lesson_block = LessonBlock(**data.model_dump(), content = content)
    return lesson_block_repo.create(db, lesson_block)

def update_lesson_block(db: Session, lesson_block_id: int, data: LessonBlockUpdate):
    lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id)
    if not lesson_block:
        raise Exception("Bloque no encontrado")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(lesson_block, key, value)

    return lesson_block_repo.update(db, lesson_block)

def delete_lesson_block(db: Session, lesson_block_id: int):
    lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id)
    if not lesson_block:
        raise Exception("Bloque no encontrado")
    return lesson_block_repo.delete(db, lesson_block)

def get_lesson_block(db: Session, lesson_block_id: int):
    return lesson_block_repo.get_by_id(db, lesson_block_id)

def get_by_lesson(db: Session, lesson_id: int):
    return lesson_block_repo.get_all_by_lesson_id(db, lesson_id)