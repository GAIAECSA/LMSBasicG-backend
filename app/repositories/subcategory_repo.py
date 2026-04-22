from sqlalchemy.orm import Session
from app.models.subcategory import Subcategory

def create(db: Session, subcategory: Subcategory):
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory

def update(db: Session, subcategory: Subcategory):
    db.merge(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory

def delete(db: Session, subcategory: Subcategory):
    subcategory.deleted = True
    db.merge(subcategory)
    db.commit()
    return subcategory

def get_by_id(db: Session, category_id: int):
    return db.query(Subcategory).filter(Subcategory.id == category_id, Subcategory.deleted == False).first()

def get_by_category_id(db: Session, category_id: int):
    return db.query(Subcategory).filter(Subcategory.category_id == category_id, Subcategory.deleted == False).all()

def get_all(db: Session):
    return db.query(Subcategory).filter(Subcategory.deleted == False).all()

def get_by_name_and_category(db: Session, name: str, category_id: int):
    return db.query(Subcategory).filter(
        Subcategory.name == name,
        Subcategory.category_id == category_id,
        Subcategory.deleted == False
    ).first()