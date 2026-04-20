from sqlalchemy.orm import Session
from app.models.role import Role

def create(db: Session, role: Role):
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def get_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()

def get_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()