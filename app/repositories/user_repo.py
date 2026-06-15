from sqlalchemy.orm import Session

from app.models.user import User

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================


# --- Crear ---
def create(db: Session, user: User):
    db.add(user)
    db.flush()
    return user


def create_bulk(db: Session, users: list[User]):
    db.add_all(users)
    db.flush()
    return users


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(db: Session, user_id: int, business_id: int):
    db.query(User).filter(User.id == user_id, User.business_id == business_id).update(
        {"deleted": True}, synchronize_session=False
    )


# --- Consultas (Lectura) ---


def get_by_id(db: Session, user_id: int, business_id: int):
    return (
        db.query(User)
        .filter(
            User.id == user_id, User.deleted == False, User.business_id == business_id
        )
        .first()
    )


def get_all(db: Session, business_id: int):
    return (
        db.query(User)
        .filter(User.deleted == False, User.business_id == business_id)
        .all()
    )


def get_by_username(db: Session, username: str, business_id: int):
    return (
        db.query(User)
        .filter(
            User.username == username,
            User.business_id == business_id,
            User.deleted == False,
        )
        .first()
    )


def get_user_by_email(db: Session, email: str, business_id: int):
    return (
        db.query(User)
        .filter(
            User.business_id == business_id,
            User.email == email,
            User.deleted.is_(False),
        )
        .first()
    )


def get_by_email_or_idnumber_hash_or_username(
    db: Session, email: str, id_number_hash: str, username: str, business_id: int
):
    return (
        db.query(User)
        .filter(
            (User.email == email)
            | (User.idnumber_hash == id_number_hash)
            | (User.username == username)
            | (User.business_id == business_id),
            User.deleted == False,
        )
        .first()
    )


# Viejos
# def get_by_username(db: Session, username: str):
#   return (
#      db.query(User).filter(User.username == username, User.deleted == False).first()
# )


# def create(db: Session, user: User):
#   db.add(user)
#  db.commit()
# db.refresh(user)
# return user


# def update(db: Session, user: User):
#   db.merge(user)
#  db.commit()
# db.refresh(user)
# return user


# def me(db: Session, user_id: int):
#   return db.query(User).filter(User.id == user_id, User.deleted == False).first()


# def get_by_id(db: Session, user_id: int):
#   return db.query(User).filter(User.id == user_id, User.deleted == False).first()


# def get_all(db: Session):
#   return db.query(User).filter(User.deleted == False).all()


# def get_by_email_or_idnumber_hash_or_username(
#   db: Session, email: str, id_number_hash: str, username: str
# ):
#   return (
#      db.query(User)
#     .filter(
#        (User.email == email)
#       | (User.idnumber_hash == id_number_hash)
#      | (User.username == username),
#     User.deleted == False,
# )
# .first()
# )


# def create_flush(db: Session, user: User):
#   db.add(user)
#  db.flush()
# return user


# def soft_delete(db: Session, user: User):
#   user.deleted = True
#  db.add(user)
# db.flush()
# return user
