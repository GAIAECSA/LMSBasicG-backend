from weasyprint import HTML

from app.core.config import settings


def export_course_structure_pdf(
    report,
    generated_at: str,
):
    template = settings.jinja_env.get_template(
        "a_course_structure/course_structure_report.html"
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
