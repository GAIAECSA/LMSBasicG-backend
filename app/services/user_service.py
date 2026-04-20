from sqlalchemy.orm import Session
from app.repositories import user_repo, role_repo
from app.core.security import hash_password, verify_password
from app.models.user import User

def create_user(db: Session, email: str, password: str):
    role = role_repo.get_by_name(db, "VISITANTE")

    user = User(
        email=email,
        password=hash_password(password),
        role_id=role.id
    )

    return user_repo.create(db, user)

def authenticate_user(db: Session, email: str, password: str):
    user = user_repo.get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user