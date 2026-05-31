from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
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
from app.reports.h_diagnostic_quizz.practice_quizz_service import (
    generate_course_practice_quizzes_pdf,
)
from app.reports.i_final_quizz.final_quizz_service import (
    generate_course_final_quizzes_pdf,
)
from app.reports.j_mdt_certificate import mdt_report_service
from app.reports.k_survey_student import survey_report_service
from app.reports.l_survey_teacher import professor_survey_report_service
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


@router.get("/students")
def get_student_surveys_report(
    course_id: int = Query(
        ..., gt=0, description="ID del curso para el reporte de estudiantes"
    ),
    db: Session = Depends(get_db),
):
    """
    Descarga el reporte en PDF de la matriz de respuestas de los ESTUDIANTES
    a todas las encuestas del curso especificado.
    """
    try:
        pdf_bytes = survey_report_service.generate_course_surveys_pdf(
            db=db, course_id=course_id
        )

        filename = f"reporte_encuestas_estudiantes_curso_{course_id}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al exportar el reporte de estudiantes: {str(e)}",
        )


# 12 Encuesta satisfacción docente


@router.get("/professors")
def get_professor_surveys_report(
    course_id: int = Query(
        ..., gt=0, description="ID del curso para el reporte de profesores"
    ),
    db: Session = Depends(get_db),
):
    """
    Descarga el reporte en PDF de la matriz de respuestas de los PROFESORES/DOCENTES
    a todas las encuestas del curso especificado.
    """
    try:
        pdf_bytes = (
            professor_survey_report_service.generate_course_professor_surveys_pdf(
                db=db, course_id=course_id
            )
        )

        filename = f"reporte_encuestas_profesores_curso_{course_id}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al exportar el reporte de profesores: {str(e)}",
        )


# 13 Evaluación diagnóstica


@router.get("/reports/practice/quizz/pdf")
def export_practice_quizz_pdf(
    course_id: int,
    db: Session = Depends(get_db),
):
    try:
        pdf = generate_course_practice_quizzes_pdf(db=db, course_id=course_id)

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


# 14 Evaluacion final teórica


@router.get("/reports/final/quizz/pdf")
def export_final_quizz_pdf(
    course_id: int,
    db: Session = Depends(get_db),
):
    try:
        pdf = generate_course_final_quizzes_pdf(db=db, course_id=course_id)

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


# 15 Reporte de descargas certificado


@router.get("/mdt-certificates")
def get_mdt_certificates_report(
    course_id: int = Query(..., gt=0, description="ID del curso a auditar"),
    certificate_type: Literal["MDT", "INSTITUTIONAL"] = Query(
        ..., description="Tipo de certificado a filtrar"
    ),
    db: Session = Depends(get_db),
):

    try:
        # 1. Invocar al servicio para generar el binario del PDF
        pdf_bytes = mdt_report_service.generate_mdt_certificates_report_pdf(
            db=db,
            course_id=course_id,
            certificate_type=certificate_type,
        )

        # 2. Sanitizar y estructurar el nombre del archivo de salida
        filename = f"reporte_descargas_{certificate_type.lower()}_curso_{course_id}.pdf"

        # 3. Retornar el archivo binario directamente al cliente
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )

    except ValueError as e:
        # Captura el error si el curso no existe
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al procesar la exportación del PDF: {str(e)}",
        )
