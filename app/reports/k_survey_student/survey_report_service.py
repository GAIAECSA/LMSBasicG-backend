import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .survey_report_pdf import export_survey_report_pdf
from .survey_report_queries import (
    get_course_survey_responses_matrix,
    get_survey_blocks_with_responses,
)
from .survey_report_schemas import (
    CourseSurveyReportSchema,
    QuestionHeaderSchema,
    SingleSurveyMatrixSchema,
    StudentSurveyRowSchema,
)


def _extract_numeric_score(value) -> float | None:
    """
    Helper para extraer el valor numérico de una respuesta Likert.
    Soporta tanto enteros/floats como cadenas del tipo '5 - Muy de acuerdo'.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    match = re.match(r"^\s*(\d+(?:\.\d+)?)", str(value))
    if match:
        return float(match.group(1))
    return None


def generate_course_surveys_pdf(db: Session, course_id: int):
    # 1. Validar curso
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.deleted.is_(False))
        .first()
    )
    if not course:
        raise ValueError("Curso no encontrado")

    # 2. Obtener los bloques de tipo encuesta activos
    survey_blocks = get_survey_blocks_with_responses(db=db, course_id=course_id)
    if not survey_blocks:
        raise ValueError("No se encontraron encuestas con respuestas en este curso")

    # 3. Obtener matriz de respuestas de los estudiantes
    raw_matrix = get_course_survey_responses_matrix(db=db, course_id=course_id)

    surveys_report_list = []

    for block in survey_blocks:
        block_responses = [r for r in raw_matrix if r.block_id == block.id]

        survey_title = "Encuesta sin título"
        questions_list = []

        if block_responses and block_responses[0].survey_definition:
            survey_json = block_responses[0].survey_definition
            survey_title = (
                survey_json.get("title")
                or survey_json.get("name")
                or f"Encuesta Bloque {block.id}"
            )
            questions_list = (
                survey_json.get("questions")
                or survey_json.get("survey_questions")
                or []
            )

        # Cabeceras dinámicas (P1, P2, P3...)
        headers = [
            QuestionHeaderSchema(
                id=q.get("id", idx + 1),
                label=f"P{idx + 1}",
                full_text=q.get("question", ""),
            )
            for idx, q in enumerate(questions_list)
        ]

        rows = []
        for res in block_responses:
            student_answers = []

            # --- CORRECCIÓN AQUÍ: Entrar a la clave "answers" del formato JSON ---
            response_json = res.survey_answers or {}
            answers_payload = response_json.get("answers", {})
            # ---------------------------------------------------------------------

            total_score_sum = 0.0
            answered_questions_count = 0

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
                avg_value = total_score_sum / answered_questions_count
                average_str = f"{avg_value:.2f}"
            else:
                average_str = "0.00"

            rows.append(
                StudentSurveyRowSchema(
                    student_name=res.student_name,
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
        course_id=course_id, course_name=course.name, surveys=surveys_report_list
    )

    return export_survey_report_pdf(
        report=report_data, generated_at=datetime.now().strftime("%d/%m/%Y %H:%M")
    )
