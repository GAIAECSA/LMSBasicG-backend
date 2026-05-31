from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.reports.a_course_structure import course_structure_report_service
from app.reports.b_students_files import homework_students_report_service
from app.reports.c_student_attendance import student_attendance_report_service
from app.reports.d_practice_lesson import homework_graded_report_service
from app.reports.e_final_grade import final_grade_report_service
from app.reports.g_teacher_attendance.teacher_attendance_service import (
    generate_teacher_attendance_pdf,
)
from app.reports.teacher import teacher_attendance_report_service
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


# 7 Reporte de prueba práctica por curso


@router.get("/reports/practice/lessons/pdf")
def export_practice_lesson_report(
    course_id: int,
    db: Session = Depends(get_db),
):

    pdf = homework_graded_report_service.generate_course_graded_pdf(
        db=db, course_id=course_id
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="practice_lesson_report.pdf"'
        },
    )


# 8 Registro notas finales


@router.get("/reports/final/grades/pdf")
def export_final_grades_report(
    course_id: int,
    db: Session = Depends(get_db),
):

    pdf = final_grade_report_service.generate_course_final_grades_pdf(
        db=db, course_id=course_id
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="final_grades_report.pdf"'
        },
    )


# 9 Petición encuesta

# 10 Reporte de asistencia del profesor


@router.get("/reports/teacher/attendance/pdf")
def export_teacher_attendance_pdf(
    course_id: int,
    db: Session = Depends(get_db),
):
    try:
        pdf = generate_teacher_attendance_pdf(db=db, course_id=course_id)

        filename = f"reporte_asistencia_docente_curso_{course_id}.pdf"

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al generar el reporte de asistencia: {str(e)}",
        )


# 11 Encuesta satisfacción estudiante

# 12 Encuesta satisfacción docente

# 13 Evaluación diagnóstica

# 14 Evaluacion final teórica

# 15 Reporte de descargas certificado
