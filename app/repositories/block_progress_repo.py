from sqlalchemy.orm import Session

from app.models.block_progress import BlockProgress
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.module import Module
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, block_progress: BlockProgress) -> BlockProgress:
    db.add(block_progress)
    db.flush()
    return block_progress


def create_bulk(
    db: Session, block_progress: list[BlockProgress]
) -> list[BlockProgress]:
    db.add_all(block_progress)
    db.flush()
    return block_progress


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(
    db: Session,
    block_progress_id: int,
    business_id: int,
) -> None:
    (
        db.query(BlockProgress)
        .filter(
            BlockProgress.id == block_progress_id,
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_enrollment(
    db: Session,
    enrollment_id: int,
    business_id: int,
) -> None:
    (
        db.query(BlockProgress)
        .filter(
            BlockProgress.enrollment_id == enrollment_id,
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson_block(
    db: Session,
    lesson_block_id: int,
    business_id: int,
) -> None:
    (
        db.query(BlockProgress)
        .filter(
            BlockProgress.lesson_block_id == lesson_block_id,
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson(
    db: Session,
    lesson_id: int,
    business_id: int,
) -> None:
    (
        db.query(BlockProgress)
        .filter(
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
            BlockProgress.lesson_block_id.in_(
                db.query(LessonBlock.id).filter(
                    LessonBlock.lesson_id == lesson_id,
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_module(
    db: Session,
    module_id: int,
    business_id: int,
) -> None:
    (
        db.query(BlockProgress)
        .filter(
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
            BlockProgress.lesson_block_id.in_(
                db.query(LessonBlock.id)
                .join(Lesson)
                .filter(
                    Lesson.module_id == module_id,
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
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
        db.query(BlockProgress)
        .filter(
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
            BlockProgress.lesson_block_id.in_(
                db.query(LessonBlock.id)
                .join(Lesson)
                .join(Module)
                .filter(
                    Module.course_id == course_id,
                    Module.business_id == business_id,
                    Module.deleted.is_(False),
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
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
        db.query(BlockProgress)
        .filter(
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
            BlockProgress.lesson_block_id.in_(
                db.query(LessonBlock.id)
                .join(Lesson)
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
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
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
        db.query(BlockProgress)
        .filter(
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
            BlockProgress.lesson_block_id.in_(
                db.query(LessonBlock.id)
                .join(Lesson)
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
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


# --- Consultas (Lectura) ---


def get_by_id(
    db: Session,
    progress_id: int,
    business_id: int,
):
    return (
        db.query(BlockProgress)
        .filter(
            BlockProgress.id == progress_id,
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
        )
        .first()
    )


def get_by_enrollment_block(
    db: Session,
    enrollment_id: int,
    lesson_block_id: int,
    business_id: int,
):
    return (
        db.query(BlockProgress)
        .filter(
            BlockProgress.enrollment_id == enrollment_id,
            BlockProgress.lesson_block_id == lesson_block_id,
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
        )
        .first()
    )


def get_by_enrollment(
    db: Session,
    enrollment_id: int,
    business_id: int,
):
    return (
        db.query(BlockProgress)
        .filter(
            BlockProgress.enrollment_id == enrollment_id,
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
        )
        .order_by(BlockProgress.lesson_block_id)
        .all()
    )


def get_by_lesson_block_id(
    db: Session,
    lesson_block_id: int,
    business_id: int,
):
    return (
        db.query(BlockProgress)
        .filter(
            BlockProgress.lesson_block_id == lesson_block_id,
            BlockProgress.business_id == business_id,
            BlockProgress.deleted.is_(False),
        )
        .all()
    )


# Viejo
# def create(db: Session, progress: BlockProgress):
#   db.add(progress)
#  db.flush()
# db.refresh(progress)
# return progress


# def create_no_flush(db: Session, progress: BlockProgress):
#   db.add(progress)
#  db.commit()
# db.refresh(progress)
# return progress


# def update(db: Session, progress: BlockProgress):
#   db.commit()
#  db.refresh(progress)
# return progress


# def delete(db: Session, progress: BlockProgress):
#   progress.deleted = True
#  db.merge(progress)
# db.flush()
# return progress


# def soft_delete_by_enrollment(db: Session, enrollment_id: int):
#   db.query(BlockProgress).filter(BlockProgress.enrollment_id == enrollment_id).update(
#      {"deleted": True}
# )

"""
def get_by_id(db: Session, progress_id: int):
    return (
        db.query(BlockProgress)
        .filter(BlockProgress.id == progress_id, BlockProgress.deleted == False)
        .first()
    )


def get_by_enrollment_block(db: Session, enrollment_id: int, lesson_block_id: int):
    return (
        db.query(BlockProgress)
        .filter(
            BlockProgress.enrollment_id == enrollment_id,
            BlockProgress.lesson_block_id == lesson_block_id,
            BlockProgress.deleted == False,
        )
        .first()
    )


def get_by_enrollment(db: Session, enrollment_id: int):
    return (
        db.query(BlockProgress)
        .filter(
            BlockProgress.enrollment_id == enrollment_id, BlockProgress.deleted == False
        )
        .order_by(BlockProgress.lesson_block_id)
        .all()
    )


def get_by_lesson_block_id(db: Session, lesson_block_id: int):
    return (
        db.query(BlockProgress)
        .filter(
            BlockProgress.lesson_block_id == lesson_block_id,
            BlockProgress.deleted == False,
        )
        .all()
    )
"""

# def bulk_create(db: Session, progresses: list[BlockProgress]):
#   db.add_all(progresses)
#  db.flush()
# return progresses
