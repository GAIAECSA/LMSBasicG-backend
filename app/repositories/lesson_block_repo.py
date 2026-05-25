from sqlalchemy.orm import Session
from app.models.lesson_block import LessonBlock
from sqlalchemy.orm import Session, joinedload


def create(db: Session, lesson_block: LessonBlock):
    db.add(lesson_block)
    db.commit()
    db.refresh(lesson_block)
    return lesson_block


def update(db: Session, lesson_block: LessonBlock):
    db.merge(lesson_block)
    db.commit()
    db.refresh(lesson_block)
    return lesson_block


def delete(db: Session, lesson_block: LessonBlock):
    lesson_block.deleted = True
    db.merge(lesson_block)
    db.commit()
    return lesson_block


def get_by_id(db: Session, lesson_block_id: int):
    return (
        db.query(LessonBlock)
        .options(joinedload(LessonBlock.lesson_block_type))
        .filter(LessonBlock.id == lesson_block_id, LessonBlock.deleted == False)
        .first()
    )


def get_all_by_lesson_id(db: Session, lesson_id: int):
    return (
        db.query(LessonBlock)
        .options(joinedload(LessonBlock.lesson_block_type))
        .filter(LessonBlock.deleted == False, LessonBlock.lesson_id == lesson_id)
        .all()
    )


def create_all(db: Session, lesson_blocks: list[LessonBlock]):
    db.add_all(lesson_blocks)
    db.flush()
    return lesson_blocks


def get_default_by_course_id(db: Session, course_id: int):
    return (
        db.query(LessonBlock)
        .filter(
            LessonBlock.deleted == False,
            LessonBlock.course_id == course_id,
            LessonBlock.default == True,
        )
        .all()
    )


def delete_default_by_course_id(
    db: Session,
    course_id: int,
):
    db.query(LessonBlock).filter(
        LessonBlock.deleted == False,
        LessonBlock.course_id == course_id,
        LessonBlock.default == True,
    ).update(
        {"deleted": True},
        synchronize_session=False,
    )

    db.flush()
