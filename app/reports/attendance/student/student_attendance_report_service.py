from datetime import datetime

from app.models.course import Course

from .student_attendance_report_pdf import export_student_attendance_pdf
from .student_attendance_report_queries import get_course_student_attendance_report
from .student_attendance_report_schemas import StudentAttendanceReport


def generate_student_attendance_pdf(
    db,
    course_id: int,
):

    report = generate_course_student_attendance_report(
        db=db,
        course_id=course_id,
    )

    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.deleted == False,
        )
        .first()
    )

    if not course:
        raise Exception("Curso no encontrado")

    pdf = export_student_attendance_pdf(
        report=report,
        course_name=course.name,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )

    return pdf


# Formateo


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
