from sqlalchemy.orm import Session
from app.models.subcategory import Subcategory
from app.repositories import subcategory_repo
from app.schemas.subcategory import SubcategoryCreate, SubcategoryUpdate

def create_subcategory(db: Session, data: SubcategoryCreate):
    existing = subcategory_repo.get_by_name_and_category(db, data.name, data.category_id)
    if existing:
        raise Exception("La subcategoría ya existe en esta categoría")

    subcategory = Subcategory(**data.model_dump())
    return subcategory_repo.create(db, subcategory)

def update_subcategory(db: Session, subcategory_id: int, data: SubcategoryUpdate):
    subcategory = subcategory_repo.get_by_id(db, subcategory_id)
    if not subcategory:
        raise Exception("Subcategoría no encontrada")

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] != subcategory.name:
        existing = subcategory_repo.get_by_name_and_category(db, update_data["name"], subcategory.category_id)
        if existing:
            raise Exception("La subcategoría ya existe en esta categoría")
    
    for key, value in update_data.items():
        setattr(subcategory, key, value)

    return subcategory_repo.update(db, subcategory)

def delete_subcategory(db: Session, subcategory_id: int):
    subcategory = subcategory_repo.get_by_id(db, subcategory_id)
    if not subcategory:
        raise Exception("Subcategoría no encontrada")

    return subcategory_repo.delete(db, subcategory)

def get_subcategory(db: Session, subcategory_id: int):
    subcategory = subcategory_repo.get_by_id(db, subcategory_id)
    if not subcategory:
        raise Exception("Subcategoría no encontrada")
    return subcategory

def get_subcategories_by_category(db: Session, category_id: int):
    return subcategory_repo.get_by_category_id(db, category_id)