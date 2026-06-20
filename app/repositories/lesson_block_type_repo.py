from sqlalchemy.orm import Session

from app.models.lesson_block_type import LessonBlockType


def get_by_id(db: Session, lesson_block_type_id: int):
    return (
        db.query(LessonBlockType)
        .filter(
            LessonBlockType.id == lesson_block_type_id, LessonBlockType.deleted == False
        )
        .first()
    )


def get_all(db: Session):
    return db.query(LessonBlockType).filter(LessonBlockType.deleted == False).all()
