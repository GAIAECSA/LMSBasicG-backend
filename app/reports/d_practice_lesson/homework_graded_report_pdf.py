from weasyprint import HTML

from app.core.config import settings


def export_graded_homework_report_pdf(
    report,
    generated_at: str,
):
    # Carga específicamente la plantilla de la matriz de calificaciones
    template = settings.jinja_env.get_template(
        "d_practice_lesson/homework_graded_report.html"
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
