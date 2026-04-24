from sqlalchemy.orm import Session
from app.repositories import user_repo
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

def create_user(db: Session, data: UserCreate):

    if user_repo.get_by_username(db, data.username):
        raise ValueError("El nombre de usuario ya existe")

    data_dict = data.model_dump(exclude={"password", "role_id"})

    user = User(
        **data_dict,
        password=hash_password(data.password),
        role_id=2 # Asigna el rol de visitante por defecto
    )

    return user_repo.create(db, user)

def authenticate_user(db: Session, data: UserLogin):
    user = user_repo.get_by_username(db, data.username)
    if not user:
        return None
    if not verify_password(data.password, user.password):
        return None
    return user

def get_current_user(db: Session, user_id: int):
    return user_repo.me(db, user_id)

def get_all_users(db: Session):
    return user_repo.get_all(db)