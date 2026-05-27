from sqlalchemy.orm import Session
from app.repositories import lesson_block_repo
from app.models.lesson_block import LessonBlock
from app.schemas.lesson_block import LessonBlockCreate, LessonBlockUpdate
from app.repositories import enrollment_repo
from app.helpers import recalculate_enrollment_certificate
from fastapi import UploadFile
from app.utils.file_upload import save_lesson_file
import os


def create_lesson_block(
    db: Session, data: LessonBlockCreate, file: UploadFile | None = None
):
    content = {"base": "base"}

    if file:
        # file_data = save_lesson_file(file)

        pass
        # "file_url": file_data["file_url"],
        # "filename": file_data["filename"]
        # }
    elif data.content:
        content = data.content
    else:
        pass

    lesson_block = LessonBlock(**data.model_dump(exclude={"content"}), content=content)

    return lesson_block_repo.create(db, lesson_block)


def update_lesson_block(
    db: Session,
    lesson_block_id: int,
    data: LessonBlockUpdate,
    file: UploadFile | None = None,
):
    lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id)

    if not lesson_block:
        raise Exception("Bloque no encontrado")

    old_counts_toward_grade = lesson_block.counts_toward_grade

    update_data = data.model_dump(
        exclude_unset=True,
        exclude={"content"},
    )

    for key, value in update_data.items():
        setattr(lesson_block, key, value)

    if file:
        old_file_url = (lesson_block.content or {}).get("file_url")

        if old_file_url:
            old_path = old_file_url.lstrip("/")

            if os.path.exists(old_path):
                os.remove(old_path)

        file_data = save_lesson_file(file)

        lesson_block.content = {
            "file_url": file_data["file_url"],
            "filename": file_data["filename"],
        }

    elif data.content is not None:
        lesson_block.content = data.content

    lesson_block = lesson_block_repo.update(db, lesson_block)

    if old_counts_toward_grade != lesson_block.counts_toward_grade:

        enrollments = enrollment_repo.get_all_by_course_id(
            db,
            lesson_block.lesson.module.course_id,
        )

        for enrollment in enrollments:
            recalculate_enrollment_certificate(
                db=db,
                enrollment=enrollment,
            )

    return lesson_block


def delete_lesson_block(db: Session, lesson_block_id: int):
    lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id)
    if not lesson_block:
        raise Exception("Bloque no encontrado")
    return lesson_block_repo.delete(db, lesson_block)


def get_lesson_block(db: Session, lesson_block_id: int):
    return lesson_block_repo.get_by_id(db, lesson_block_id)


def get_by_lesson(db: Session, lesson_id: int):
    return lesson_block_repo.get_all_by_lesson_id(db, lesson_id)


def get_all_default_blocks_by_course_and_block_type(db: Session, course_id: int, block_type_id: int):
    return lesson_block_repo.get_all_default_blocks_by_course_and_block_type(db, course_id, block_type_id)
