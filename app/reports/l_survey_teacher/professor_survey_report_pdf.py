import os

from weasyprint import HTML

from app.core.config import settings


def export_professor_survey_report_pdf(
    report,
    generated_at: str,
    domain: str,
):
    template = settings.jinja_env.get_template(
        f"l_survey_teacher/{domain}.html",
        "l_survey_teacher/course_professor_survey_report.html",
    )

    dynamic_logo_path = f"static/reports_resources/{domain}.png"

    if not os.path.exists(f"app/{dynamic_logo_path}"):
        dynamic_logo_path = "static/reports_resources/logo_athena.png"

    html_string = template.render(
        report=report,
        generated_at=generated_at,
        logo_path=dynamic_logo_path,
        logo_plataform="static/reports_resources/logo_athena.png",
    )

    return HTML(
        string=html_string,
        base_url="app",
    ).write_pdf()
