from decimal import Decimal

from pydantic import BaseModel


class GradedHomeworkRow(BaseModel):
    student_id: int
    student_name: str
    activity_title: str
    has_submitted: bool
    score: Decimal | None
    submitted_at: str | None
    status_label: str


class GradedHomeworkReport(BaseModel):
    course_id: int
    course_name: str
    records: list[GradedHomeworkRow]
