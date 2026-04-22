from sqlalchemy.orm import Session
from app.models.lesson_block_type import LessonBlockType

def create(db: Session, lesson_block_type: LessonBlockType):
    db.add(lesson_block_type)
    db.commit()
    db.refresh(lesson_block_type)
    return lesson_block_type

def update(db: Session, lesson_block_type: LessonBlockType):
    db.merge(lesson_block_type)
    db.commit()
    db.refresh(lesson_block_type)
    return lesson_block_type

def delete(db: Session, lesson_block_type: LessonBlockType):
    lesson_block_type.deleted = True
    db.merge(lesson_block_type)
    db.commit()
    return lesson_block_type

def get_by_id(db: Session, lesson_block_type_id: int):
    return db.query(LessonBlockType).filter(LessonBlockType.id == lesson_block_type_id, LessonBlockType.deleted == False).first()

def get_all(db: Session):
    return db.query(LessonBlockType).filter(LessonBlockType.deleted == False).all()