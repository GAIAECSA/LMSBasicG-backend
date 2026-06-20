from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .mdt_report_pdf import export_mdt_certificate_report_pdf
from .mdt_report_queries import get_mdt_certificates_report_data
from .mdt_report_schemas import MdtReportResponseSchema, MdtReportRowSchema


def generate_mdt_certificates_report_pdf(
    db: Session,
    course_id: int,
    certificate_type: str,
    business_id: int,
    domain: str,
):
    # 1. Validar la existencia del curso
    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.deleted.is_(False),
            Course.business_id == business_id,
        )
        .first()
    )

    if not course:
        raise ValueError("Curso no encontrado")

    # 2. Recuperar registros cruzados de la base de datos
    raw_data = get_mdt_certificates_report_data(
        db=db,
        course_id=course_id,
        certificate_type=certificate_type,
        business_id=business_id,
    )

    # 3. Construir filas estructuradas para la plantilla
    report_rows = []

    for row in raw_data:
        # Resolver nombre del alumno o fallback al documento si no hay match exacto
        if row.student_firstname and row.student_lastname:
            student_name = f"{row.student_lastname} " f"{row.student_firstname}"
        else:
            student_name = (
                f"Usuario no emparejado " f"(Doc: {row.certificate_id_number})"
            )

        # Determinar estado de visualización (visited_at)
        if row.visited_at:
            status = "Descargado"
            viewed_at = row.visited_at.strftime("%d/%m/%Y %H:%M")
        else:
            status = "No visto (Nel)"
            viewed_at = "—"

        report_rows.append(
            MdtReportRowSchema(
                student_name=student_name,
                certificate_type=row.certificate_type,
                status=status,
                viewed_at=viewed_at,
            )
        )

    # 4. Consolidar el payload del reporte
    report_payload = MdtReportResponseSchema(
        course_id=course_id,
        course_name=course.name,
        certificate_type=certificate_type,
        rows=report_rows,
    )

    return export_mdt_certificate_report_pdf(
        report=report_payload,
        domain=domain,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
