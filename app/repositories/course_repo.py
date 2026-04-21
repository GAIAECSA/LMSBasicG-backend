from sqlalchemy.orm import Session
from app.models.course import Course

def create(db: Session, course: Course):
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def update(db: Session, course: Course):
    db.merge(course)
    db.commit()
    db.refresh(course)
    return course

def delete(db: Session, course: Course):
    course.deleted = True
    db.merge(course)
    db.commit()
    return course

def get_by_id(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id, Course.deleted == False).first()

def get_by_subcategory_id(db: Session, subcategory_id: int):
    return db.query(Course).filter(Course.subcategory_id == subcategory_id, Course.deleted == False).all()

def get_all(db: Session):
    return db.query(Course).filter(Course.deleted == False).all()
