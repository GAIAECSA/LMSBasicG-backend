from sqlalchemy.orm import Session
from app.models.course_attendance import CourseAttendance
from app.repositories import course_attendance_repo
from app.schemas.course_attendance import CourseAttendanceCreate, CourseAttendanceUpdate


def create_course_attendance(db: Session, data: CourseAttendanceCreate):
    course_attendance = CourseAttendance(**data.model_dump())
    return course_attendance_repo.create(db, course_attendance)


def update_course_attendance(
    db: Session, course_attendance_id: int, data: CourseAttendanceUpdate
):
    course_attendance = course_attendance_repo.get_by_id(db, course_attendance_id)
    if not course_attendance:
        raise Exception("No encontrado")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(course_attendance, key, value)

    return course_attendance_repo.update(db, course_attendance)


def delete_course_attendance(db: Session, course_attendance_id: int):
    course_attendance = course_attendance_repo.get_by_id(db, course_attendance_id)
    if not course_attendance:
        raise Exception("No encontrado")
    return course_attendance_repo.delete(db, course_attendance)


def get_course_attendance(db: Session, course_attendance_id: int):
    return course_attendance_repo.get_by_id(db, course_attendance_id)


def get_course_attendances_by_course(db: Session, course_id: int):
    return course_attendance_repo.get_by_course(db, course_id)
