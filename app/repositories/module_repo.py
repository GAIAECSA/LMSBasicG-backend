from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.module import Module
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, module: Module) -> Module:
    db.add(module)
    db.flush()
    return module


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(
    db: Session,
    module_id: int,
    business_id: int,
) -> None:
    (
        db.query(Module)
        .filter(
            Module.id == module_id,
            Module.business_id == business_id,
            Module.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_course(
    db: Session,
    course_id: int,
    business_id: int,
) -> None:
    (
        db.query(Module)
        .filter(
            Module.course_id == course_id,
            Module.business_id == business_id,
            Module.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_subcategory(
    db: Session,
    subcategory_id: int,
    business_id: int,
) -> None:
    (
        db.query(Module)
        .filter(
            Module.business_id == business_id,
            Module.deleted.is_(False),
            Module.course_id.in_(
                db.query(Course.id).filter(
                    Course.subcategory_id == subcategory_id,
                    Course.business_id == business_id,
                    Course.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_category(
    db: Session,
    category_id: int,
    business_id: int,
) -> None:
    (
        db.query(Module)
        .filter(
            Module.business_id == business_id,
            Module.deleted.is_(False),
            Module.course_id.in_(
                db.query(Course.id)
                .join(Subcategory)
                .filter(
                    Subcategory.category_id == category_id,
                    Subcategory.business_id == business_id,
                    Subcategory.deleted.is_(False),
                    Course.business_id == business_id,
                    Course.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


# --- Consultas (Lectura) ---


def get_by_id(db: Session, module_id: int, business_id: int):
    return (
        db.query(Module)
        .filter(
            Module.id == module_id,
            Module.business_id == business_id,
            Module.deleted == False,
        )
        .first()
    )


def get_by_course_id(db: Session, course_id: int, business_id: int):
    return (
        db.query(Module)
        .filter(
            Module.course_id == course_id,
            Module.business_id == business_id,
            Module.deleted == False,
        )
        .all()
    )


# Viejo
# def create(db: Session, module: Module):
#   db.add(module)
#  db.commit()
# db.refresh(module)
# return module


# def update(db: Session, module: Module):
#   db.merge(module)
#  db.commit()
# db.refresh(module)
# return module


# def delete(db: Session, module: Module):
##  db.merge(module)
# db.commit()
# return module


# def get_by_id(db: Session, module_id: int):
#   return (
#      db.query(Module).filter(Module.id == module_id, Module.deleted == False).first()
# )


# def get_by_course_id(db: Session, course_id: int):
#   return (
#      db.query(Module)
#     .filter(Module.course_id == course_id, Module.deleted == False)
#    .all()
# )
