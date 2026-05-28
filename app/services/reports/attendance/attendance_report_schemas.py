from pydantic import BaseModel


class StudentAttendanceReport(BaseModel):

    student_id: int
    student_name: str

    total_attendances: int

    present_count: int
    absent_count: int
    pending_count: int

    attendance_percentage: float


class TeacherAttendanceReport(BaseModel):

    course_id: int
    course_name: str

    teacher_id: int
    teacher_name: str

    total_attendances: int

    present_count: int
    absent_count: int
    pending_count: int

    attendance_percentage: float
