from sqlalchemy.orm import Session

from app.models.user import User


def get_by_username(db: Session, username: str):
    return (
        db.query(User).filter(User.username == username, User.deleted == False).first()
    )


def create(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User):
    db.merge(user)
    db.commit()
    db.refresh(user)
    return user


def me(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.deleted == False).first()


def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.deleted == False).first()


def get_all(db: Session):
    return db.query(User).filter(User.deleted == False).all()


def get_by_email_or_idnumber_hash(db: Session, email: str, id_number_hash: str):
    return (
        db.query(User)
        .filter(
            (User.email == email) | (User.idnumber_hash == id_number_hash),
            User.deleted == False,
        )
        .first()
    )


def create_flush(db: Session, user: User):
    db.add(user)
    db.flush()
    return user


def soft_delete(db: Session, user: User):
    user.deleted = True
    db.add(user)
    db.flush()
    return user
