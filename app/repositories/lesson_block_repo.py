from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.module import Module
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, lesson_block: LessonBlock) -> LessonBlock:
    db.add(lesson_block)
    db.flush()
    return lesson_block


def create_bulk(db: Session, lesson_blocks: list[LessonBlock]) -> list[LessonBlock]:
    db.add_all(lesson_blocks)
    db.flush()
    return lesson_blocks


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(
    db: Session,
    lesson_block_id: int,
    business_id: int,
) -> None:
    (
        db.query(LessonBlock)
        .filter(
            LessonBlock.id == lesson_block_id,
            LessonBlock.business_id == business_id,
            LessonBlock.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson(
    db: Session,
    lesson_id: int,
    business_id: int,
) -> None:
    (
        db.query(LessonBlock)
        .filter(
            LessonBlock.lesson_id == lesson_id,
            LessonBlock.business_id == business_id,
            LessonBlock.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_module(
    db: Session,
    module_id: int,
    business_id: int,
) -> None:
    (
        db.query(LessonBlock)
        .filter(
            LessonBlock.business_id == business_id,
            LessonBlock.deleted.is_(False),
            LessonBlock.lesson_id.in_(
                db.query(Lesson.id).filter(
                    Lesson.module_id == module_id,
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_course(
    db: Session,
    course_id: int,
    business_id: int,
) -> None:
    (
        db.query(LessonBlock)
        .filter(
            LessonBlock.business_id == business_id,
            LessonBlock.deleted.is_(False),
            LessonBlock.lesson_id.in_(
                db.query(Lesson.id)
                .join(Module)
                .filter(
                    Module.course_id == course_id,
                    Module.business_id == business_id,
                    Module.deleted.is_(False),
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
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
        db.query(LessonBlock)
        .filter(
            LessonBlock.business_id == business_id,
            LessonBlock.deleted.is_(False),
            LessonBlock.lesson_id.in_(
                db.query(Lesson.id)
                .join(Module)
                .join(Course)
                .filter(
                    Course.subcategory_id == subcategory_id,
                    Course.business_id == business_id,
                    Course.deleted.is_(False),
                    Module.business_id == business_id,
                    Module.deleted.is_(False),
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
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
        db.query(LessonBlock)
        .filter(
            LessonBlock.business_id == business_id,
            LessonBlock.deleted.is_(False),
            LessonBlock.lesson_id.in_(
                db.query(Lesson.id)
                .join(Module)
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
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


# --- Consultas (Lectura) ---


def get_by_id(db: Session, lesson_block_id: int, business_id: int):
    return (
        db.query(LessonBlock)
        .options(joinedload(LessonBlock.lesson_block_type))
        .filter(
            LessonBlock.id == lesson_block_id,
            LessonBlock.business_id == business_id,
            LessonBlock.deleted == False,
        )
        .first()
    )


def get_all_by_lesson_id(db: Session, lesson_id: int, business_id: int):
    return (
        db.query(LessonBlock)
        .options(joinedload(LessonBlock.lesson_block_type))
        .filter(
            LessonBlock.deleted == False,
            LessonBlock.business_id == business_id,
            LessonBlock.lesson_id == lesson_id,
        )
        .all()
    )


def get_default_by_course_id(db: Session, course_id: int, business_id: int):
    return (
        db.query(LessonBlock)
        .filter(
            LessonBlock.deleted == False,
            LessonBlock.course_id == course_id,
            LessonBlock.business_id == business_id,
            LessonBlock.default == True,
        )
        .all()
    )


def get_all_default_blocks_by_course_and_block_type(
    db: Session, course_id: int, block_type_id: int, business_id: int
):
    return (
        db.query(LessonBlock)
        .filter(
            LessonBlock.deleted == False,
            LessonBlock.course_id == course_id,
            LessonBlock.block_type_id == block_type_id,
            LessonBlock.business_id == business_id,
            LessonBlock.default == True,
        )
        .all()
    )


# Viejos
# def create(db: Session, lesson_block: LessonBlock):
#   db.add(lesson_block)
#  db.flush()
# db.refresh(lesson_block)
# return lesson_block


# def update(db: Session, lesson_block: LessonBlock):
#   lesson_block = db.merge(lesson_block)
#  db.flush()
# db.refresh(lesson_block)
# return lesson_block


# def delete(db: Session, lesson_block: LessonBlock):
#   lesson_block.deleted = True
#  db.merge(lesson_block)
# db.flush()
# return lesson_block


# def get_by_id(db: Session, lesson_block_id: int):
#   return (
#      db.query(LessonBlock)
#     .options(joinedload(LessonBlock.lesson_block_type))
#    .filter(LessonBlock.id == lesson_block_id, LessonBlock.deleted == False)
#   .first()
# )


# def get_all_by_lesson_id(db: Session, lesson_id: int):
#   return (
#      db.query(LessonBlock)
#     .options(joinedload(LessonBlock.lesson_block_type))
#    .filter(LessonBlock.deleted == False, LessonBlock.lesson_id == lesson_id)
#   .all()
# )


# def create_all(db: Session, lesson_blocks: list[LessonBlock]):
#   db.add_all(lesson_blocks)
#  db.flush()
# return lesson_blocks


# def get_default_by_course_id(db: Session, course_id: int):
#   return (
#      db.query(LessonBlock)
#     .filter(
#        LessonBlock.deleted == False,
#       LessonBlock.course_id == course_id,
#      LessonBlock.default == True,
# )
# .all()
# )


# def delete_default_by_course_id(
#   db: Session,
#  course_id: int,
# ):
#   db.query(LessonBlock).filter(
#      LessonBlock.deleted == False,
#     LessonBlock.course_id == course_id,
#    LessonBlock.default == True,
# ).update(
#   {"deleted": True},
#  synchronize_session=False,
# )

# db.flush()


# def get_all_default_blocks_by_course_and_block_type(
#   db: Session, course_id: int, block_type_id: int
# ):
#   return (
#      db.query(LessonBlock)
#     .filter(
#        LessonBlock.deleted == False,
#       LessonBlock.course_id == course_id,
#      LessonBlock.block_type_id == block_type_id,
#     LessonBlock.default == True,
# )
# .all()
# )
