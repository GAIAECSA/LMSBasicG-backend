from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.reports.a_course_structure import course_structure_report_service
from app.reports.b_students_files import homework_students_report_service
from app.reports.c_attendance.student import student_attendance_report_service
from app.reports.c_attendance.teacher import teacher_attendance_report_service
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


# 2 Copia Titulo


@router.get("/reports/degree/students/pdf")
def export_degree_students_pdf(
    course_id: int,
    db: Session = Depends(get_db),
):
    try:
        pdf_content = (
            homework_students_report_service.generate_homework_students_report(
                db=db, course_id=course_id, title="Copia Título"
            )
        )

        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="degree_students_{course_id}.pdf"'
            },
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


# 3 Copia certificado laboral


@router.get("/reports/certificate/students/pdf")
def export_certificate_students_pdf(
    course_id: int,
    db: Session = Depends(get_db),
):
    try:
        pdf_content = (
            homework_students_report_service.generate_homework_students_report(
                db=db, course_id=course_id, title="Copia de Certificado Laboral"
            )
        )

        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="certificate_students_{course_id}.pdf"'
            },
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


# 4 Copia Cédula


@router.get("/reports/idnumber/students/pdf")
def export_idnumber_students_pdf(
    course_id: int,
    db: Session = Depends(get_db),
):
    try:
        pdf_content = (
            homework_students_report_service.generate_homework_students_report(
                db=db, course_id=course_id, title="Copia Cédula"
            )
        )

        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="idnumber_students_{course_id}.pdf"'
            },
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


# 5 Comprobante de pago


@router.get("/reports/payment/students/pdf")
def export_payment_students_pdf(
    course_id: int,
    db: Session = Depends(get_db),
):
    try:
        pdf_content = (
            homework_students_report_service.generate_homework_students_report(
                db=db, course_id=course_id, title="Comprobante de pago"
            )
        )

        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="payment_students_{course_id}.pdf"'
            },
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


# 6 Reporte de asistencia de estudiantes


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
