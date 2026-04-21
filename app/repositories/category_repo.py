from sqlalchemy.orm import Session
from app.models.category import Category

def create(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update(db: Session, category: Category):
    db.merge(category)
    db.commit()
    db.refresh(category)
    return category

def delete(db: Session, category: Category):
    category.deleted = True
    db.merge(category)
    db.commit()
    return category

def get_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id, Category.deleted == False).first()

def get_all(db: Session):
    return db.query(Category).filter(Category.deleted == False).all()

def get_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name, Category.deleted == False).first()