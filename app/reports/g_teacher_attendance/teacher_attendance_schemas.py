from pydantic import BaseModel


class TeacherAttendanceRow(BaseModel):
    date: str
    start_time: str
    end_time: str
    status: str


class TeacherAttendanceReport(BaseModel):
    course_id: int
    course_name: str
    teacher_name: str
    records: list[TeacherAttendanceRow]
