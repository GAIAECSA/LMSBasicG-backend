from pydantic import BaseModel


class BlockHeaderSchema(BaseModel):
    id: int
    title: str


class StudentGradeRowSchema(BaseModel):
    student_name: str
    grades: list[str]  # Lista alineada al orden de los headers
    average: str
    status: str  # PASÓ o NO PASÓ


class FinalGradeReportSchema(BaseModel):
    course_id: int
    course_name: str
    headers: list[BlockHeaderSchema]
    rows: list[StudentGradeRowSchema]
