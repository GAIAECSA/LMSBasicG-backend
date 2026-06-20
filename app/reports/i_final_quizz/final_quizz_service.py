from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .final_quizz_pdf import export_final_quizz_pdf
from .final_quizz_queries import (
    get_final_quizzes_headers,
    get_students_final_quizzes_matrix,
)
from .final_quizz_schemas import (
    FinalQuizzReportSchema,
    QuizzDetailSchema,
    QuizzHeaderSchema,
    StudentFinalRowSchema,
)


def generate_course_final_quizzes_pdf(
    db: Session,
    course_id: int,
    business_id: int,
    domain: str,
):
    # 1. Validar curso
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

    # 2. Columnas de Quizzes (count_towards_grade = True)
    quizz_blocks = get_final_quizzes_headers(
        db=db,
        course_id=course_id,
        business_id=business_id,
    )

    headers = []

    for b in quizz_blocks:
        title = f"Quiz {b.id}"

        if b.content:
            if isinstance(b.content, dict):
                title = b.content.get("title", title)
            elif isinstance(b.content, str):
                title = b.content

        headers.append(
            QuizzHeaderSchema(
                id=b.id,
                title=title,
            )
        )

    # 3. Datos crudos de la matriz
    raw_matrix = get_students_final_quizzes_matrix(
        db=db,
        course_id=course_id,
        business_id=business_id,
    )

    # 4. Agrupar por estudiante
    students_map = {}

    for row in raw_matrix:
        if row.student_id not in students_map:
            students_map[row.student_id] = {
                "name": row.student_name,
                "quizzes": {},
            }

        students_map[row.student_id]["quizzes"][row.block_id] = {
            "score": row.score,
            "is_passed": row.is_passed,
        }

    # 5. Estructurar filas y promedios
    report_rows = []

    for _, s_info in students_map.items():
        quizzes_results = []

        total_score_sum = 0.0
        attempts_count = 0

        for header in headers:
            attempt = s_info["quizzes"].get(header.id)

            if attempt and attempt["score"] is not None:
                float_score = float(attempt["score"])

                quizzes_results.append(
                    QuizzDetailSchema(
                        score=f"{float_score:.2f}",
                        is_passed=attempt["is_passed"],
                    )
                )

                total_score_sum += float_score
                attempts_count += 1

            else:
                quizzes_results.append(
                    QuizzDetailSchema(
                        score="Sin intentar",
                        is_passed=None,
                    )
                )

        average = total_score_sum / attempts_count if attempts_count > 0 else 0.0

        report_rows.append(
            StudentFinalRowSchema(
                student_name=s_info["name"],
                quizzes=quizzes_results,
                average=f"{average:.2f}",
            )
        )

    report_data = FinalQuizzReportSchema(
        course_id=course_id,
        course_name=course.name,
        headers=headers,
        rows=report_rows,
    )

    return export_final_quizz_pdf(
        report=report_data,
        domain=domain,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
