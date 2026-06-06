from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.course_attendance import CourseAttendance
from app.repositories import attendance_repo, course_attendance_repo, enrollment_repo
from app.schemas.course_attendance import CourseAttendanceCreate, CourseAttendanceUpdate


def create_course_attendance(db: Session, data: CourseAttendanceCreate):

    try:

        with db.begin():

            course_attendance = CourseAttendance(**data.model_dump())

            created = course_attendance_repo.create(db, course_attendance)

            enrollments = enrollment_repo.get_all_by_course_id(db, data.course_id)

            attendances = [
                Attendance(
                    enrollment_id=e.id,
                    course_attendance_id=created.id,
                    attendance_state="PENDIENTE",
                )
                for e in enrollments
            ]

            attendance_repo.create_many(db, attendances)

        return created

    except Exception as e:
        raise e


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
    print("¿Hay transacción activa ANTES de empezar?:", db.in_transaction())
    try:
        with db.begin():
            course_attendance = course_attendance_repo.get_by_id(
                db,
                course_attendance_id,
            )

            if not course_attendance:
                raise Exception("No encontrado")

            for student_attendance in course_attendance.attendance:
                attendance_repo.delete(db, student_attendance)

            course_attendance_repo.delete(db, course_attendance)

        return True

    except Exception as e:
        raise e


def get_course_attendance(db: Session, course_attendance_id: int):
    return course_attendance_repo.get_by_id(db, course_attendance_id)


def get_course_attendances_by_course(db: Session, course_id: int):
    return course_attendance_repo.get_by_course(db, course_id)
