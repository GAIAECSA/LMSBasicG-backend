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


def generate_course_final_grades_pdf(db: Session, course_id: int):
    # 1. Validar curso
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.deleted.is_(False))
        .first()
    )
    if not course:
        raise ValueError("Curso no encontrado")

    # 2. Obtener headers (Columnas dinámicas)
    evaluable_blocks = get_evaluable_blocks(db=db, course_id=course_id)
    headers = [
        BlockHeaderSchema(id=b.id, title=b.content or f"Bloque {b.id}")
        for b in evaluable_blocks
    ]

    # 3. Obtener matriz plana de notas
    raw_matrix = get_students_grades_matrix(db=db, course_id=course_id)

    # 4. Agrupar por estudiante
    students_data = {}
    for row in raw_matrix:
        if row.student_id not in students_data:
            students_data[row.student_id] = {"name": row.student_name, "grades_map": {}}
        students_data[row.student_id]["grades_map"][row.block_id] = row.score

    # 5. Construir filas calculando promedio y estado
    report_rows = []
    total_blocks_count = len(headers)

    for s_id, s_info in students_data.items():
        student_grades = []
        total_score_sum = 0.0

        for header in headers:
            score = s_info["grades_map"].get(header.id)
            if score is not None:
                float_score = float(score)
                student_grades.append(f"{float_score:.2f}")
                total_score_sum += float_score
            else:
                student_grades.append("Sin entrega")
                # Nota: Una tarea no entregada suma 0.00 al promedio final

        # Cálculo de promedio sobre el total de bloques obligatorios del curso
        average = (
            total_score_sum / total_blocks_count if total_blocks_count > 0 else 0.0
        )
        status = "PASÓ" if average >= 7.00 else "NO PASÓ"

        report_rows.append(
            StudentGradeRowSchema(
                student_name=s_info["name"],
                grades=student_grades,
                average=f"{average:.2f}",
                status=status,
            )
        )

    report_data = FinalGradeReportSchema(
        course_id=course_id, course_name=course.name, headers=headers, rows=report_rows
    )

    return export_final_grade_report_pdf(
        report=report_data, generated_at=datetime.now().strftime("%d/%m/%Y %H:%M")
    )
