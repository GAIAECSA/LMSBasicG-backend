from sqlalchemy.orm import Session
from app.models.user import User

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username, User.deleted == False).first()

def create(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def me(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.deleted == False).first()

def get_all(db: Session):
    return db.query(User).filter(User.deleted == False).all()