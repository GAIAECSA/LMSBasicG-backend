from typing import List, Optional

from sqlalchemy.orm import Session

from app.constants import constants_roles
from app.core.security import hash_password, verify_password
from app.helpers import blind_index
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

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def create_user(
    db: Session,
    data: UserCreate,
    business_id: int,
) -> User:
    with db.begin():
        existing_users = user_repo.get_by_username_or_email(
            db=db,
            username=data.username,
            email=data.email,
            business_id=business_id,
        )

        if any(user.username == data.username for user in existing_users):
            raise UserAlreadyExistsError("El nombre de usuario ya existe")

        if data.email and any(user.email == data.email for user in existing_users):
            raise UserAlreadyExistsError("El email de usuario ya existe")

        data_dict = data.model_dump(
            exclude={"password", "role_id", "domain"}, exclude_unset=True
        )

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
            idnumber_hash=idnumber_hash,
            phone_number_hash=phone_number_hash,
            password=hash_password(data.password),
            role_id=constants_roles.VISITOR_ROLE,
            business_id=business_id,
        )

        return user_repo.create(db, user)


def authenticate_user(db: Session, data: UserLogin, business_id: int) -> Optional[User]:
    user = user_repo.get_by_username(db, data.username, business_id)
    if not user:
        return None
    if not verify_password(data.password, user.password):
        return None
    return user


def update_user(
    db: Session,
    user_id: int,
    data: UserUpdate,
    business_id: int,
) -> User:
    with db.begin():
        user = user_repo.get_by_id(db, user_id, business_id)

        if not user:
            raise UserNotFoundError("Usuario no encontrado")

        update_data = data.model_dump(exclude_unset=True)

        username = update_data.get("username")
        email = update_data.get("email")

        if username or email:
            existing_users = user_repo.get_by_username_or_email(
                db=db,
                username=username,
                email=email,
                business_id=business_id,
            )

            for existing_user in existing_users:
                if existing_user.id == user_id:
                    continue

                if username and existing_user.username == username:
                    raise UserAlreadyExistsError("El nombre de usuario ya existe")

                if email and existing_user.email == email:
                    raise UserAlreadyExistsError("El email ya existe")

        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        if "idnumber" in update_data:
            update_data["idnumber_hash"] = (
                blind_index.generate_blind_index(update_data["idnumber"])
                if update_data["idnumber"]
                else None
            )

        if "phone_number" in update_data:
            update_data["phone_number_hash"] = (
                blind_index.generate_blind_index(update_data["phone_number"])
                if update_data["phone_number"]
                else None
            )

        for key, value in update_data.items():
            setattr(user, key, value)

        return user


def get_current_user(db: Session, user_id: int, business_id: int) -> Optional[User]:
    return user_repo.get_by_id(db, user_id, business_id)


def get_all_users(db: Session, business_id: int) -> List[User]:
    return user_repo.get_all(db, business_id)


def delete_user(db: Session, user_id: int, business_id: int) -> None:
    with db.begin():
        user = user_repo.get_by_id(db, user_id, business_id)
        if not user:
            raise UserNotFoundError("Usuario no encontrado")

        cascade_steps = [
            homework_response_repo.delete_soft_by_user,
            quizz_response_repo.delete_soft_by_user,
            survey_response_repo.delete_soft_by_user,
            forum_response_repo.delete_soft_by_user,
            attendance_repo.delete_soft_by_user,
            block_progress_repo.delete_soft_by_user,
            certificate_repo.delete_soft_by_user,
            enrollment_repo.delete_soft_by_user,
            user_privacy_policy_repo.delete_soft_by_user,
        ]

        for step in cascade_steps:
            step(db, user_id, business_id)

        user_repo.delete_soft_by_id(db, user_id, business_id)


# Viejos
"""
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
"""
