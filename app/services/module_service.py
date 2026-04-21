from sqlalchemy.orm import Session
from app.models.module import Module
from app.repositories import module_repo
from app.schemas.module import ModuleCreate, ModuleUpdate

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