from app.models.lesson_block import LessonBlock
from sqlalchemy.orm import Session
from fastapi import UploadFile
import os

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.utils.file_upload import save_course_image
from app.repositories import course_repo
from app.repositories import enrollment_repo
from app.repositories import lesson_block_repo


def create_course(
    db: Session,
    data: CourseCreate,
    image: UploadFile | None = None,
):

    with db.begin():

        existing = course_repo.get_by_name_and_subcategory(
            db,
            data.name,
            data.subcategory_id,
        )

        if existing:
            raise ValueError("El curso ya existe en esta subcategoría")

        image_url = save_course_image(image) if image else None

        course = Course(
            **data.model_dump(),
            image_url=image_url,
        )

        course_repo.create(db, course)

        lesson_block_repo.create_all(
            db,
            create_default_blocks(),
        )

        return course


def update_course(
    db: Session,
    course_id: int,
    data: CourseUpdate,
    image: UploadFile | None = None,
):

    with db.begin():

        course = course_repo.get_by_id(db, course_id)

        if not course:
            raise Exception("Curso no encontrado")

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] != course.name:
            existing = course_repo.get_by_name_and_subcategory(
                db,
                update_data["name"],
                course.subcategory_id,
            )

            if existing:
                raise Exception("El curso ya existe en esta subcategoría")

        old_is_mdt = course.is_mdt
        new_is_mdt = update_data.get("is_mdt", old_is_mdt)

        for key, value in update_data.items():
            setattr(course, key, value)

        if image:

            if course.image_url:
                old_path = course.image_url.lstrip("/")

                if os.path.exists(old_path):
                    os.remove(old_path)

            course.image_url = save_course_image(image)

        handle_mdt_blocks_transition(
            db=db,
            course=course,
            old_is_mdt=old_is_mdt,
            new_is_mdt=new_is_mdt,
        )

        return course_repo.update(db, course)


def delete_course(db: Session, course_id: int):
    course = course_repo.get_by_id(db, course_id)

    if not course:
        raise Exception("Curso no encontrado")

    enrollment_repo.delete_by_course_id(db, course_id)
    return course_repo.delete(db, course)


def get_course(db: Session, course_id: int):
    return course_repo.get_by_id(db, course_id)


def get_courses_by_subcategory(db: Session, subcategory_id: int):
    return course_repo.get_by_subcategory_id(db, subcategory_id)


def get_all_courses(db: Session):
    return course_repo.get_all(db)


# Privados
DEFAULT_MDT_BLOCKS = [
    {
        "content": {
            "title": "Copia Cédula",
            "instructions": "Subir la copia de cédula",
            "attachments": [],
        },
        "order": 0,
        "completion_type": "SUBIR",
        "is_active": True,
    },
    {
        "content": {
            "title": "Copia Título",
            "instructions": "Subir la copia de título",
            "attachments": [],
        },
        "order": 1,
        "completion_type": "SUBIR",
        "is_active": True,
    },
    {
        "content": {
            "title": "Copia de Certificado Laboral",
            "instructions": "Subir la copia de certificado laboral",
            "attachments": [],
        },
        "order": 2,
        "completion_type": "SUBIR",
        "is_active": True,
    },
    {
        "content": {
            "title": "Comprobante de pago",
            "instructions": "Subir el comprobante de pago",
            "attachments": [],
        },
        "order": 3,
        "completion_type": "SUBIR",
        "is_active": True,
    },
    {
        "content": {
            "title": "Informe del Instructor",
            "instructions": "Subir el informe del instructor",
            "attachments": [],
        },
        "order": 4,
        "completion_type": "VER",
        "is_active": False,
    },
    {
        "content": {
            "title": "Evidencia asistencia",
            "instructions": "Evidencia asistencia",
            "attachments": [],
        },
        "order": 5,
        "completion_type": "VER",
        "is_active": False,
    },
]


def create_default_blocks():

    return [
        build_lesson_block(
            content=block["content"],
            order=block["order"],
            completion_type=block["completion_type"],
            is_active=block["is_active"],
        )
        for block in DEFAULT_MDT_BLOCKS
    ]


def build_lesson_block(
    content: dict,
    order: int,
    completion_type: str,
    is_active: bool,
    course_id: int | None = None,
):
    return LessonBlock(
        content=content,
        completion_type=completion_type,
        completion_value=0,
        order=order,
        default=True,
        lesson_id=None,
        block_type_id=1,
        course_id=course_id,
        date_available=None,
        is_active=is_active,
        deleted=False,
    )


def handle_mdt_blocks_transition(
    db: Session,
    course: Course,
    old_is_mdt: bool,
    new_is_mdt: bool,
):

    if not old_is_mdt and new_is_mdt:

        existing_blocks = lesson_block_repo.get_default_by_course_id(
            db,
            course.id,
        )

        if not existing_blocks:

            blocks = create_default_blocks(course.id)

            lesson_block_repo.create_all(
                db,
                blocks,
            )

    elif old_is_mdt and not new_is_mdt:

        lesson_block_repo.delete_default_by_course_id(
            db,
            course.id,
        )
