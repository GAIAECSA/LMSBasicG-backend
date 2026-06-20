from sqlalchemy.orm import Session

from app.models.module import Module
from app.repositories import (
    block_progress_repo,
    forum_response_repo,
    homework_response_repo,
    lesson_block_repo,
    lesson_repo,
    module_repo,
    quizz_response_repo,
    survey_response_repo,
)
from app.schemas.module import ModuleCreate, ModuleUpdate

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class ModuleNotFoundError(Exception):
    pass


class CategoryAlreadyExistsError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def create_module(db: Session, data: ModuleCreate, business_id: int):
    with db.begin():
        module = Module(**data.model_dump(), business_id=business_id)
        return module_repo.create(db, module)


def update_module(db: Session, module_id: int, data: ModuleUpdate, business_id: int):
    with db.begin():
        module = module_repo.get_by_id(db, module_id, business_id)
        if not module:
            raise ModuleNotFoundError("Módulo no encontrado")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(module, key, value)

        return module


def delete_module(db: Session, module_id: int, business_id: int):
    with db.begin():
        module = module_repo.get_by_id(db, module_id, business_id)
        if not module:
            raise ModuleNotFoundError("Módulo no encontrado")

        cascade_steps = [
            # Blocks
            homework_response_repo.delete_soft_by_module(),
            forum_response_repo.delete_soft_by_module(),
            survey_response_repo.delete_soft_by_module(),
            quizz_response_repo.delete_soft_by_module(),
            # Navigation
            lesson_block_repo.delete_soft_by_module(),
            block_progress_repo.delete_soft_by_module(),
            lesson_repo.delete_soft_by_module(),
        ]
        for step in cascade_steps:
            step(db, module_id, business_id)

        return module_repo.delete_soft_by_id(db, module, business_id)


def get_module(db: Session, module_id: int, business_id: int):
    module = module_repo.get_by_id(db, module_id, business_id)
    if not module:
        raise ModuleNotFoundError("Módulo no encontrado")
    return module


def get_modules_by_course(db: Session, course_id: int):
    return module_repo.get_by_course_id(db, course_id)


"""
def create_module(db: Session, data: ModuleCreate):
    module = Module(**data.model_dump())
    return module_repo.create(db, module)


def update_module(db: Session, module_id: int, data: ModuleUpdate):
    module = module_repo.get_by_id(db, module_id)
    if not module:
        raise Exception("Módulo no encontrado")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(module, key, value)

    return module_repo.update(db, module)


def delete_module(db: Session, module_id: int):
    module = module_repo.get_by_id(db, module_id)
    if not module:
        raise Exception("Módulo no encontrado")
    return module_repo.delete(db, module)


def get_module(db: Session, module_id: int):
    return module_repo.get_by_id(db, module_id)


def get_modules_by_course(db: Session, course_id: int):
    return module_repo.get_by_course_id(db, course_id)
"""
