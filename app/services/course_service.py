from sqlalchemy.orm import Session
from fastapi import UploadFile
import os

from app.models.course import Course
from app.repositories import course_repo
from app.schemas.course import CourseCreate, CourseUpdate
from app.utils.file_upload import save_course_image


def create_course(db: Session, data: CourseCreate, image: UploadFile | None = None):
    existing = course_repo.get_by_name_and_subcategory(
        db, data.name, data.subcategory_id
    )
    if existing:
        raise Exception("El curso ya existe en esta subcategoría")

    image_url = save_course_image(image)

    course = Course(
        **data.model_dump(),
        image_url=image_url
    )

    return course_repo.create(db, course)

def update_course(
    db: Session,
    course_id: int,
    data: CourseUpdate,
    image: UploadFile | None = None
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
    return course_repo.delete(db, course)

def get_course(db: Session, course_id: int):
    return course_repo.get_by_id(db, course_id)

def get_courses_by_subcategory(db: Session, subcategory_id: int):
    return course_repo.get_by_subcategory_id(db, subcategory_id)

def get_all_courses(db: Session):
    return course_repo.get_all(db)