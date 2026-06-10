from decimal import Decimal

from pydantic import BaseModel


class HomeworkHeaderSchema(BaseModel):
    id: int
    title: str


class HomeworkCellSchema(BaseModel):
    score: str
    submitted: bool


class StudentHomeworkRowSchema(BaseModel):
    student_name: str
    homeworks: list[HomeworkCellSchema]
    average: str


class HomeworkMatrixReportSchema(BaseModel):
    course_id: int
    course_name: str
    headers: list[HomeworkHeaderSchema]
    rows: list[StudentHomeworkRowSchema]
