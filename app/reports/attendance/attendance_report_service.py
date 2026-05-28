from .attendance_report_queries import (
    get_course_student_attendance_report,
    get_course_teacher_attendance_report,
)
from .attendance_report_schemas import StudentAttendanceReport, TeacherAttendanceReport


def generate_course_student_attendance_report(
    db,
    course_id: int,
):

    rows = get_course_student_attendance_report(
        db=db,
        course_id=course_id,
    )

    report = []

    for row in rows:

        percentage = 0

        valid_total = row.present_count + row.absent_count

        if valid_total > 0:

            percentage = round(
                (row.present_count / valid_total) * 100,
                2,
            )

        report.append(
            StudentAttendanceReport(
                student_id=row.student_id,
                student_name=row.student_name,
                total_attendances=row.total_attendances,
                present_count=row.present_count,
                absent_count=row.absent_count,
                pending_count=row.pending_count,
                attendance_percentage=percentage,
            )
        )

    return report


def generate_course_teacher_attendance_report(
    db,
):

    rows = get_course_teacher_attendance_report(
        db=db,
    )

    report = []

    for row in rows:

        valid_total = row.present_count + row.absent_count

        percentage = 0

        if valid_total > 0:

            percentage = round(
                (row.present_count / valid_total) * 100,
                2,
            )

        report.append(
            TeacherAttendanceReport(
                course_id=row.course_id,
                course_name=row.course_name,
                teacher_id=row.teacher_id,
                teacher_name=row.teacher_name,
                total_attendances=row.total_attendances,
                present_count=row.present_count,
                absent_count=row.absent_count,
                pending_count=row.pending_count,
                attendance_percentage=percentage,
            )
        )

    return report
