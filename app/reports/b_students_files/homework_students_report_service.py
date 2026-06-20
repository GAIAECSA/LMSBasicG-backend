from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .homework_students_report_pdf import export_homework_report_pdf
from .homework_students_report_queries import (
    get_homework_block_id_by_title,
    get_students_homework_submissions,
)
from .homework_students_report_schemas import (
    HomeworkStudentsReport,
    StudentHomeworkSubmission,
)


def generate_homework_students_report(
    db: Session,
    course_id: int,
    title: str,
    business_id: int,
    domain: str,
):
    # 1. Validar la existencia del curso
    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.deleted.is_(False),
            Course.business_id == business_id,
        )
        .first()
    )

    if not course:
        raise ValueError("Curso no encontrado")

    # 2. Obtener la información estructurada pasándole el título dinámico
    report_data = format_homework_report_data(
        db=db,
        course_id=course_id,
        course_name=course.name,
        title=title,
        business_id=business_id,
    )

    # 3. Compilar a formato PDF binario
    pdf = export_homework_report_pdf(
        domain=domain,
        report=report_data,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )

    return pdf


def format_homework_report_data(
    db: Session,
    course_id: int,
    course_name: str,
    title: str,
    business_id: int,
) -> HomeworkStudentsReport:
    # Buscar el bloque usando el título dinámico mandado desde el Router
    lesson_block_id = get_homework_block_id_by_title(
        db=db,
        course_id=course_id,
        title=title,
        business_id=business_id,
    )

    rows = get_students_homework_submissions(
        db=db,
        course_id=course_id,
        lesson_block_id=lesson_block_id,
        business_id=business_id,
    )

    students_list = []

    for row in rows:
        has_submitted = row.response_id is not None
        formatted_date = None

        if has_submitted and row.submitted_at:
            formatted_date = row.submitted_at.strftime("%d/%m/%Y %H:%M")

        # Mapeo amigable de etiquetas de estado
        status_label = "No entregado"
        if has_submitted:
            status_label = (
                "Entregado"
                if row.submission_status == "submitted"
                else str(row.submission_status or "Entregado")
            )

        students_list.append(
            StudentHomeworkSubmission(
                student_id=row.student_id,
                student_name=row.student_name,
                has_submitted=has_submitted,
                submitted_at=formatted_date,
                status_label=status_label,
            )
        )

    return HomeworkStudentsReport(
        course_id=course_id,
        course_name=course_name,
        activity_title=title,
        students=students_list,
    )
