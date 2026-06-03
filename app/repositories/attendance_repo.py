from sqlalchemy.orm import Session

from app.models.attendance import Attendance


def create(db: Session, attendance: Attendance):
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


def update(db: Session, attendance: Attendance):
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


def delete(db: Session, attendance: Attendance):
    attendance.deleted = True
    db.add(attendance)
    db.flush()
    return attendance


def get_by_id(db: Session, attendance_id: int):
    return (
        db.query(Attendance)
        .filter(Attendance.id == attendance_id, Attendance.deleted == False)
        .first()
    )


def get_all_by_course_attendance(db: Session, course_attendance_id: int):
    return (
        db.query(Attendance)
        .filter(
            Attendance.deleted == False,
            Attendance.course_attendance_id == course_attendance_id,
        )
        .all()
    )


def get_by_enrollment_and_course_attendance(
    db: Session, enrollment_id: int, course_attendance_id: int
):
    return (
        db.query(Attendance)
        .filter(
            Attendance.deleted == False,
            Attendance.course_attendance_id == course_attendance_id,
            Attendance.enrollment_id == enrollment_id,
        )
        .first()
    )


def get_all_by_enrollment(db: Session, enrollment_id: int):
    return (
        db.query(Attendance)
        .filter(
            Attendance.deleted == False,
            Attendance.enrollment_id == enrollment_id,
        )
        .all()
    )


# Metodos compuestos


def create_many(db: Session, attendances: list[Attendance]):
    db.add_all(attendances)
    return attendances
