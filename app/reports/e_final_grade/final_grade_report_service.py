from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .final_grade_report_pdf import export_final_grade_report_pdf
from .final_grade_report_queries import get_evaluable_blocks, get_students_grades_matrix
from .final_grade_report_schemas import (
    BlockHeaderSchema,
    FinalGradeReportSchema,
    StudentGradeRowSchema,
)


def generate_course_final_grades_pdf(
    db: Session,
    course_id: int,
):
    # 1. Validar curso
    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.deleted.is_(False),
        )
        .first()
    )

    if not course:
        raise ValueError("Curso no encontrado")

    # 2. Obtener bloques evaluables
    evaluable_blocks = get_evaluable_blocks(
        db=db,
        course_id=course_id,
    )

    # 3. Construir headers de forma robusta
    headers = []

    for block in evaluable_blocks:
        title = f"Bloque {block.id}"

        try:
            if isinstance(block.content, dict):
                title = block.content.get(
                    "title",
                    f"Bloque {block.id}",
                )

            elif isinstance(block.content, str):
                title = block.content

            elif block.content is not None:
                title = str(block.content)

        except Exception:
            title = f"Bloque {block.id}"

        headers.append(
            BlockHeaderSchema(
                id=block.id,
                title=title,
            )
        )

    # 4. Obtener matriz plana de notas
    raw_matrix = get_students_grades_matrix(
        db=db,
        course_id=course_id,
    )

    # 5. Agrupar por estudiante
    students_data = {}

    for row in raw_matrix:
        if row.student_id not in students_data:
            students_data[row.student_id] = {
                "name": row.student_name,
                "grades_map": {},
            }

        students_data[row.student_id]["grades_map"][row.block_id] = row.score

    # 6. Construir filas del reporte
    report_rows = []
    total_blocks_count = len(headers)

    for student_id, student_info in students_data.items():
        grades = []
        total_score = 0.0

        for header in headers:
            score = student_info["grades_map"].get(header.id)

            if score is not None:
                score_float = float(score)

                grades.append(f"{score_float:.2f}")

                total_score += score_float
            else:
                grades.append("Sin entrega")

        average = total_score / total_blocks_count if total_blocks_count > 0 else 0.0

        status = "PASÓ" if average >= 7.0 else "NO PASÓ"

        report_rows.append(
            StudentGradeRowSchema(
                student_name=student_info["name"],
                grades=grades,
                average=f"{average:.2f}",
                status=status,
            )
        )

    # 7. Construir DTO final
    report_data = FinalGradeReportSchema(
        course_id=course_id,
        course_name=course.name,
        headers=headers,
        rows=report_rows,
    )

    # 8. Exportar PDF
    return export_final_grade_report_pdf(
        report=report_data,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
