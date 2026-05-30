import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .homework_graded_report_pdf import export_graded_homework_report_pdf
from .homework_graded_report_queries import get_all_graded_homeworks_matrix
from .homework_graded_report_schemas import GradedHomeworkReport, GradedHomeworkRow


def generate_course_graded_pdf(db: Session, course_id: int):
    # 1. Validar Curso
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.deleted.is_(False))
        .first()
    )
    if not course:
        raise ValueError("Curso no encontrado")

    # 2. Obtener matriz de datos plana
    rows = get_all_graded_homeworks_matrix(db=db, course_id=course_id)
    records_list = []

    for row in rows:
        has_submitted = row.response_id is not None
        formatted_date = None

        if has_submitted and row.submitted_at:
            formatted_date = row.submitted_at.strftime("%d/%m/%Y %H:%M")

        # Parsear de forma segura el título del LessonBlock desde el JSONB
        activity_title = "Tarea sin título"
        if isinstance(row.block_content, dict):
            activity_title = (
                row.block_content.get("title")
                or row.block_content.get("name")
                or "Tarea sin título"
            )
        elif isinstance(row.block_content, str):
            try:
                content_dict = json.loads(row.block_content)
                activity_title = (
                    content_dict.get("title")
                    or content_dict.get("name")
                    or "Tarea sin título"
                )
            except Exception:
                activity_title = row.block_content

        # Definir etiquetas de estado
        status_label = "Entregado" if has_submitted else "No entregado"

        records_list.append(
            GradedHomeworkRow(
                student_id=row.student_id,
                student_name=row.student_name,
                activity_title=activity_title,
                has_submitted=has_submitted,
                score=row.score if has_submitted else None,
                submitted_at=formatted_date,
                status_label=status_label,
            )
        )

    report_data = GradedHomeworkReport(
        course_id=course_id,
        course_name=course.name,
        records=records_list,
    )

    # 3. Renderizar PDF pasándole la plantilla correcta
    return export_graded_homework_report_pdf(
        report=report_data,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
