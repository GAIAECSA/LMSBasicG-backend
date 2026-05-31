from weasyprint import HTML

from app.core.config import settings


def export_practice_quizz_pdf(report, generated_at: str):
    template = settings.jinja_env.get_template(
        "h_diagnostic_quizz/practice_quizz_report.html"
    )

    html_string = template.render(
        report=report,
        generated_at=generated_at,
        logo_path="static/reports_resources/logo_empresa.png",
        logo_plataform="static/reports_resources/logo_athena.png",
    )

    return HTML(
        string=html_string,
        base_url="app",
    ).write_pdf()
