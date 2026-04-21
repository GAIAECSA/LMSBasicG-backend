from sqlalchemy.orm import Session
from app.models.course import Course
from app.repositories import course_repo
from app.schemas.course import CourseCreate, CourseUpdate

def create_course(db: Session, data: CourseCreate):
    course = Course(**data.model_dump())
    return course_repo.create(db, course)

def update_course(db: Session, course_id: int, data: CourseUpdate):
    course = course_repo.get_by_id(db, course_id)
    if not course:
        return None
    for key, value in data.model_dump().items():
        setattr(course, key, value)
    return course_repo.update(db, course)

def delete_course(db: Session, course_id: int):
    course = course_repo.get_by_id(db, course_id)
    if not course:
        return None
    return course_repo.delete(db, course)

def get_course(db: Session, course_id: int):
    return course_repo.get_by_id(db, course_id)

def get_courses_by_subcategory(db: Session, subcategory_id: int):
    return course_repo.get_by_subcategory_id(db, subcategory_id)

def get_all_courses(db: Session):
    return course_repo.get_all(db)