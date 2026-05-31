from typing import List

from pydantic import BaseModel


class QuestionHeaderSchema(BaseModel):
    id: int
    label: str  # P1, P2, P3...
    full_text: str  # El texto completo de la pregunta


class ProfessorSurveyRowSchema(BaseModel):
    professor_name: str
    answers: List[str]  # Lista de respuestas ("4", "1", "—")
    average: str  # Promedio obtenido por el docente


class ProfessorSurveyMatrixSchema(BaseModel):
    block_id: int
    survey_title: str
    headers: List[QuestionHeaderSchema]
    rows: List[ProfessorSurveyRowSchema]


class ProfessorCourseSurveyReportSchema(BaseModel):
    course_id: int
    course_name: str
    surveys: List[ProfessorSurveyMatrixSchema]
