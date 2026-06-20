from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.lesson_block_type import LessonBlockType
from app.models.module import Module


def get_course_structure_rows(
    db: Session,
    course_id: int,
    business_id: int,
):
    return (
        db.query(
            Course.id.label("course_id"),
            Course.name.label("course_name"),
            Module.id.label("module_id"),
            Module.name.label("module_name"),
            Module.order.label("module_order"),
            Lesson.id.label("lesson_id"),
            Lesson.name.label("lesson_name"),
            Lesson.order.label("lesson_order"),
            LessonBlock.id.label("block_id"),
            LessonBlock.order.label("block_order"),
            LessonBlock.default.label("is_default"),
            LessonBlock.content.label("content"),
            LessonBlockType.name.label("block_type"),
        )
        .outerjoin(
            Module,
            and_(
                Module.course_id == Course.id,
                Module.deleted.is_(False),
            ),
        )
        .outerjoin(
            Lesson,
            and_(
                Lesson.module_id == Module.id,
                Lesson.deleted.is_(False),
            ),
        )
        .outerjoin(
            LessonBlock,
            and_(
                LessonBlock.lesson_id == Lesson.id,
                LessonBlock.deleted.is_(False),
            ),
        )
        .outerjoin(
            LessonBlockType,
            LessonBlockType.id == LessonBlock.block_type_id,
        )
        .filter(
            Course.id == course_id,
            Course.business_id == business_id,
            Course.deleted.is_(False),
        )
        .order_by(
            Module.order,
            Lesson.order,
            LessonBlock.order,
        )
        .all()
    )


def get_default_course_blocks(
    db: Session,
    course_id: int,
    business_id: int,
):
    return (
        db.query(
            LessonBlock.id.label("block_id"),
            LessonBlock.content.label("content"),
            LessonBlock.order.label("block_order"),
            LessonBlockType.name.label("block_type"),
        )
        .join(
            LessonBlockType,
            LessonBlockType.id == LessonBlock.block_type_id,
        )
        .filter(
            LessonBlock.course_id == course_id,
            LessonBlock.business_id == business_id,
            LessonBlock.default.is_(True),
            LessonBlock.deleted.is_(False),
        )
        .order_by(
            LessonBlock.order,
        )
        .all()
    )
