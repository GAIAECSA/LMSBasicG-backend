from sqlalchemy.orm import Session
from app.helpers import recalculate_enrollment_certificate
from app.helpers.recalculate_enrollment_certificate import (
    recalculate_enrollment_certificate,
)
from fastapi import UploadFile
from app.models.homework_response import HomeworkResponse
from app.repositories import homework_response_repo
from app.schemas.homework_response import (
    HomeworkResponseCreate,
    HomeworkResponseUpdate,
    HomeworkResponseGrade,
)

from app.utils.file_upload import save_homework_file
import os
import logging

logger = logging.getLogger(__name__)


def create_homework_response(
    db: Session,
    data: HomeworkResponseCreate,
    file: UploadFile | None,
):

    with db.begin():

        existing = homework_response_repo.get_by_enrollment_and_lesson_block(
            db,
            data.enrollment_id,
            data.lesson_block_id,
        )

        if existing:
            raise Exception("La tarea ya fue enviada")

        submitted_file_url = None
        submitted_filename = None

        if file:

            saved_file = save_homework_file(file)

            submitted_file_url = saved_file["file_url"]

            submitted_filename = saved_file["filename"]

        homework_response = HomeworkResponse(
            **data.model_dump(),
            submitted_file_url=submitted_file_url,
            submitted_filename=submitted_filename,
        )

        response = homework_response_repo.create(
            db,
            homework_response,
        )

        if response.score is not None:

            recalculate_enrollment_certificate(
                db=db,
                enrollment=response.enrollment,
            )

    return response


def update_homework_response(
    db: Session,
    homework_response_id: int,
    data: HomeworkResponseUpdate,
    file: UploadFile | None,
):

    old_file_path = None

    with db.begin():

        homework_response = homework_response_repo.get_by_id(
            db,
            homework_response_id,
        )

        if not homework_response:
            raise Exception("Entrega no encontrada")

        update_data = data.model_dump(exclude_unset=True)

        if file:

            if homework_response.submitted_file_url:

                old_file_path = homework_response.submitted_file_url.lstrip("/")

            saved_file = save_homework_file(file)

            update_data["submitted_file_url"] = saved_file["file_url"]

            update_data["submitted_filename"] = saved_file["filename"]

        for key, value in update_data.items():
            setattr(homework_response, key, value)

        updated = homework_response_repo.update(
            db,
            homework_response,
        )

        if data.score is not None:

            recalculate_enrollment_certificate(
                db=db,
                enrollment=updated.enrollment,
            )

    if file and old_file_path and os.path.exists(old_file_path):

        try:

            os.remove(old_file_path)

        except Exception as e:

            logger.warning(f"No se pudo eliminar archivo viejo: {e}")

    return updated


def grade_homework_response(
    db: Session, homework_response_id: int, data: HomeworkResponseGrade
):

    homework_response = homework_response_repo.get_by_id(db, homework_response_id)

    if not homework_response:
        raise Exception("Entrega no encontrada")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(homework_response, key, value)

    return homework_response_repo.update(db, homework_response)


def delete_homework_response(db: Session, homework_response_id: int):

    homework_response = homework_response_repo.get_by_id(db, homework_response_id)

    if not homework_response:
        raise Exception("Entrega no encontrada")

    return homework_response_repo.delete(db, homework_response)


def get_homework_response(db: Session, homework_response_id: int):

    homework_response = homework_response_repo.get_by_id(db, homework_response_id)

    if not homework_response:
        raise Exception("Entrega no encontrada")

    return homework_response


def get_homework_response_by_enrollment_and_block(
    db: Session, enrollment_id: int, lesson_block_id: int
):

    homework_response = homework_response_repo.get_by_enrollment_and_lesson_block(
        db, enrollment_id, lesson_block_id
    )

    if not homework_response:
        raise Exception("Entrega no encontrada")

    return homework_response


def get_homework_responses_by_enrollment(db: Session, enrollment_id: int):

    return homework_response_repo.get_all_by_enrollment(db, enrollment_id)


def get_homework_responses_by_lesson_block(db: Session, lesson_block_id: int):

    return homework_response_repo.get_all_by_lesson_block(db, lesson_block_id)


def get_homework_responses_by_course_default(
    db: Session,
    course_id: int,
):

    return homework_response_repo.get_by_course_id_default(
        db,
        course_id,
    )
