from sqlalchemy.orm import Session
from app.repositories import lesson_block_repo
from app.models.lesson_block import LessonBlock
from app.schemas.lesson_block import LessonBlockCreate, LessonBlockUpdate
from fastapi import UploadFile
from app.utils.file_upload import save_lesson_file
import os

def create_lesson_block(db: Session, data: LessonBlockCreate, file: UploadFile | None = None):
    content = {}

    if file and data.content:
        raise ValueError("No puedes enviar archivo y content al mismo tiempo")

    if file:
        file_data = save_lesson_file(file)

        content = {
            "file_url": file_data["file_url"],
            "filename": file_data["filename"]
        }
    
    elif data.content:
        content = data.content

    lesson_block = LessonBlock(
        **data.model_dump(exclude={"content"}),
        content=content
    )

    return lesson_block_repo.create(db, lesson_block)

def update_lesson_block(
    db: Session,
    lesson_block_id: int,
    data: LessonBlockUpdate,
    file: UploadFile | None = None
):
    lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id)
    if not lesson_block:
        raise Exception("Bloque no encontrado")

    if file and data.content:
        raise ValueError("No puedes enviar archivo y content al mismo tiempo")

    update_data = data.model_dump(exclude_unset=True, exclude={"content"})

    for key, value in update_data.items():
        setattr(lesson_block, key, value)

    if file:
        old_content = lesson_block.content or {}
        old_file_url = old_content.get("file_url")

        if old_file_url:
            old_path = old_file_url.lstrip("/")
            if os.path.exists(old_path):
                os.remove(old_path)

        file_data = save_lesson_file(file)

        lesson_block.content = {
            "file_url": file_data["file_url"],
            "filename": file_data["filename"]
        }

    elif data.content is not None:
        lesson_block.content = data.content

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