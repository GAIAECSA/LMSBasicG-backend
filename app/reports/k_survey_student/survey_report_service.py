import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .survey_report_pdf import export_survey_report_pdf
from .survey_report_queries import (
    get_enrollments_with_optional_survey_responses,
    get_survey_blocks_by_course,
)
from .survey_report_schemas import (
    CourseSurveyReportSchema,
    QuestionHeaderSchema,
    SingleSurveyMatrixSchema,
    StudentSurveyRowSchema,
)

STUDENT_ROLE_ID = 4


def _extract_numeric_score(value) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    match = re.match(r"^\s*(\d+(?:\.\d+)?)", str(value))
    if match:
        return float(match.group(1))
    return None


def generate_course_surveys_pdf(db: Session, course_id: int):
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.deleted.is_(False))
        .first()
    )
    course_name = course.name if course else f"Curso ID: {course_id}"

    # 1. Obtener todas las encuestas del curso estructuralmente
    survey_blocks = get_survey_blocks_by_course(db=db, course_id=course_id)
    surveys_report_list = []

    for block in survey_blocks:
        # 2. Obtener a todos los estudiantes (con o sin respuesta para este bloque)
        enrollments_responses = get_enrollments_with_optional_survey_responses(
            db=db, course_id=course_id, block_id=block.id, role_id=STUDENT_ROLE_ID
        )

        survey_title = f"Encuesta Bloque {block.id}"
        questions_list = []

        # 3. Buscar el primer registro que contenga la definición de la encuesta para armar los headers
        for r in enrollments_responses:
            if r.survey_definition:
                survey_title = (
                    r.survey_definition.get("title")
                    or r.survey_definition.get("name")
                    or survey_title
                )
                questions_list = (
                    r.survey_definition.get("questions")
                    or r.survey_definition.get("survey_questions")
                    or []
                )
                break

        # Construir headers dinámicos
        headers = [
            QuestionHeaderSchema(
                id=q.get("id", idx + 1),
                label=f"P{idx + 1}",
                full_text=q.get("question", ""),
            )
            for idx, q in enumerate(questions_list)
        ]

        # 4. Construir las filas para todos los matriculados
        rows = []
        for res in enrollments_responses:
            student_answers = []

            response_json = res.survey_answers or {}
            answers_payload = response_json.get("answers", {})

            total_score_sum = 0.0
            answered_questions_count = 0

            # Si la encuesta tiene preguntas mapeadas, buscamos el valor de cada una
            for h in headers:
                val = answers_payload.get(str(h.id)) or answers_payload.get(h.id)

                if val is not None:
                    student_answers.append(str(val))
                    numeric_val = _extract_numeric_score(val)
                    if numeric_val is not None:
                        total_score_sum += numeric_val
                        answered_questions_count += 1
                else:
                    student_answers.append("—")

            if answered_questions_count > 0:
                average_str = f"{(total_score_sum / answered_questions_count):.2f}"
            else:
                average_str = "0.00"

            rows.append(
                StudentSurveyRowSchema(
                    student_name=res.user_name,
                    answers=student_answers,
                    average=average_str,
                )
            )

        surveys_report_list.append(
            SingleSurveyMatrixSchema(
                block_id=block.id, survey_title=survey_title, headers=headers, rows=rows
            )
        )

    report_data = CourseSurveyReportSchema(
        course_id=course_id, course_name=course_name, surveys=surveys_report_list
    )

    return export_survey_report_pdf(
        report=report_data, generated_at=datetime.now().strftime("%d/%m/%Y %H:%M")
    )
