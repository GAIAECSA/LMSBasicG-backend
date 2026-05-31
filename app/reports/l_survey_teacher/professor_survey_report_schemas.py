from typing import List

from pydantic import BaseModel


class ProfessorQuestionHeaderSchema(BaseModel):
    id: int
    label: str  # P1, P2, P3...
    full_text: str


class ProfessorSurveyRowSchema(BaseModel):
    professor_name: str
    answers: List[str]  # Respuestas ordenadas ("4", "1", "—")
    average: str  # Promedio de la escala Likert del docente


class SingleProfessorSurveyMatrixSchema(BaseModel):
    block_id: int
    survey_title: str
    headers: List[ProfessorQuestionHeaderSchema]
    rows: List[ProfessorSurveyRowSchema]


class CourseProfessorSurveyReportSchema(BaseModel):
    course_id: int
    course_name: str
    surveys: List[SingleProfessorSurveyMatrixSchema]
