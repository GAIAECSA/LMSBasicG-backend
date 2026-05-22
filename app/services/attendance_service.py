from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.repositories import attendance_repo
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


def create_attendance(db: Session, data: AttendanceCreate):
    existing = attendance_repo.get_by_enrollment_and_course_attendance(
        db, data.enrollment_id, data.course_attendance_id
    )
    if existing:
        raise Exception("La asistencia ya existe para este estudiante")
    attendance = Attendance(**data.model_dump())

    return attendance_repo.create(db, attendance)


def update_attendance(db: Session, attendance_id: int, data: AttendanceUpdate):
    attendance = attendance_repo.get_by_id(db, attendance_id)

    if not attendance:
        raise Exception("Asistencia no encontrada")

    update_data = data.model_dump(exclude_unset=True)
    enrollment_id = update_data.get("enrollment_id", attendance.enrollment_id)
    course_attendance_id = update_data.get(
        "course_attendance_id", attendance.course_attendance_id
    )

    existing = attendance_repo.get_by_enrollment_and_course_attendance(
        db, enrollment_id, course_attendance_id
    )
    if existing and existing.id != attendance.id:
        raise Exception("Ya existe una asistencia para este estudiante")

    for key, value in update_data.items():
        setattr(attendance, key, value)

    return attendance_repo.update(db, attendance)


def delete_attendance(db: Session, attendance_id: int):
    attendance = attendance_repo.get_by_id(db, attendance_id)

    if not attendance:
        raise Exception("Asistencia no encontrada")

    return attendance_repo.delete(db, attendance)


def get_attendance(db: Session, attendance_id: int):
    attendance = attendance_repo.get_by_id(db, attendance_id)

    if not attendance:
        raise Exception("Asistencia no encontrada")

    return attendance


def get_all_attendance_by_course_attendance(db: Session, course_attendance_id: int):
    return attendance_repo.get_all_by_course_attendance(db, course_attendance_id)

def get_all_attendance_by_enrollment(db: Session, enrollment_id: int):
    return attendance_repo.get_all_by_enrollment(db, enrollment_id)