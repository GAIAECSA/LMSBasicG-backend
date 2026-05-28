from weasyprint import HTML

from app.core.config import settings


def export_student_attendance_pdf(
    report,
    course_name: str,
):

    template = settings.jinja_env.get_template(
        "attendance/templates/student_attendance_report.html"
    )

    html_string = template.render(
        report=report,
        course_name="Python Básico",
        generated_at="27/05/2026",
        logo_path="static/logos/logo.png",
    )

    pdf = HTML(
        string=html_string,
        base_url="app/",
    ).write_pdf()

    return pdf
