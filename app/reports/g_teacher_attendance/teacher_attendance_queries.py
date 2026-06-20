from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.course_attendance import CourseAttendance
from app.models.enrollment import Enrollment
from app.models.user import User

TEACHER_ROLE_ID = 3


def get_teacher_attendance_report_data(db: Session, course_id: int, business_id: int):
    """
    Recupera todas las sesiones de asistencia programadas para un curso
    junto con el estado de asistencia marcado para el docente.
    """
    return (
        db.query(
            CourseAttendance.day.label("date"),
            CourseAttendance.start_time.label("start_time"),
            CourseAttendance.end_time.label("end_time"),
            Attendance.attendance_state.label("status"),
            User.firstname.label("teacher_firstname"),
            User.lastname.label("teacher_lastname"),
        )
        .select_from(CourseAttendance)
        .join(
            Attendance,
            and_(
                Attendance.course_attendance_id == CourseAttendance.id,
                Attendance.business_id == business_id,
                Attendance.deleted.is_(False),
            ),
        )
        .join(
            Enrollment,
            and_(
                Enrollment.id == Attendance.enrollment_id,
                Enrollment.course_id == course_id,
                Enrollment.business_id == business_id,
                Enrollment.role_id == TEACHER_ROLE_ID,
                Enrollment.deleted.is_(False),
            ),
        )
        .join(
            User,
            and_(
                User.id == Enrollment.user_id,
                User.business_id == business_id,
                User.deleted.is_(False),
            ),
        )
        .filter(
            CourseAttendance.course_id == course_id,
            CourseAttendance.business_id == business_id,
            CourseAttendance.deleted.is_(False),
        )
        .order_by(
            CourseAttendance.day.asc(),
            CourseAttendance.start_time.asc(),
        )
        .all()
    )
