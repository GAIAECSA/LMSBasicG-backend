from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User


def get_course_teacher_attendance_report(
    db: Session,
):

    query = (
        db.query(
            Course.id.label("course_id"),
            Course.name.label("course_name"),
            User.id.label("teacher_id"),
            func.concat(
                User.firstname,
                " ",
                User.lastname,
            ).label("teacher_name"),
            func.count(Attendance.id).label("total_attendances"),
            func.sum(
                case(
                    (
                        Attendance.attendance_state == "PRESENTE",
                        1,
                    ),
                    else_=0,
                )
            ).label("present_count"),
            func.sum(
                case(
                    (
                        Attendance.attendance_state == "AUSENTE",
                        1,
                    ),
                    else_=0,
                )
            ).label("absent_count"),
            func.sum(
                case(
                    (
                        Attendance.attendance_state == "PENDIENTE",
                        1,
                    ),
                    else_=0,
                )
            ).label("pending_count"),
        )
        .join(
            Enrollment,
            Enrollment.id == Attendance.enrollment_id,
        )
        .join(
            User,
            User.id == Enrollment.user_id,
        )
        .join(
            Course,
            Course.id == Enrollment.course_id,
        )
        .filter(
            Enrollment.role_id == 3,
            Enrollment.deleted == False,
            Attendance.deleted == False,
            User.deleted == False,
            Course.deleted == False,
        )
        .group_by(
            Course.id,
            Course.name,
            User.id,
            User.firstname,
            User.lastname,
        )
        .order_by(
            Course.name.asc(),
            User.lastname.asc(),
        )
    )

    return query.all()
