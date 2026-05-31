from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .teacher_attendance_pdf import export_teacher_attendance_pdf
from .teacher_attendance_queries import get_teacher_attendance_report_data
from .teacher_attendance_schemas import TeacherAttendanceReport, TeacherAttendanceRow


def generate_teacher_attendance_pdf(db: Session, course_id: int):
    # 1. Validar existencia del curso
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.deleted.is_(False))
        .first()
    )
    if not course:
        raise ValueError("Curso no encontrado")

    # 2. Extraer registros de asistencia del profesor
    rows = get_teacher_attendance_report_data(db=db, course_id=course_id)

    records_list = []
    teacher_name = "No asignado"

    if rows:
        # Extraer el nombre completo del docente del primer registro encontrado
        teacher_name = f"{rows[0].teacher_firstname} {rows[0].teacher_lastname}"

    for row in rows:
        formatted_date = row.date.strftime("%d/%m/%Y") if row.date else "—"
        formatted_start = row.start_time.strftime("%H:%M") if row.start_time else "—"
        formatted_end = row.end_time.strftime("%H:%M") if row.end_time else "—"

        records_list.append(
            TeacherAttendanceRow(
                date=formatted_date,
                start_time=formatted_start,
                end_time=formatted_end,
                status=row.status or "PENDIENTE",
            )
        )

    report_data = TeacherAttendanceReport(
        course_id=course_id,
        course_name=course.name,
        teacher_name=teacher_name,
        records=records_list,
    )

    # 3. Construir binario del PDF
    return export_teacher_attendance_pdf(
        report=report_data,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
