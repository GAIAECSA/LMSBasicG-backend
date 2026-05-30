from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.reports.attendance.student import student_attendance_report_service
from app.reports.attendance.teacher import teacher_attendance_report_service
from app.reports.a_course_structure import course_structure_report_service
from app.utils.jwt import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Reporte 1 Estructura del curso


@router.get("/reports/courses/structure/pdf")
def export_course_structure_pdf(
    course_id: int,
    db: Session = Depends(get_db),
):
    try:
        pdf_content = course_structure_report_service.generate_course_structure_report(
            db=db,
            course_id=course_id,
        )

        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="course_structure_{course_id}.pdf"'
            },
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get(
    "/reports/courses/{course_id}/attendance/students/pdf",
)
def export_course_student_attendance_pdf(
    course_id: int,
    db: Session = Depends(get_db),
):

    try:

        pdf = student_attendance_report_service.generate_student_attendance_pdf(
            db=db,
            course_id=course_id,
        )

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="attendance_course_{course_id}.pdf"'
            },
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/reports/attendance/teachers/pdf")
def export_teacher_attendance_report(
    db: Session = Depends(get_db),
):

    pdf = teacher_attendance_report_service.generate_teacher_attendance_pdf(
        db=db,
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="teacher_attendance_report.pdf"'
        },
    )
