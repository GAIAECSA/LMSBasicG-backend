import os

from weasyprint import HTML

from app.core.config import settings


def export_practice_quizz_pdf(
    report,
    generated_at: str,
    domain: str,
):
    template = settings.jinja_env.get_template(
        f"h_diagnostic_quizz/{domain}.html",
        "h_diagnostic_quizz/practice_quizz_report.html",
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
