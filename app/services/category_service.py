from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories import (
    attendance_repo,
    block_progress_repo,
    category_repo,
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
from app.schemas.category import CategoryCreate, CategoryUpdate

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class CategoryNotFoundError(Exception):
    pass


class CategoryAlreadyExistsError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def create_category(db: Session, data: CategoryCreate, business_id: int):
    with db.begin():
        existing = category_repo.get_by_name(db, data.name, business_id)
        if existing:
            raise CategoryAlreadyExistsError("La categoría ya existe")

        category = Category(**data.model_dump(), business_id=business_id)

        return category_repo.create(db, category)


def update_category(
    db: Session, category_id: int, data: CategoryUpdate, business_id: int
):
    with db.begin():
        category = category_repo.get_by_id(db, category_id, business_id)
        if not category:
            raise CategoryNotFoundError("Categoría no encontrada")

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] != category.name:
            existing = category_repo.get_by_name(db, update_data["name"], business_id)
            if existing:
                raise CategoryAlreadyExistsError("La categoría ya existe")

        for key, value in update_data.items():
            setattr(category, key, value)

        return category


def delete_category(db: Session, category_id: int, business_id: int):
    with db.begin():
        category = category_repo.get_by_id(db, category_id, business_id)
        if not category:
            raise CategoryNotFoundError("Categoría no encontrada")

        cascade_steps = [
            # Blocks
            homework_response_repo.delete_soft_by_category(),
            forum_response_repo.delete_soft_by_category(),
            survey_response_repo.delete_soft_by_category(),
            quizz_response_repo.delete_soft_by_category(),
            # Navigation
            lesson_block_repo.delete_soft_by_category(),
            lesson_repo.delete_soft_by_category(),
            module_repo.delete_soft_by_category(),
            # Certificates
            certificate_repo.delete_soft_by_category(),
            mdt_certificate_repo.delete_soft_by_category(),
            certificate_template_repo.delete_soft_by_category(),
            # Attendance
            attendance_repo.delete_soft_by_category(),
            course_attendance_repo.delete_soft_by_category(),
            # Enrollments
            enrollment_repo.delete_soft_by_category(),
            # Block Progress
            block_progress_repo.delete_soft_by_category(),
            # Course
            course_repo.delete_soft_by_category(),
            # Subcategory
            subcategory_repo.delete_soft_by_category(),
        ]

        for step in cascade_steps:
            step(db, category_id, business_id)

        return category_repo.delete_soft_by_id(db, category, business_id)


def get_category(db: Session, category_id: int, business_id: int):
    category = category_repo.get_by_id(db, category_id, business_id)
    if not category:
        raise CategoryNotFoundError("Categoría no encontrada")
    return category


def get_all_categories(db: Session, business_id: int):
    return category_repo.get_all(db, business_id)


"""
def create_category(db: Session, data: CategoryCreate):
    existing = category_repo.get_by_name(db, data.name)
    if existing:
        raise Exception("La categoría ya existe")

    category = Category(**data.model_dump())

    return category_repo.create(db, category)


def update_category(db: Session, category_id: int, data: CategoryUpdate):
    category = category_repo.get_by_id(db, category_id)
    if not category:
        raise Exception("Categoría no encontrada")

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] != category.name:
        existing = category_repo.get_by_name(db, update_data["name"])
        if existing:
            raise Exception("La categoría ya existe")

    for key, value in update_data.items():
        setattr(category, key, value)

    return category_repo.update(db, category)


def delete_category(db: Session, category_id: int):
    category = category_repo.get_by_id(db, category_id)
    if not category:
        raise Exception("Categoría no encontrada")

    return category_repo.delete(db, category)


def get_category(db: Session, category_id: int):
    category = category_repo.get_by_id(db, category_id)
    if not category:
        raise Exception("Categoría no encontrada")
    return category


def get_all_categories(db: Session):
    return category_repo.get_all(db)
"""
