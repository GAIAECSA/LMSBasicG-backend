import os

from weasyprint import HTML

from app.core.config import settings


def export_student_attendance_pdf(
    report,
    course_name: str,
    generated_at: str,
    domain: str,
):

    template = settings.jinja_env.get_template(
        f"c_student_attendance/{domain}.html",
        "c_student_attendance/student_attendance_report.html",
    )

    dynamic_logo_path = f"static/reports_resources/{domain}.png"

    if not os.path.exists(f"app/{dynamic_logo_path}"):
        dynamic_logo_path = "static/reports_resources/logo_athena.png"

    html_string = template.render(
        report=report,
        course_name=course_name,
        generated_at=generated_at,
        logo_path=dynamic_logo_path,
        logo_plataform="static/reports_resources/logo_athena.png",
    )

    return HTML(
        string=html_string,
        base_url="app",
    ).write_pdf()
