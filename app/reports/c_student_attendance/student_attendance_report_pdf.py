from weasyprint import HTML

from app.core.config import settings


def export_student_attendance_pdf(
    report,
    course_name: str,
    generated_at: str,
):

    template = settings.jinja_env.get_template(
        "c_student_attendance/student_attendance_report.html"
    )

    html_string = template.render(
        report=report,
        course_name=course_name,
        generated_at=generated_at,
        logo_path="static/reports_resources/logo_empresa.png",
    )

    return HTML(
        string=html_string,
        base_url="app",
    ).write_pdf()
