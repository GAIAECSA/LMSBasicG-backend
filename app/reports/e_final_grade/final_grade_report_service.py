from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .final_grade_report_pdf import export_final_grade_report_pdf
from .final_grade_report_queries import (
    get_course_students,
    get_evaluable_blocks,
    get_homework_scores,
    get_quizz_scores,
)
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

    # 2. Obtener bloques evaluables (Headers)
    evaluable_blocks = get_evaluable_blocks(db=db, course_id=course_id)

    headers = []
    for block in evaluable_blocks:
        title = f"Bloque {block.id}"
        try:
            if isinstance(block.content, dict):
                title = block.content.get("title", f"Bloque {block.id}")
            elif isinstance(block.content, str):
                title = block.content
            elif block.content is not None:
                title = str(block.content)
        except Exception:
            pass

        headers.append(
            BlockHeaderSchema(
                id=block.id,
                title=title,
            )
        )

    # 3. Obtener Estudiantes (Filas)
    students = get_course_students(db=db, course_id=course_id)

    # 4. Obtener Notas y armar mapa en memoria: mapa[enrollment_id][block_id] = score
    hw_scores = get_homework_scores(db=db, course_id=course_id)
    qz_scores = get_quizz_scores(db=db, course_id=course_id)

    scores_map = {student.enrollment_id: {} for student in students}

    for hw in hw_scores:
        if hw.enrollment_id in scores_map:
            scores_map[hw.enrollment_id][hw.lesson_block_id] = hw.score

    for qz in qz_scores:
        if qz.enrollment_id in scores_map:
            scores_map[qz.enrollment_id][qz.lesson_block_id] = qz.score

    # 5. Construir filas del reporte evaluando condiciones de entrega
    report_rows = []
    total_blocks_count = len(headers)

    for student in students:
        grades = []
        total_score = 0.0
        student_scores = scores_map[student.enrollment_id]

        for block in evaluable_blocks:
            if block.id not in student_scores:
                # No existe el registro en HomeworkResponse ni QuizzResponse
                grades.append("No entregado")
            else:
                score = student_scores[block.id]
                if score is None:
                    # Existe el registro pero el campo score es nulo
                    grades.append("Sin calificación")
                else:
                    # Tiene calificación
                    score_float = float(score)
                    grades.append(f"{score_float:.2f}")
                    total_score += score_float

        average = total_score / total_blocks_count if total_blocks_count > 0 else 0.0
        status = "PASÓ" if average >= 7.0 else "NO PASÓ"

        report_rows.append(
            StudentGradeRowSchema(
                student_name=student.student_name,
                grades=grades,
                average=f"{average:.2f}",
                status=status,
            )
        )

    # 6. Construir DTO final
    report_data = FinalGradeReportSchema(
        course_id=course_id,
        course_name=course.name,
        headers=headers,
        rows=report_rows,
    )

    # 7. Exportar PDF
    return export_final_grade_report_pdf(
        report=report_data,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
