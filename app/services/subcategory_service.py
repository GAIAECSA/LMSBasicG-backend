from sqlalchemy.orm import Session

from app.models.subcategory import Subcategory
from app.repositories import (
    attendance_repo,
    block_progress_repo,
    certificate_repo,
    certificate_template_repo,
    course_attendance_repo,
    course_repo,
    enrollment_repo,
    forum_response_repo,
    homework_response_repo,
    lesson_block_repo,
    lesson_repo,
    mdt_certificate_repo,
    module_repo,
    quizz_response_repo,
    subcategory_repo,
    survey_response_repo,
)
from app.schemas.subcategory import SubcategoryCreate, SubcategoryUpdate

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class SubcategoryNotFoundError(Exception):
    pass


class SubcategoryAlreadyExistsError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def create_subcategory(db: Session, data: SubcategoryCreate, business_id: int):
    with db.begin():
        existing = subcategory_repo.get_by_name_and_category(
            db, data.name, data.category_id, business_id
        )
        if existing:
            raise SubcategoryAlreadyExistsError(
                "La subcategoría ya existe en esta categoría"
            )

        subcategory = Subcategory(**data.model_dump(), business_id=business_id)
        return subcategory_repo.create(db, subcategory)


def update_subcategory(
    db: Session, subcategory_id: int, data: SubcategoryUpdate, business_id: int
):
    with db.begin():
        subcategory = subcategory_repo.get_by_id(db, subcategory_id, business_id)
        if not subcategory:
            raise SubcategoryNotFoundError("Subcategoría no encontrada")

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] != subcategory.name:
            existing = subcategory_repo.get_by_name_and_category(
                db, update_data["name"], subcategory.category_id, business_id
            )
            if existing:
                raise SubcategoryAlreadyExistsError(
                    "La subcategoría ya existe en esta categoría"
                )

        for key, value in update_data.items():
            setattr(subcategory, key, value)

        return subcategory


def delete_subcategory(db: Session, subcategory_id: int, business_id: int):
    with db.begin():
        subcategory = subcategory_repo.get_by_id(db, subcategory_id, business_id)
        if not subcategory:
            raise SubcategoryNotFoundError("Subcategoría no encontrada")

        cascade_steps = [
            # Blocks
            homework_response_repo.delete_soft_by_subcategory(),
            forum_response_repo.delete_soft_by_subcategory(),
            survey_response_repo.delete_soft_by_subcategory(),
            quizz_response_repo.delete_soft_by_subcategory(),
            # Navigation
            lesson_block_repo.delete_soft_by_subcategory(),
            lesson_repo.delete_soft_by_subcategory(),
            module_repo.delete_soft_by_subcategory(),
            # Certificates
            certificate_repo.delete_soft_by_subcategory(),
            mdt_certificate_repo.delete_soft_by_subcategory(),
            certificate_template_repo.delete_soft_by_subcategory(),
            # Attendance
            attendance_repo.delete_soft_by_subcategory(),
            course_attendance_repo.delete_soft_by_subcategory(),
            # Enrollments
            enrollment_repo.delete_soft_by_subcategory(),
            # Block Progress
            block_progress_repo.delete_soft_by_subcategory(),
            # Course
            course_repo.delete_soft_by_subcategory(),
        ]

        for step in cascade_steps:
            step(db, subcategory_id, business_id)
        return subcategory_repo.delete_soft_by_id(db, subcategory_id, business_id)


def get_subcategory(db: Session, subcategory_id: int, business_id: int):
    subcategory = subcategory_repo.get_by_id(db, subcategory_id, business_id)
    if not subcategory:
        raise SubcategoryNotFoundError("Subcategoría no encontrada")
    return subcategory


def get_subcategories_by_category(db: Session, category_id: int, business_id: int):
    return subcategory_repo.get_by_category(db, category_id, business_id)


def get_all_subcategories(db: Session, business_id: int):
    return subcategory_repo.get_all(db, business_id)


"""
def create_subcategory(db: Session, data: SubcategoryCreate):
    existing = subcategory_repo.get_by_name_and_category(
        db, data.name, data.category_id
    )
    if existing:
        raise Exception("La subcategoría ya existe en esta categoría")

    subcategory = Subcategory(**data.model_dump())
    return subcategory_repo.create(db, subcategory)


def update_subcategory(db: Session, subcategory_id: int, data: SubcategoryUpdate):
    subcategory = subcategory_repo.get_by_id(db, subcategory_id)
    if not subcategory:
        raise Exception("Subcategoría no encontrada")

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] != subcategory.name:
        existing = subcategory_repo.get_by_name_and_category(
            db, update_data["name"], subcategory.category_id
        )
        if existing:
            raise Exception("La subcategoría ya existe en esta categoría")

    for key, value in update_data.items():
        setattr(subcategory, key, value)

    return subcategory_repo.update(db, subcategory)


def delete_subcategory(db: Session, subcategory_id: int):
    subcategory = subcategory_repo.get_by_id(db, subcategory_id)
    if not subcategory:
        raise Exception("Subcategoría no encontrada")

    return subcategory_repo.delete(db, subcategory)


def get_subcategory(db: Session, subcategory_id: int):
    subcategory = subcategory_repo.get_by_id(db, subcategory_id)
    if not subcategory:
        raise Exception("Subcategoría no encontrada")
    return subcategory


def get_subcategories_by_category(db: Session, category_id: int):
    return subcategory_repo.get_by_category_id(db, category_id)


def get_all_subcategories(db: Session):
    return subcategory_repo.get_all(db)
"""
