import logging
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

logger = logging.getLogger(__name__)

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
    logger.info(
        "[SURVEY_REPORT] ===== INICIO REPORTE CURSO %s =====",
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
        "[SURVEY_REPORT] Curso encontrado=%s",
        course is not None,
    )

    course_name = course.name if course else f"Curso ID: {course_id}"

    survey_blocks = get_survey_blocks_by_course(
        db=db,
        course_id=course_id,
    )

    logger.info(
        "[SURVEY_REPORT] Total bloques encuesta=%s",
        len(survey_blocks),
    )

    surveys_report_list = []

    for block in survey_blocks:
        logger.info(
            "[SURVEY_REPORT] Procesando block_id=%s",
            block.id,
        )

        enrollments_responses = get_enrollments_with_optional_survey_responses(
            db=db,
            course_id=course_id,
            block_id=block.id,
            role_id=STUDENT_ROLE_ID,
        )

        logger.info(
            "[SURVEY_REPORT] block_id=%s estudiantes=%s",
            block.id,
            len(enrollments_responses),
        )

        survey_definition = block.content or {}

        survey_title = (
            survey_definition.get("title")
            or survey_definition.get("name")
            or f"Encuesta Bloque {block.id}"
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

        logger.info(
            "[SURVEY_REPORT] Headers generados=%s",
            len(headers),
        )

        rows = []

        for res in enrollments_responses:
            logger.info(
                "[SURVEY_REPORT] Alumno=%s",
                res.user_name,
            )

            response_json = res.survey_answers or {}

            logger.info(
                "[SURVEY_REPORT] Respuesta=%s",
                response_json,
            )

            answers_payload = response_json.get("answers", {})

            logger.info(
                "[SURVEY_REPORT] Keys answers=%s",
                list(answers_payload.keys()),
            )

            student_answers = []
            total_score_sum = 0.0
            answered_questions_count = 0

            for h in headers:
                val = answers_payload.get(str(h.id)) or answers_payload.get(h.id)

                logger.info(
                    "[SURVEY_REPORT] Pregunta=%s valor=%s",
                    h.id,
                    val,
                )

                if val is not None:
                    numeric_val = _extract_numeric_score(val)

                    if numeric_val is not None:
                        student_answers.append(str(int(numeric_val)))
                        total_score_sum += numeric_val
                        answered_questions_count += 1
                    else:
                        student_answers.append(str(val))
                else:
                    student_answers.append("—")

            average_str = (
                f"{(total_score_sum / answered_questions_count):.2f}"
                if answered_questions_count > 0
                else "0.00"
            )

            rows.append(
                StudentSurveyRowSchema(
                    student_name=res.user_name,
                    answers=student_answers,
                    average=average_str,
                )
            )

        logger.info(
            "[SURVEY_REPORT] Filas generadas=%s",
            len(rows),
        )

        surveys_report_list.append(
            SingleSurveyMatrixSchema(
                block_id=block.id,
                survey_title=survey_title,
                headers=headers,
                rows=rows,
            )
        )

    logger.info(
        "[SURVEY_REPORT] Encuestas finales=%s",
        len(surveys_report_list),
    )

    report_data = CourseSurveyReportSchema(
        course_id=course_id,
        course_name=course_name,
        surveys=surveys_report_list,
    )

    logger.info("[SURVEY_REPORT] ===== FIN REPORTE =====")

    return export_survey_report_pdf(
        report=report_data,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
