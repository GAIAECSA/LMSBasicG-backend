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
            raise ValueError(
                "El curso ya existe en esta subcategoría"
            )

        image_url = (
            save_course_image(image)
            if image
            else None
        )

        course = Course(
            **data.model_dump(),
            image_url=image_url,
        )

        course_repo.create(db, course)

        blocks = [
            build_lesson_block(
                {
                    "type": "introduction",
                    "text": "Bienvenido al curso!",
                },
                0,
            ),
            build_lesson_block(
                {
                    "type": "video",
                    "url": "https://...",
                },
                1,
            ),
            build_lesson_block(
                {
                    "type": "quiz",
                    "questions": [],
                },
                2,
            ),
        ]

        lesson_block_repo.create_all(
            db,
            blocks,
        )

        return course


def update_course(
    db: Session, course_id: int, data: CourseUpdate, image: UploadFile | None = None
):
    course = course_repo.get_by_id(db, course_id)

    if not course:
        raise Exception("Curso no encontrado")

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] != course.name:
        existing = course_repo.get_by_name_and_subcategory(
            db, update_data["name"], course.subcategory_id
        )
        if existing:
            raise Exception("El curso ya existe en esta subcategoría")

    for key, value in update_data.items():
        setattr(course, key, value)

    if image:
        if course.image_url:
            old_path = course.image_url.lstrip("/")
            if os.path.exists(old_path):
                os.remove(old_path)

        course.image_url = save_course_image(image)

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




def build_lesson_block(
    content: dict,
    order: int,
):
    return LessonBlock(
        content=content,
        completion_type="automatic",
        completion_value=0,
        order=order,
        default=True,
        lesson_id=None,
        block_type_id=1,
        date_available=None,
        is_active=True,
        deleted=False,
    )