from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, lesson: Lesson) -> Lesson:
    db.add(lesson)
    db.flush()
    return lesson


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(
    db: Session,
    lesson_id: int,
    business_id: int,
) -> None:
    (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id,
            Lesson.business_id == business_id,
            Lesson.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_module(
    db: Session,
    module_id: int,
    business_id: int,
) -> None:
    (
        db.query(Lesson)
        .filter(
            Lesson.module_id == module_id,
            Lesson.business_id == business_id,
            Lesson.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_course(
    db: Session,
    course_id: int,
    business_id: int,
) -> None:
    (
        db.query(Lesson)
        .filter(
            Lesson.business_id == business_id,
            Lesson.deleted.is_(False),
            Lesson.module_id.in_(
                db.query(Module.id).filter(
                    Module.course_id == course_id,
                    Module.business_id == business_id,
                    Module.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_subcategory(
    db: Session,
    subcategory_id: int,
    business_id: int,
) -> None:
    (
        db.query(Lesson)
        .filter(
            Lesson.business_id == business_id,
            Lesson.deleted.is_(False),
            Lesson.module_id.in_(
                db.query(Module.id)
                .join(Course)
                .filter(
                    Course.subcategory_id == subcategory_id,
                    Course.business_id == business_id,
                    Course.deleted.is_(False),
                    Module.business_id == business_id,
                    Module.deleted.is_(False),
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
        db.query(Lesson)
        .filter(
            Lesson.business_id == business_id,
            Lesson.deleted.is_(False),
            Lesson.module_id.in_(
                db.query(Module.id)
                .join(Course)
                .join(Subcategory)
                .filter(
                    Subcategory.category_id == category_id,
                    Subcategory.business_id == business_id,
                    Subcategory.deleted.is_(False),
                    Course.business_id == business_id,
                    Course.deleted.is_(False),
                    Module.business_id == business_id,
                    Module.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


# --- Consultas (Lectura) ---


def get_by_id(db: Session, lesson_id: int, business_id: int):
    return (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id,
            Lesson.business_id == business_id,
            Lesson.deleted == False,
        )
        .first()
    )


def get_by_module_id(db: Session, module_id: int, business_id: int):
    return (
        db.query(Lesson)
        .filter(
            Lesson.module_id == module_id,
            Lesson.business_id == business_id,
            Lesson.deleted == False,
        )
        .all()
    )


# Viejo
# def create(db: Session, lesson: Lesson):
#   db.add(lesson)
#  db.commit()
# db.refresh(lesson)
# return lesson


# def update(db: Session, lesson: Lesson):
#   db.merge(lesson)
#  db.commit()
# db.refresh(lesson)
# return lesson


# def delete(db: Session, lesson: Lesson):
#   lesson.deleted = True
#  db.merge(lesson)
# db.commit()
# return lesson


# def get_by_id(db: Session, lesson_id: int):
#   return (
#      db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.deleted == False).first()
# )


# def get_by_module_id(db: Session, module_id: int):
#   return (
#      db.query(Lesson)
#     .filter(Lesson.module_id == module_id, Lesson.deleted == False)
#    .all()
# )
