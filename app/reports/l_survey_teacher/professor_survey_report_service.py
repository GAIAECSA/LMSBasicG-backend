import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .professor_survey_report_pdf import export_professor_survey_report_pdf
from .professor_survey_report_queries import (
    get_professor_enrollments_with_optional_responses,
    get_professor_survey_blocks_by_course,
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
    Soporta enteros, floats y cadenas formateadas como '5 - Muy de acuerdo'.
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
    """
    Genera el PDF del reporte de encuestas de profesores garantizando
    que aparezcan TODOS los docentes matriculados en el curso.
    """
    # 1. Obtener información básica del curso (Fallback elegante si no existe)
    course = (
        db.query(Course).filter(Course.id == course_id, Course.deleted == False).first()
    )
    course_name = course.name if course else f"Curso ID: {course_id}"

    # 2. Obtener la lista de todos los bloques de tipo encuesta (block_type_id = 7)
    survey_blocks = get_professor_survey_blocks_by_course(db=db, course_id=course_id)
    surveys_report_list = []

    for block in survey_blocks:
        # 3. Obtener todos los profesores matriculados (vía LEFT JOIN con sus respuestas)
        enrollments_responses = get_professor_enrollments_with_optional_responses(
            db=db, course_id=course_id, block_id=block.id
        )

        survey_title = f"Encuesta Docente Bloque {block.id}"
        questions_list = []

        # 4. Buscar la estructura base de preguntas del primer registro que tenga la definición válida
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

        # Construir los encabezados de columnas (P1, P2, P3...)
        headers = [
            ProfessorQuestionHeaderSchema(
                id=q.get("id", idx + 1),
                label=f"P{idx + 1}",
                full_text=q.get("question", ""),
            )
            for idx, q in enumerate(questions_list)
        ]

        # 5. Mapear las filas de forma obligatoria para todos los docentes matriculados
        rows = []
        for res in enrollments_responses:
            professor_answers = []

            # Extraer de manera segura el payload interno de "answers"
            response_json = res.survey_answers or {}
            answers_payload = response_json.get("answers", {})

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
                    # Relleno visual en la matriz si el docente no ha contestado la encuesta o esa pregunta
                    professor_answers.append("—")

            # Cálculo de promedios individuales
            if answered_questions_count > 0:
                average_str = f"{(total_score_sum / answered_questions_count):.2f}"
            else:
                average_str = "0.00"

            rows.append(
                ProfessorSurveyRowSchema(
                    professor_name=res.user_name,
                    answers=professor_answers,
                    average=average_str,
                )
            )

        surveys_report_list.append(
            SingleProfessorSurveyMatrixSchema(
                block_id=block.id, survey_title=survey_title, headers=headers, rows=rows
            )
        )

    # 6. Empaquetar la estructura final para el generador de PDF
    report_data = CourseProfessorSurveyReportSchema(
        course_id=course_id, course_name=course_name, surveys=surveys_report_list
    )

    return export_professor_survey_report_pdf(
        report=report_data, generated_at=datetime.now().strftime("%d/%m/%Y %H:%M")
    )
