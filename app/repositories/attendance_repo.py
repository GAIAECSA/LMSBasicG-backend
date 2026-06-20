from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.course import Course
from app.models.course_attendance import CourseAttendance
from app.models.enrollment import Enrollment
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, attendance: Attendance) -> Attendance:
    db.add(attendance)
    db.flush()
    return attendance


def create_bulk(db: Session, attendances: list[Attendance]) -> list[Attendance]:
    db.add_all(attendances)
    db.flush()
    return attendances


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(db: Session, attendance_id: int, business_id: int) -> None:
    db.query(Attendance).filter(
        Attendance.id == attendance_id, Attendance.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_enrollment(
    db: Session, enrollment_id: int, business_id: int
) -> None:
    db.query(Attendance).filter(
        Attendance.enrollment_id == enrollment_id, Attendance.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_user(
    db: Session,
    user_id: int,
    business_id: int,
) -> None:
    (
        db.query(Attendance)
        .join(
            Enrollment,
            Attendance.enrollment_id == Enrollment.id,
        )
        .filter(
            Attendance.business_id == business_id,
            Attendance.deleted.is_(False),
            Enrollment.user_id == user_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_hard_by_enrollment(
    db: Session, enrollment_id: int, business_id: int
) -> None:
    db.query(Attendance).filter(
        Attendance.enrollment_id == enrollment_id, Attendance.business_id == business_id
    ).delete(synchronize_session=False)


def delete_soft_by_course_attendance(
    db: Session, course_attendance_id: int, business_id: int
) -> None:
    db.query(Attendance).filter(
        Attendance.course_attendance_id == course_attendance_id,
        Attendance.business_id == business_id,
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_course(db: Session, course_id: int, business_id: int) -> None:
    db.query(Attendance).filter(
        Attendance.business_id == business_id,
        Attendance.course_attendance_id.in_(
            db.query(CourseAttendance.id).filter(
                CourseAttendance.course_id == course_id,
                CourseAttendance.business_id == business_id,
            )
        ),
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_subcategory(
    db: Session, subcategory_id: int, business_id: int
) -> None:
    db.query(Attendance).filter(
        Attendance.business_id == business_id,
        Attendance.course_attendance_id.in_(
            db.query(CourseAttendance.id).filter(
                CourseAttendance.business_id == business_id,
                CourseAttendance.course_id.in_(
                    db.query(Course.id).filter(
                        Course.subcategory_id == subcategory_id,
                        Course.business_id == business_id,
                    )
                ),
            )
        ),
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_category(db: Session, category_id: int, business_id: int) -> None:
    db.query(Attendance).filter(
        Attendance.business_id == business_id,
        Attendance.course_attendance_id.in_(
            db.query(CourseAttendance.id).filter(
                CourseAttendance.business_id == business_id,
                CourseAttendance.course_id.in_(
                    db.query(Course.id).filter(
                        Course.business_id == business_id,
                        Course.subcategory_id.in_(
                            db.query(Subcategory.id).filter(
                                Subcategory.category_id == category_id,
                                Subcategory.business_id == business_id,
                            )
                        ),
                    )
                ),
            )
        ),
    ).update({"deleted": True}, synchronize_session=False)


# --- Consultas (Lectura) ---


def get_by_id(db: Session, attendance_id: int, business_id: int) -> Attendance | None:
    return (
        db.query(Attendance)
        .filter(
            Attendance.id == attendance_id,
            Attendance.business_id == business_id,
            Attendance.deleted.is_(False),
        )
        .first()
    )


def get_all_by_course_attendance(
    db: Session, course_attendance_id: int, business_id: int
) -> list[Attendance]:
    return (
        db.query(Attendance)
        .filter(
            Attendance.deleted.is_(False),
            Attendance.course_attendance_id == course_attendance_id,
            Attendance.business_id == business_id,
        )
        .all()
    )


def get_by_enrollment_and_course_attendance(
    db: Session, enrollment_id: int, course_attendance_id: int, business_id: int
) -> Attendance | None:
    return (
        db.query(Attendance)
        .filter(
            Attendance.deleted.is_(False),
            Attendance.course_attendance_id == course_attendance_id,
            Attendance.enrollment_id == enrollment_id,
            Attendance.business_id == business_id,
        )
        .first()
    )


def get_all_by_enrollment(
    db: Session, enrollment_id: int, business_id: int
) -> list[Attendance]:
    return (
        db.query(Attendance)
        .filter(
            Attendance.deleted.is_(False),
            Attendance.enrollment_id == enrollment_id,
            Attendance.business_id == business_id,
        )
        .all()
    )


# =====================================================================
# CÓDIGO ANTERIOR (VERSIÓN BÁSICA COMENTADA POR HISTORIAL)
# =====================================================================

# def create(db: Session, attendance: Attendance):
#     db.add(attendance)
#     db.commit()
#     db.refresh(attendance)
#     return attendance
#
# def update(db: Session, attendance: Attendance):
#     db.add(attendance)
#     db.commit()
#     db.refresh(attendance)
#     return attendance
#
# def delete(db: Session, attendance: Attendance):
#     attendance.deleted = True
#     db.add(attendance)
#     db.flush()
#     return attendance
#
# def soft_delete_by_enrollment(db: Session, enrollment_id: int):
#     db.query(Attendance).filter(Attendance.enrollment_id == enrollment_id).update(
#         {"deleted": True}
#     )
#
# def get_by_id(db: Session, attendance_id: int):
#     return (
#         db.query(Attendance)
#         .filter(Attendance.id == attendance_id, Attendance.deleted == False)
#         .first()
#     )
#
# def get_all_by_course_attendance(db: Session, course_attendance_id: int):
#     return (
#         db.query(Attendance)
#         .filter(
#             Attendance.deleted == False,
#             Attendance.course_attendance_id == course_attendance_id,
#         )
#         .all()
#     )
#
# def get_by_enrollment_and_course_attendance(
#     db: Session, enrollment_id: int, course_attendance_id: int
# ):
#     return (
#         db.query(Attendance)
#         .filter(
#             Attendance.deleted == False,
#             Attendance.course_attendance_id == course_attendance_id,
#             Attendance.enrollment_id == enrollment_id,
#         )
#         .first()
#     )
#
# def get_all_by_enrollment(db: Session, enrollment_id: int):
#     return (
#         db.query(Attendance)
#         .filter(
#             Attendance.deleted == False,
#             Attendance.enrollment_id == enrollment_id,
#         )
#         .all()
#     )
#
# # Metodos compuestos
#
# def create_many(db: Session, attendances: list[Attendance]):
#     db.add_all(attendances)
#     return attendances
