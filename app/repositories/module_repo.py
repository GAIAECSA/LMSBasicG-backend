from sqlalchemy.orm import Session
from app.models.module import Module

def create(db: Session, module: Module):
    db.add(module)
    db.commit()
    db.refresh(module)
    return module

def update(db: Session, module: Module):
    db.merge(module)
    db.commit()
    db.refresh(module)
    return module

def delete(db: Session, module: Module):
    module.deleted = True
    db.merge(module)
    db.commit()
    return module

def get_by_id(db: Session, module_id: int):
    return db.query(Module).filter(Module.id == module_id, Module.deleted == False).first()

def get_by_course_id(db: Session, course_id: int):
    return db.query(Module).filter(Module.course_id == course_id, Module.deleted == False).all()


