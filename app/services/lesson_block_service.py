import os

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from app.helpers import recalculate_enrollment_certificate
from app.models.block_progress import BlockProgress
from app.models.lesson_block import LessonBlock
from app.repositories import (
    block_progress_repo,
    course_repo,
    enrollment_repo,
    forum_response_repo,
    homework_response_repo,
    lesson_block_repo,
    lesson_repo,
    quizz_response_repo,
    survey_response_repo,
)
from app.schemas.lesson_block import LessonBlockCreate, LessonBlockUpdate
from app.utils.file_upload import save_lesson_file

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class LessonNotFoundError(Exception):
    pass


class LessonBlockNotFoundError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================
def create_lesson_block(
    db: Session,
    data: LessonBlockCreate,
    business_id: int,
    file: UploadFile | None = None,
):
    with db.begin():
        lesson = lesson_repo.get_by_id(db, data.lesson_id, business_id)
        if not lesson:
            raise LessonNotFoundError("Lección no encontrada")

        content = data.content.copy() if data.content else {}

        if file:
            file_data = save_lesson_file(file, business_id)

            if file_data:
                content.update(
                    {
                        "file_url": file_data["file_url"],
                        "filename": file_data["filename"],
                        "stored_name": file_data["stored_name"],
                    }
                )

        lesson_block = LessonBlock(
            **data.model_dump(exclude={"content"}),
            content=content,
            business_id=business_id
        )

        lesson_block = lesson_block_repo.create(db, lesson_block)

        course_id = lesson.module.course_id
        if not course_id:
            raise CourseNotFoundError("Curso no encontrado")
        enrollments = enrollment_repo.get_all_by_course(db, course_id, business_id)

        if enrollments:
            progress_objects = [
                BlockProgress(
                    enrollment_id=enrollment.id,
                    lesson_block_id=lesson_block.id,
                    business_id=business_id,
                )
                for enrollment in enrollments
            ]

            block_progress_repo.create_bulk(db, progress_objects)

        return lesson_block


def update_lesson_block(
    db: Session,
    lesson_block_id: int,
    data: LessonBlockUpdate,
    business_id: int,
    file: UploadFile | None = None,
):
    old_file_path_to_delete = None
    new_file_path_to_delete_on_error = None

    try:
        with db.begin():
            lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id, business_id)

            if not lesson_block:
                raise LessonBlockNotFoundError("Bloque no encontrado")

            old_counts_toward_grade = lesson_block.counts_toward_grade

            data_dict = data.model_dump(exclude_unset=True)

            update_data = {
                key: value for key, value in data_dict.items() if key != "content"
            }
            for key, value in update_data.items():
                setattr(lesson_block, key, value)

            current_content = (lesson_block.content or {}).copy()

            if "content" in data_dict and data_dict["content"] is not None:
                current_content.update(jsonable_encoder(data_dict["content"]))

            if file:
                old_file_url = current_content.get("file_url")
                if old_file_url:
                    old_file_path_to_delete = old_file_url.lstrip("/")

                file_data = save_lesson_file(file, business_id)
                new_file_path_to_delete_on_error = file_data["file_url"].lstrip("/")

                current_content.update(
                    {
                        "file_url": file_data["file_url"],
                        "filename": file_data["filename"],
                        "stored_name": file_data.get("stored_name"),
                    }
                )

            lesson_block.content = current_content
            flag_modified(lesson_block, "content")

            course_id = lesson_block.lesson.module.course_id
            course = course_repo.get_by_id(db, course_id, business_id)
            if not course:
                raise CourseNotFoundError("Curso no encontrado")

            if (
                old_counts_toward_grade != lesson_block.counts_toward_grade
                and lesson_block.counts_toward_grade == True
                and course.is_mdt == False
            ):

                enrollments = enrollment_repo.get_all_by_course(
                    db, course_id, business_id
                )

                for enrollment in enrollments:
                    recalculate_enrollment_certificate.recalculate_enrollment_certificate_MOOC(
                        db, enrollment, business_id
                    )

        if old_file_path_to_delete and os.path.exists(old_file_path_to_delete):
            os.remove(old_file_path_to_delete)

        return lesson_block

    except Exception:
        if new_file_path_to_delete_on_error and os.path.exists(
            new_file_path_to_delete_on_error
        ):
            os.remove(new_file_path_to_delete_on_error)
        raise


