from sqlalchemy.orm import Session
from app.models.lesson import Lesson

def create(db: Session, lesson: Lesson):
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson

def update(db: Session, lesson: Lesson):
    db.merge(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson

def delete(db: Session, lesson: Lesson):
    lesson.deleted = True
    db.merge(lesson)
    db.commit()
    return lesson

def get_by_id(db: Session, lesson_id: int):
    return db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.deleted == False).first()

def get_by_module_id(db: Session, module_id: int):
    return db.query(Lesson).filter(Lesson.module_id == module_id, Lesson.deleted == False).all()
