import logging
import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

# Importaciones internas corregidas apuntando a los nuevos nombres de archivo
from .professor_survey_report_pdf import export_professor_survey_report_pdf
from .professor_survey_report_queries import (
    get_enrollments_with_optional_survey_responses,
    get_survey_blocks_by_course,
)
from .professor_survey_report_schemas import (
    ProfessorCourseSurveyReportSchema,
    ProfessorSurveyMatrixSchema,
    ProfessorSurveyRowSchema,
    QuestionHeaderSchema,
)

logger = logging.getLogger(__name__)

# ID del rol correspondiente a los profesores en tu sistema
PROFESSOR_ROLE_ID = 3


def _extract_numeric_score(value) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    match = re.match(r"^\s*(\d+(?:\.\d+)?)", str(value))
    if match:
        return float(match.group(1))
    return None


def generate_professor_surveys_pdf(db: Session, course_id: int):
    logger.info(
        "[PROFESSOR_SURVEY_REPORT] ===== INICIO REPORTE DOCENTE CURSO %s =====",
        course_id,
    )

    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.deleted.is_(False),
        )
        .first()
    )

    logger.info(
        "[PROFESSOR_SURVEY_REPORT] Curso encontrado=%s",
        course is not None,
    )

    course_name = course.name if course else f"Curso ID: {course_id}"

    survey_blocks = get_survey_blocks_by_course(
        db=db,
        course_id=course_id,
    )

    logger.info(
        "[PROFESSOR_SURVEY_REPORT] Total bloques encuesta=%s",
        len(survey_blocks),
    )

    surveys_report_list = []

    for block in survey_blocks:
        logger.info(
            "[PROFESSOR_SURVEY_REPORT] Procesando block_id=%s",
            block.id,
        )

        enrollments_responses = get_enrollments_with_optional_survey_responses(
            db=db,
            course_id=course_id,
            block_id=block.id,
            role_id=PROFESSOR_ROLE_ID,
        )

        logger.info(
            "[PROFESSOR_SURVEY_REPORT] block_id=%s docentes=%s",
            block.id,
            len(enrollments_responses),
        )

        survey_definition = block.content or {}

        survey_title = (
            survey_definition.get("title")
            or survey_definition.get("name")
            or f"Encuesta Docente Bloque {block.id}"
        )

        questions_list = (
            survey_definition.get("questions")
            or survey_definition.get("survey_questions")
            or []
        )

        headers = [
            QuestionHeaderSchema(
                id=q.get("id", idx + 1),
                label=f"P{idx + 1}",
                full_text=q.get("question", ""),
            )
            for idx, q in enumerate(questions_list)
        ]

        rows = []

        for res in enrollments_responses:
            logger.info(
                "[PROFESSOR_SURVEY_REPORT] Docente=%s",
                res.user_name,
            )

            response_json = res.survey_answers or {}
            answers_payload = response_json.get("answers", {})

            professor_answers = []
            total_score_sum = 0.0
            answered_questions_count = 0

            for h in headers:
                val = answers_payload.get(str(h.id)) or answers_payload.get(h.id)

                if val is not None:
                    numeric_val = _extract_numeric_score(val)

                    if numeric_val is not None:
                        professor_answers.append(str(int(numeric_val)))
                        total_score_sum += numeric_val
                        answered_questions_count += 1
                    else:
                        professor_answers.append(str(val))
                else:
                    professor_answers.append("—")

            average_str = (
                f"{(total_score_sum / answered_questions_count):.2f}"
                if answered_questions_count > 0
                else "0.00"
            )

            rows.append(
                ProfessorSurveyRowSchema(
                    professor_name=res.user_name,
                    answers=professor_answers,
                    average=average_str,
                )
            )

        surveys_report_list.append(
            ProfessorSurveyMatrixSchema(
                block_id=block.id,
                survey_title=survey_title,
                headers=headers,
                rows=rows,
            )
        )

    report_data = ProfessorCourseSurveyReportSchema(
        course_id=course_id,
        course_name=course_name,
        surveys=surveys_report_list,
    )

    logger.info("[PROFESSOR_SURVEY_REPORT] ===== FIN REPORTE =====")

    return export_professor_survey_report_pdf(
        report=report_data,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
