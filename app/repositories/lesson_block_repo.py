from operator import or_

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


def get_all_default_blocks_by_course_and_block_type(
    db: Session,
    course_id: int,
    block_type_id: int
):
    print("course_id:", course_id)
    print("block_type_id:", block_type_id)

    q1 = db.query(LessonBlock).filter(
        or_(LessonBlock.deleted.is_(False), LessonBlock.deleted.is_(None))
    )
    print("Solo no eliminados:", q1.count())

    q2 = q1.filter(LessonBlock.course_id == course_id)
    print("Por curso:", q2.count())

    q3 = q2.filter(LessonBlock.block_type_id == block_type_id)
    print("Por curso + tipo bloque:", q3.count())

    q4 = q3.filter(LessonBlock.default.is_(True))
    print("Por curso + tipo bloque + default:", q4.count())

    return q4.all()
