import json
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.course import Course

from .homework_graded_report_pdf import export_graded_homework_report_pdf
from .homework_graded_report_queries import get_all_graded_homeworks_matrix
from .homework_graded_report_schemas import (
    HomeworkCellSchema,
    HomeworkHeaderSchema,
    HomeworkMatrixReportSchema,
    StudentHomeworkRowSchema,
)


def extract_title(content):
    if isinstance(content, dict):
        return content.get("title") or content.get("name") or "Tarea sin título"

    if isinstance(content, str):
        try:
            data = json.loads(content)
            return data.get("title") or data.get("name") or "Tarea sin título"
        except Exception:
            return content

    return "Tarea sin título"


def generate_course_graded_pdf(
    db: Session,
    course_id: int,
):
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

    rows = get_all_graded_homeworks_matrix(
        db=db,
        course_id=course_id,
    )

    headers_dict = OrderedDict()

    for row in rows:
        if row.block_id not in headers_dict:
            headers_dict[row.block_id] = HomeworkHeaderSchema(
                id=row.block_id,
                title=extract_title(row.block_content),
            )

    headers = list(headers_dict.values())

    students = OrderedDict()

    for row in rows:

        if row.student_id not in students:
            students[row.student_id] = {
                "student_name": row.student_name,
                "scores": {},
            }

        if row.response_id:

            score_value = str(row.score) if row.score is not None else "0"

            students[row.student_id]["scores"][row.block_id] = score_value

    report_rows = []

    for _, student_data in students.items():

        cells = []

        numeric_scores = []

        for header in headers:

            score = student_data["scores"].get(header.id)

            if score is None:

                cells.append(
                    HomeworkCellSchema(
                        score="No entregado",
                        submitted=False,
                    )
                )

            else:

                cells.append(
                    HomeworkCellSchema(
                        score=score,
                        submitted=True,
                    )
                )

                try:
                    numeric_scores.append(Decimal(score))
                except Exception:
                    pass

        average = "0"

        if numeric_scores:
            average = str(
                round(
                    sum(numeric_scores) / len(numeric_scores),
                    2,
                )
            )

        report_rows.append(
            StudentHomeworkRowSchema(
                student_name=student_data["student_name"],
                homeworks=cells,
                average=average,
            )
        )

    report = HomeworkMatrixReportSchema(
        course_id=course.id,
        course_name=course.name,
        headers=headers,
        rows=report_rows,
    )

    return export_graded_homework_report_pdf(
        report=report,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
