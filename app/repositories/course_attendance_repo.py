from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.course_attendance import CourseAttendance
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, course_attendance: CourseAttendance):
    db.add(course_attendance)
    db.flush()
    return course_attendance


def create_bulk(db: Session, course_attendances: list[CourseAttendance]):
    db.add_all(course_attendances)
    db.flush()
    return course_attendances


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(db: Session, course_attendance_id: int):
    db.query(CourseAttendance).filter(
        CourseAttendance.id == course_attendance_id
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_course(db: Session, course_id: int):
    db.query(CourseAttendance).filter(CourseAttendance.course_id == course_id).update(
        {"deleted": True}, synchronize_session=False
    )


def delete_soft_by_subcategory(db: Session, subcategory_id: int) -> None:
    db.query(CourseAttendance).filter(
        CourseAttendance.course_id.in_(
            db.query(Course.id).filter(Course.subcategory_id == subcategory_id)
        )
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_category(db: Session, category_id: int) -> None:
    db.query(CourseAttendance).filter(
        CourseAttendance.course_id.in_(
            db.query(Course.id).filter(
                Course.subcategory_id.in_(
                    db.query(Subcategory.id).filter(
                        Subcategory.category_id == category_id
                    )
                )
            )
        )
    ).update({"deleted": True}, synchronize_session=False)


# --- Consultas (Lectura) ---


def get_by_id(db: Session, course_attendance_id: int):
    return (
        db.query(CourseAttendance)
        .filter(
            CourseAttendance.id == course_attendance_id,
            CourseAttendance.deleted == False,
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


# Viejitos
# def update(db: Session, course_attendance: CourseAttendance):
#   db.merge(course_attendance)
#  db.commit()
# db.refresh(course_attendance)
# return course_attendance


# def delete(db: Session, course_attendance: CourseAttendance):
#   course_attendance.deleted = True
#  db.add(course_attendance)
# db.flush()
# return course_attendance


# def get_by_id(db: Session, course_attendance_id: int):
#   return (
#      db.query(CourseAttendance)
#     .filter(
#        CourseAttendance.id == course_attendance_id,
#       CourseAttendance.deleted == False,
#  )
# .first()
# )


# def get_by_course(db: Session, course_id: int):
#   return (
#      db.query(CourseAttendance)
#     .filter(
#        CourseAttendance.course_id == course_id, CourseAttendance.deleted == False
#   )
#  .all()
# )


# Metodos compuestos


# def create(db: Session, course_attendance: CourseAttendance):
#   db.add(course_attendance)
#  db.flush()
# return course_attendance
