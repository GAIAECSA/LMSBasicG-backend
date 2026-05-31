import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .professor_survey_report_pdf import export_professor_survey_report_pdf
from .professor_survey_report_queries import (
    get_course_professor_survey_responses_matrix,
    get_professor_survey_blocks_with_responses,
)
from .professor_survey_report_schemas import (
    CourseProfessorSurveyReportSchema,
    ProfessorQuestionHeaderSchema,
    ProfessorSurveyRowSchema,
    SingleProfessorSurveyMatrixSchema,
)


def _extract_numeric_score(value) -> float | None:
    """
    Parsea la respuesta Likert para extraer el valor numérico.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    match = re.match(r"^\s*(\d+(?:\.\d+)?)", str(value))
    if match:
        return float(match.group(1))
    return None


def generate_course_professor_surveys_pdf(db: Session, course_id: int):
    # 1. Validar curso
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.deleted.is_(False))
        .first()
    )
    if not course:
        raise ValueError("Curso no encontrado")

    # 2. Obtener bloques de encuestas contestadas por profesores
    survey_blocks = get_professor_survey_blocks_with_responses(
        db=db, course_id=course_id
    )
    if not survey_blocks:
        raise ValueError(
            "No se encontraron encuestas con respuestas de docentes en este curso"
        )

    # 3. Obtener matriz cruda de respuestas
    raw_matrix = get_course_professor_survey_responses_matrix(
        db=db, course_id=course_id
    )

    surveys_report_list = []

    for block in survey_blocks:
        block_responses = [r for r in raw_matrix if r.block_id == block.id]

        survey_title = "Encuesta Docente sin título"
        questions_list = []

        if block_responses and block_responses[0].survey_definition:
            survey_json = block_responses[0].survey_definition
            survey_title = (
                survey_json.get("title")
                or survey_json.get("name")
                or f"Encuesta Docente Bloque {block.id}"
            )
            questions_list = (
                survey_json.get("questions")
                or survey_json.get("survey_questions")
                or []
            )

        headers = [
            ProfessorQuestionHeaderSchema(
                id=q.get("id", idx + 1),
                label=f"P{idx + 1}",
                full_text=q.get("question", ""),
            )
            for idx, q in enumerate(questions_list)
        ]

        rows = []
        for res in block_responses:
            professor_answers = []

            # --- CORRECCIÓN AQUÍ: Entrar a la clave "answers" del formato JSON ---
            response_json = res.survey_answers or {}
            answers_payload = response_json.get("answers", {})
            # ---------------------------------------------------------------------

            total_score_sum = 0.0
            answered_questions_count = 0

            for h in headers:
                val = answers_payload.get(str(h.id)) or answers_payload.get(h.id)

                if val is not None:
                    professor_answers.append(str(val))
                    numeric_val = _extract_numeric_score(val)
                    if numeric_val is not None:
                        total_score_sum += numeric_val
                        answered_questions_count += 1
                else:
                    professor_answers.append("—")

            if answered_questions_count > 0:
                avg_value = total_score_sum / answered_questions_count
                average_str = f"{avg_value:.2f}"
            else:
                average_str = "0.00"

            rows.append(
                ProfessorSurveyRowSchema(
                    professor_name=res.professor_name,
                    answers=professor_answers,
                    average=average_str,
                )
            )

        surveys_report_list.append(
            SingleProfessorSurveyMatrixSchema(
                block_id=block.id, survey_title=survey_title, headers=headers, rows=rows
            )
        )

    report_data = CourseProfessorSurveyReportSchema(
        course_id=course_id, course_name=course.name, surveys=surveys_report_list
    )

    return export_professor_survey_report_pdf(
        report=report_data, generated_at=datetime.now().strftime("%d/%m/%Y %H:%M")
    )
