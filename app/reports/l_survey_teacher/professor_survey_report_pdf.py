from weasyprint import HTML

from app.core.config import settings


def export_professor_survey_report_pdf(report, generated_at: str):
    template = settings.jinja_env.get_template(
        "l_survey_teacher/course_professor_survey_report.html"
    )

    html_string = template.render(
        report=report,
        generated_at=generated_at,
        logo_path="static/reports_resources/logo_empresa.png",
    )

    return HTML(
        string=html_string,
        base_url="app",
    ).write_pdf()
