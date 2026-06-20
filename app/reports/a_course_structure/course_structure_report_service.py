from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import Course

from .course_structure_report_pdf import export_course_structure_pdf
from .course_structure_report_queries import (
    get_course_structure_rows,
    get_default_course_blocks,
)
from .course_structure_report_schemas import (
    CourseBlockReport,
    CourseLessonReport,
    CourseModuleReport,
    CourseStructureReport,
)


def generate_course_structure_report(
    db: Session, course_id: int, business_id: int, domain: str
):
    # Validar existencia del curso base
    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.deleted == False,
            Course.business_id == business_id,
        )
        .first()
    )

    if not course:
        raise Exception("Curso no encontrado")

    report = generate_course_structure_report_data(
        db=db,
        course_id=course_id,
        course_name=course.name,
        business_id=business_id,
    )

    pdf = export_course_structure_pdf(
        domain=domain,
        report=report,
        generated_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )

    return pdf


# Formateo y Mapeo Manual


def generate_course_structure_report_data(
    db: Session,
    course_id: int,
    course_name: str,
    business_id: int,
):
    rows = get_course_structure_rows(
        db=db, course_id=course_id, business_id=business_id
    )
    default_rows = get_default_course_blocks(
        db=db, course_id=course_id, business_id=business_id
    )

    # 1. Mapear bloques globales por defecto
    default_blocks = []
    for d_row in default_rows:
        block_title = "Sin título"
        if isinstance(d_row.content, dict):
            block_title = (
                d_row.content.get("title") or d_row.content.get("name") or "Sin título"
            )
        elif isinstance(d_row.content, str):
            block_title = d_row.content

        default_blocks.append(
            CourseBlockReport(
                block_id=d_row.block_id,
                block_title=block_title,
                block_type=d_row.block_type or "Bloque",
                is_default=True,
            )
        )

    # 2. Agrupar filas planas
    modules_map = {}

    for row in rows:
        if row.module_id is None:
            continue

        if row.module_id not in modules_map:
            modules_map[row.module_id] = {
                "module_id": row.module_id,
                "module_name": row.module_name,
                "module_order": row.module_order,
                "lessons_map": {},
            }

        mod_group = modules_map[row.module_id]

        if row.lesson_id is None:
            continue

        if row.lesson_id not in mod_group["lessons_map"]:
            mod_group["lessons_map"][row.lesson_id] = {
                "lesson_id": row.lesson_id,
                "lesson_name": row.lesson_name,
                "lesson_order": row.lesson_order,
                "blocks": [],
            }

        lesson_group = mod_group["lessons_map"][row.lesson_id]

        if row.block_id is None:
            continue

        # Validar el título del bloque dinámicamente
        block_title = "Sin título"
        if isinstance(row.content, dict):
            block_title = (
                row.content.get("title") or row.content.get("name") or "Sin título"
            )
        elif isinstance(row.content, str):
            block_title = row.content

        # ¡CORRECCIÓN AQUÍ!: Asignar el valor real de la fila (row.is_default)
        lesson_group["blocks"].append(
            CourseBlockReport(
                block_id=row.block_id,
                block_title=block_title,
                block_type=row.block_type or "Bloque",
                is_default=bool(row.is_default),
            )
        )

    # 3. Ensamblar estructuras finales hacia esquemas Pydantic
    modules_report = []
    for _, mod_data in sorted(modules_map.items(), key=lambda x: x[1]["module_order"]):
        lessons_report = []
        for _, les_data in sorted(
            mod_data["lessons_map"].items(), key=lambda x: x[1]["lesson_order"]
        ):
            lessons_report.append(
                CourseLessonReport(
                    lesson_id=les_data["lesson_id"],
                    lesson_name=les_data["lesson_name"],
                    lesson_order=les_data["lesson_order"],
                    blocks=les_data["blocks"],
                )
            )

        modules_report.append(
            CourseModuleReport(
                module_id=mod_data["module_id"],
                module_name=mod_data["module_name"],
                module_order=mod_data["module_order"],
                lessons=lessons_report,
            )
        )

    return CourseStructureReport(
        course_id=course_id,
        course_name=course_name,
        default_blocks=default_blocks,
        modules=modules_report,
    )
