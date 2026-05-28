import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.helpers.recalculate_enrollment_certificate import (
    recalculate_enrollment_certificate,
)
from app.models.lesson_block import LessonBlock
from app.repositories import enrollment_repo, lesson_block_repo
from app.schemas.lesson_block import LessonBlockCreate, LessonBlockUpdate
from app.utils.file_upload import save_lesson_file
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.attributes import flag_modified


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
    old_file_path_to_delete = None
    new_file_path_to_delete_on_error = None

    try:
        with db.begin():
            lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id)

            if not lesson_block:
                raise Exception("Bloque no encontrado")

            old_counts_toward_grade = lesson_block.counts_toward_grade

            data_dict = data.model_dump(
                exclude_unset=True,
            )

            update_data = {
                key: value
                for key, value in data_dict.items()
                if key != "content"
            }

            for key, value in update_data.items():
                setattr(lesson_block, key, value)

            if file:
                old_file_url = (lesson_block.content or {}).get("file_url")

                if old_file_url:
                    old_file_path_to_delete = old_file_url.lstrip("/")

                file_data = save_lesson_file(file)

                new_file_path_to_delete_on_error = file_data["file_url"].lstrip("/")

                lesson_block.content = {
                    "file_url": file_data["file_url"],
                    "filename": file_data["filename"],
                }

                flag_modified(lesson_block, "content")

            elif "content" in data_dict:
                incoming_content = data_dict.get("content")

                if incoming_content is not None:
                    lesson_block.content = jsonable_encoder(incoming_content)
                    flag_modified(lesson_block, "content")

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

        if old_file_path_to_delete and os.path.exists(old_file_path_to_delete):
            os.remove(old_file_path_to_delete)

        return lesson_block

    except Exception:
        if new_file_path_to_delete_on_error and os.path.exists(new_file_path_to_delete_on_error):
            os.remove(new_file_path_to_delete_on_error)

        raise


def delete_lesson_block(db: Session, lesson_block_id: int):
    lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id)
    if not lesson_block:
        raise Exception("Bloque no encontrado")
    return lesson_block_repo.delete(db, lesson_block)


def get_lesson_block(db: Session, lesson_block_id: int):
    return lesson_block_repo.get_by_id(db, lesson_block_id)


def get_by_lesson(db: Session, lesson_id: int):
    return lesson_block_repo.get_all_by_lesson_id(db, lesson_id)


def get_all_default_blocks_by_course_and_block_type(
    db: Session, course_id: int, block_type_id: int
):
    return lesson_block_repo.get_all_default_blocks_by_course_and_block_type(
        db, course_id, block_type_id
    )
