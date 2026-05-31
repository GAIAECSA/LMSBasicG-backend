from typing import List

from pydantic import BaseModel


class QuestionHeaderSchema(BaseModel):
    id: int
    label: str  # P1, P2, P3...
    full_text: str  # El texto completo de la pregunta para el tooltip/leyenda


class StudentSurveyRowSchema(BaseModel):
    student_name: str
    answers: List[str]  # Lista de valores o respuestas dadas ("4", "1", "—")
    average: str  # Promedio de la escala Likert obtenido por el alumno


class SingleSurveyMatrixSchema(BaseModel):
    block_id: int
    survey_title: str
    headers: List[QuestionHeaderSchema]
    rows: List[StudentSurveyRowSchema]


class CourseSurveyReportSchema(BaseModel):
    course_id: int
    course_name: str
    surveys: List[SingleSurveyMatrixSchema]
