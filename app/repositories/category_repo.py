from sqlalchemy.orm import Session

from app.models.category import Category

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, category: Category):
    db.add(category)
    db.flush()
    return category


def create_bulk(db: Session, categories: list[Category]):
    db.add_all(categories)
    db.flush()
    return categories


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(db: Session, category_id: int, business_id: int):
    db.query(Category).filter(
        Category.id == category_id, Category.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


# --- Consultas (Lectura) ---


def get_by_id(db: Session, category_id: int, business_id: int):
    return (
        db.query(Category)
        .filter(
            Category.id == category_id,
            Category.business_id == business_id,
            Category.deleted == False,
        )
        .first()
    )


def get_all(db: Session, business_id):
    return (
        db.query(Category)
        .filter(Category.business_id == business_id, Category.deleted == False)
        .all()
    )


def get_by_name(db: Session, name: str, business_id):
    return (
        db.query(Category)
        .filter(
            Category.name == name,
            Category.business_id == business_id,
            Category.deleted == False,
        )
        .first()
    )


# Viejo
# def create(db: Session, category: Category):
#   db.add(category)
#  db.commit()
# db.refresh(category)
# return category


# def update(db: Session, category: Category):
#   db.merge(category)
#  db.commit()
# db.refresh(category)
# return category


# def delete(db: Session, category: Category):
#   category.deleted = True
#  db.merge(category)
# db.commit()
# return category


# def get_by_id(db: Session, category_id: int):
#   return (
#      db.query(Category)
#     .filter(Category.id == category_id, Category.deleted == False)
#    .first()
# )


# def get_all(db: Session):
#   return db.query(Category).filter(Category.deleted == False).all()


# def get_by_name(db: Session, name: str):
#   return (
#      db.query(Category)
#     .filter(Category.name == name, Category.deleted == False)
#    .first()
# )
