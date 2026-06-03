from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.helpers import blind_index
from app.models.user import User
from app.repositories import user_repo
from app.schemas.user import UserCreate, UserLogin, UserUpdate


def create_user(db: Session, data: UserCreate):
    if user_repo.get_by_username(db, data.username):
        raise ValueError("El nombre de usuario ya existe")

    data_dict = data.model_dump(exclude={"password", "role_id"})

    # Calculamos los Blind Indexes (Hashes) en la capa de servicio
    idnumber_hash = (
        blind_index.generate_blind_index(data.idnumber) if data.idnumber else None
    )
    phone_number_hash = (
        blind_index.generate_blind_index(data.phone_number)
        if data.phone_number
        else None
    )

    user = User(
        **data_dict,
        idnumber_hash=idnumber_hash,  # Asignamos el hash de la cédula
        phone_number_hash=phone_number_hash,  # Asignamos el hash del teléfono
        password=hash_password(data.password),
        role_id=2  # Asigna el rol de visitante por defecto
    )

    # El repositorio guarda el objeto sin saber nada de los hashes
    return user_repo.create(db, user)


def authenticate_user(db: Session, data: UserLogin):
    user = user_repo.get_by_username(db, data.username)
    if not user:
        return None
    if not verify_password(data.password, user.password):
        return None
    return user


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise Exception("Usuario no encontrado")

    update_data = data.model_dump(exclude_unset=True)

    if "username" in update_data:
        existing_user = user_repo.get_by_username(db, update_data["username"])
        if existing_user and existing_user.id != user_id:
            raise ValueError("El nombre de usuario ya existe")

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    update_data = {k: v for k, v in update_data.items() if v is not None}

    for key, value in update_data.items():
        setattr(user, key, value)

        if key == "idnumber":
            user.idnumber_hash = blind_index.generate_blind_index(value)
        elif key == "phone_number":
            user.phone_number_hash = blind_index.generate_blind_index(value)

    return user_repo.update(db, user)


def get_current_user(db: Session, user_id: int):
    return user_repo.me(db, user_id)


def get_all_users(db: Session):
    return user_repo.get_all(db)