def delete_lesson_block(db: Session, lesson_block_id: int, business_id: int):
    file_path_to_delete = None

    with db.begin():
        lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id, business_id)
        if not lesson_block:
            raise LessonBlockNotFoundError("Bloque no encontrado")

        was_counting_toward_grade = lesson_block.counts_toward_grade

        course_id = lesson_block.lesson.module.course_id
        course = course_repo.get_by_id(db, course_id, business_id)
        if not course:
            raise CourseNotFoundError("Curso no encontrado")

        if lesson_block.content and isinstance(lesson_block.content, dict):
            old_file_url = lesson_block.content.get("file_url")
            if old_file_url:
                file_path_to_delete = old_file_url.lstrip("/")

        cascade_steps = [
            # Blocks
            homework_response_repo.delete_soft_by_lesson_block(),
            forum_response_repo.delete_soft_by_lesson_block(),
            survey_response_repo.delete_soft_by_lesson_block(),
            quizz_response_repo.delete_soft_by_lesson_block(),
            # Progress
            block_progress_repo.delete_soft_by_lesson(),
        ]
        for step in cascade_steps:
            step(db, lesson_block_id, business_id)
        lesson_block_repo.delete_soft_by_id(db, lesson_block_id, business_id)

        if was_counting_toward_grade and course.is_mdt == False:
            enrollments = enrollment_repo.get_all_by_course(db, course_id, business_id)

            for enrollment in enrollments:
                recalculate_enrollment_certificate.recalculate_enrollment_certificate_MOOC(
                    db, enrollment, business_id
                )

    if file_path_to_delete and os.path.exists(file_path_to_delete):
        try:
            os.remove(file_path_to_delete)
        except Exception:
            pass

    return lesson_block


def get_lesson_block(db: Session, lesson_block_id: int, business_id: int):
    lesson_block = lesson_block_repo.get_by_id(db, lesson_block_id, business_id)
    if not lesson_block:
        raise LessonBlockNotFoundError("Bloque no encontrado")
    return lesson_block


def get_by_lesson(db: Session, lesson_id: int, business_id: int):
    return lesson_block_repo.get_all_by_lesson_id(db, lesson_id, business_id)


def get_all_default_blocks_by_course_and_block_type(
    db: Session, course_id: int, block_type_id: int, business_id: int
):
    return lesson_block_repo.get_all_default_blocks_by_course_and_block_type(
        db, course_id, block_type_id, business_id
    )


"""
def create_lesson_block(
    db: Session,
    data: LessonBlockCreate,
    file: UploadFile | None = None,
):
    with db.begin():
        lesson = lesson_repo.get_by_id(db, data.lesson_id)
        if not lesson:
            raise ValueError("Lección no encontrada")

        content = data.content.copy() if data.content else {}

        if file:
            file_data = save_lesson_file(file)

            if file_data:
                content.update(
                    {
                        "file_url": file_data["file_url"],
                        "filename": file_data["filename"],
                        "stored_name": file_data["stored_name"],
                    }
                )

        lesson_block = LessonBlock(
            **data.model_dump(exclude={"content"}),
            content=content,
        )

        lesson_block = lesson_block_repo.create(db, lesson_block)

        course_id = lesson.module.course_id
        enrollments = enrollment_repo.get_all_by_course_id(db, course_id)

        if enrollments:
            progress_objects = [
                BlockProgress(
                    enrollment_id=enrollment.id,
                    lesson_block_id=lesson_block.id,
                )
                for enrollment in enrollments
            ]

            block_progress_repo.bulk_create(db, progress_objects)

        return lesson_block


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
                raise ValueError("Bloque no encontrado")

            old_counts_toward_grade = lesson_block.counts_toward_grade

            data_dict = data.model_dump(exclude_unset=True)

            update_data = {
                key: value for key, value in data_dict.items() if key != "content"
            }
            for key, value in update_data.items():
                setattr(lesson_block, key, value)

            current_content = (lesson_block.content or {}).copy()

            if "content" in data_dict and data_dict["content"] is not None:
                current_content.update(jsonable_encoder(data_dict["content"]))

            if file:
                old_file_url = current_content.get("file_url")
                if old_file_url:
                    old_file_path_to_delete = old_file_url.lstrip("/")

                file_data = save_lesson_file(file)
                new_file_path_to_delete_on_error = file_data["file_url"].lstrip("/")

                current_content.update(
                    {
                        "file_url": file_data["file_url"],
                        "filename": file_data["filename"],
                        "stored_name": file_data.get("stored_name"),
                    }
                )

            lesson_block.content = current_content
            flag_modified(lesson_block, "content")

            lesson_block = lesson_block_repo.update(db, lesson_block)

            if old_counts_toward_grade != lesson_block.counts_toward_grade:
                course_id = lesson_block.lesson.module.course_id
                enrollments = enrollment_repo.get_all_by_course_id(db, course_id)

                for enrollment in enrollments:
                    recalculate_enrollment_certificate_optimized(db, enrollment)

        if old_file_path_to_delete and os.path.exists(old_file_path_to_delete):
            os.remove(old_file_path_to_delete)

        return lesson_block

    except Exception:
        if new_file_path_to_delete_on_error and os.path.exists(
            new_file_path_to_delete_on_error
        ):
            os.remove(new_file_path_to_delete_on_error)
        raise


def delete_lesson_block(db: Session, lesson_block_id: int):
    with db.begin():

        lesson_block = lesson_block_repo.get_by_id(
            db,
            lesson_block_id,
        )

        if not lesson_block:
            raise Exception("Bloque no encontrado")

        progresses = block_progress_repo.get_by_lesson_block_id(
            db,
            lesson_block_id,
        )

        for progress in progresses:
            block_progress_repo.delete(
                db,
                progress,
            )

        lesson_block_repo.delete(
            db,
            lesson_block,
        )

        return lesson_block


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
"""
