from datetime import datetime

from .teacher_attendance_report_pdf import export_teacher_attendance_pdf
from .teacher_attendance_report_queries import get_course_teacher_attendance_report
from .teacher_attendance_report_schemas import TeacherAttendanceReport


def generate_teacher_attendance_pdf(
    db,
):

    report = generate_course_teacher_attendance_report(
        db=db,
    )

    return export_teacher_attendance_pdf(
        report=report,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )


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
