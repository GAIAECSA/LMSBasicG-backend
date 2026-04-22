from sqlalchemy.orm import Session
from app.models.lesson_block_type import LessonBlockType
from app.repositories import lesson_block_type_repo
from app.schemas.lesson_block_type import LessonBlockTypeCreate, LessonBlockTypeUpdate


def create_lesson_block_type(db: Session, data: LessonBlockTypeCreate):
    existing = lesson_block_type_repo.get_by_name(db, data.name)
    if existing:
        raise Exception("El tipo de bloque de lección ya existe")

    lesson_block_type = LessonBlockType(**data.model_dump()) 
    
    return lesson_block_type_repo.create(db, lesson_block_type)

def update_lesson_block_type(db: Session, lesson_block_type_id: int, data: LessonBlockTypeUpdate):
    lesson_block_type = lesson_block_type_repo.get_by_id(db, lesson_block_type_id)
    if not lesson_block_type:
        raise Exception("Tipo de bloque de lección no encontrado")

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] != lesson_block_type.name:
        existing = lesson_block_type_repo.get_by_name(db, update_data["name"])
        if existing:
            raise Exception("El tipo de bloque de lección ya existe")

    for key, value in update_data.items():
        setattr(lesson_block_type, key, value)

    return lesson_block_type_repo.update(db, lesson_block_type)

def delete_lesson_block_type(db: Session, lesson_block_type_id: int):
    lesson_block_type = lesson_block_type_repo.get_by_id(db, lesson_block_type_id)
    if not lesson_block_type:
        raise Exception("Tipo de bloque de lección no encontrado")

    return lesson_block_type_repo.delete(db, lesson_block_type)

def get_lesson_block_type(db: Session, lesson_block_type_id: int):
    lesson_block_type = lesson_block_type_repo.get_by_id(db, lesson_block_type_id)
    if not lesson_block_type:
        raise Exception("Tipo de bloque de lección no encontrado")
    return lesson_block_type

def get_all_lesson_block_types(db: Session):
    return lesson_block_type_repo.get_all(db)