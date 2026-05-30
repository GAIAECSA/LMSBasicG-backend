from pydantic import BaseModel


class StudentHomeworkSubmission(BaseModel):
    student_id: int
    student_name: str
    has_submitted: bool
    submitted_at: str | None
    status_label: str


class HomeworkStudentsReport(BaseModel):
    course_id: int
    course_name: str
    activity_title: str
    students: list[StudentHomeworkSubmission]
