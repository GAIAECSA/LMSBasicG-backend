import os

from weasyprint import HTML

from app.core.config import settings


def export_course_structure_pdf(
    domain: str,
    report,
    generated_at: str,
):
    template = settings.jinja_env.select_template(
        [
            f"a_course_structure/{domain}.html",
            "a_course_structure/course_structure_report.html",
        ]
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
