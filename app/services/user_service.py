from django import db
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.helpers import blind_index
from app.models import enrollment
from app.models.user import User
from app.repositories import (
    attendance_repo,
    block_progress_repo,
    certificate_repo,
    enrollment_repo,
    forum_response_repo,
    homework_response_repo,
    quizz_response_repo,
    survey_response_repo,
    user_privacy_policy_repo,
    user_repo,
)
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
        role_id=2,  # Asigna el rol de visitante por defecto
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


def delete_user(db: Session, user_id: int):
    try:
        with db.begin():
            user = user_repo.get_by_id(db, user_id)
            if not user:
                raise Exception("Usuario no encontrado")
            user_repo.soft_delete(db, user)
            enrollments = enrollment_repo.get_all_by_user(db, user_id)
            for enrollment in enrollments:
                # Bloques
                block_progress_repo.soft_delete_by_enrollment(db, enrollment.id)
                # Respuestas
                homework_response_repo.soft_delete_by_enrollment(db, enrollment.id)
                quizz_response_repo.soft_delete_by_enrollment(db, enrollment.id)
                survey_response_repo.soft_delete_by_enrollment(db, enrollment.id)
                forum_response_repo.soft_delete_by_enrollment(db, enrollment.id)
                # Asistencias
                attendance_repo.soft_delete_by_enrollment(db, enrollment.id)
                enrollment_repo.soft_delete(db, enrollment)

            certificate_repo.soft_delete_by_user(db, user.id)
            user_privacy_policy_repo.soft_delete_by_user(db, user.id)

    except Exception as e:
        raise Exception(f"Error al eliminar el usuario: {str(e)}")
