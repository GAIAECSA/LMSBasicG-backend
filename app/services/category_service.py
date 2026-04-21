from sqlalchemy.orm import Session
from app.models.category import Category
from app.repositories import category_repo
from app.schemas.category import CategoryCreate, CategoryUpdate

def create_category(db: Session, data: CategoryCreate):
    existing = category_repo.get_by_name(db, data.name)
    if existing:
        raise Exception("La categoría ya existe")

    category = Category(**data.model_dump()) 
    
    return category_repo.create(db, category)

def update_category(db: Session, category_id: int, data: CategoryUpdate):
    category = category_repo.get_by_id(db, category_id)
    if not category:
        raise Exception("Categoría no encontrada")

    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] != category.name:
        existing = category_repo.get_by_name(db, update_data["name"])
        if existing:
            raise Exception("La categoría ya existe")

    for key, value in update_data.items():
        setattr(category, key, value)

    return category_repo.update(db, category)

def delete_category(db: Session, category_id: int):
    category = category_repo.get_by_id(db, category_id)
    if not category:
        raise Exception("Categoría no encontrada")

    return category_repo.delete(db, category)

def get_category(db: Session, category_id: int):
    category = category_repo.get_by_id(db, category_id)
    if not category:
        raise Exception("Categoría no encontrada")
    return category

def get_all_categories(db: Session):
    return category_repo.get_all(db)