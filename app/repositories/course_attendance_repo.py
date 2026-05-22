from sqlalchemy.orm import Session
from app.models.course_attendance import CourseAttendance


def update(db: Session, course_attendance: CourseAttendance):
    db.merge(course_attendance)
    db.commit()
    db.refresh(course_attendance)
    return course_attendance


def delete(db: Session, course_attendance: CourseAttendance):
    course_attendance.deleted = True
    db.merge(course_attendance)
    db.commit()
    return course_attendance


def get_by_id(db: Session, certificate_id: int):
    return (
        db.query(CourseAttendance)
        .filter(
            CourseAttendance.id == certificate_id, CourseAttendance.deleted == False
        )
        .first()
    )


def get_by_course(db: Session, course_id: int):
    return (
        db.query(CourseAttendance)
        .filter(
            CourseAttendance.course_id == course_id, CourseAttendance.deleted == False
        )
        .all()
    )


# Metodos compuestos


def create(db: Session, course_attendance: CourseAttendance):
    db.add(course_attendance)
    db.flush()
    return course_attendance
