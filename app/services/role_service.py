from sqlalchemy.orm import Session
from app.models.role import Role
from app.repositories import role_repo

def create_role(db: Session, name: str):
    existing = role_repo.get_by_name(db, name)
    if existing:
        raise Exception("El rol ya existe")

    role = Role(name=name)
    return role_repo.create(db, role)

def get_role_by_id(db: Session, role_id: int):
    return role_repo.get_by_id(db, role_id)

def get_role_by_name(db: Session, name: str):
    return role_repo.get_by_name(db, name)