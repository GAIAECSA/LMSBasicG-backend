from typing import Optional

from pydantic import BaseModel


class QuizzHeaderSchema(BaseModel):
    id: int
    title: str


class QuizzDetailSchema(BaseModel):
    score: str
    is_passed: Optional[bool] = None


class StudentPracticeRowSchema(BaseModel):
    student_name: str
    quizzes: list[QuizzDetailSchema]
    average: str


class PracticeQuizzReportSchema(BaseModel):
    course_id: int
    course_name: str
    headers: list[QuizzHeaderSchema]
    rows: list[StudentPracticeRowSchema]
