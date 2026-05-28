from app.reports.attendance import attendance_report_queries, attendance_report_schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.reports.attendance import (
    attendance_report_service,
)
from app.utils.jwt import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/reports/courses/{course_id}/attendance/students",
    response_model=list[attendance_report_schemas.StudentAttendanceReport],
)
def get_course_student_attendance_report(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    try:

        return attendance_report_service.generate_course_student_attendance_report(
            db=db,
            course_id=course_id,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/reports/attendance/teachers",
    response_model=list[attendance_report_schemas.TeacherAttendanceReport],
)
def get_course_teacher_attendance_report(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    try:

        return attendance_report_service.generate_course_teacher_attendance_report(
            db=db,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
