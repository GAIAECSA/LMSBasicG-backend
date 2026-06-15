from sqlalchemy.orm import Session

from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, subcategory: Subcategory):
    db.add(subcategory)
    db.flush()
    return subcategory


def create_bulk(db: Session, subcategories: list[Subcategory]):
    db.add_all(subcategories)
    db.flush()
    return subcategories


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(db: Session, subcategory_id: int, business_id: int):
    db.query(Subcategory).filter(
        Subcategory.id == subcategory_id, Subcategory.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_category(db: Session, category_id: int, business_id: int):
    db.query(Subcategory).filter(
        Subcategory.category_id == category_id, Subcategory.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


# --- Consultas (Lectura) ---


def get_by_id(db: Session, subcategory_id: int, business_id: int):
    return (
        db.query(Subcategory)
        .filter(
            Subcategory.id == subcategory_id,
            Subcategory.business_id == business_id,
            Subcategory.deleted == False,
        )
        .first()
    )


def get_all(db: Session, business_id: int):
    return (
        db.query(Subcategory)
        .filter(Subcategory.business_id == business_id, Subcategory.deleted == False)
        .all()
    )


def get_by_category(db: Session, category_id: int, business_id: int):
    return (
        db.query(Subcategory)
        .filter(
            Subcategory.category_id == category_id,
            Subcategory.business_id == business_id,
            Subcategory.deleted == False,
        )
        .all()
    )


def get_by_name_and_category(
    db: Session, name: str, category_id: int, business_id: int
):
    return (
        db.query(Subcategory)
        .filter(
            Subcategory.name == name,
            Subcategory.category_id == category_id,
            Subcategory.business_id == business_id,
            Subcategory.deleted == False,
        )
        .first()
    )


# Viejos
# def create(db: Session, subcategory: Subcategory):
#   db.add(subcategory)
#  db.commit()
# db.refresh(subcategory)
# return subcategory


# def update(db: Session, subcategory: Subcategory):
#   db.merge(subcategory)
#  db.commit()
# db.refresh(subcategory)
# return subcategory


# def delete(db: Session, subcategory: Subcategory):
#   subcategory.deleted = True
#  db.merge(subcategory)
# db.commit()
# return subcategory


# def get_by_id(db: Session, subcategory_id: int):
#   return (
#      db.query(Subcategory)
#     .filter(Subcategory.id == subcategory_id, Subcategory.deleted == False)
#    .first()
# )


# def get_by_category_id(db: Session, category_id: int):
#   return (
#      db.query(Subcategory)
#     .filter(Subcategory.category_id == category_id, Subcategory.deleted == False)
#    .all()
# )


# def get_all(db: Session):
#   return db.query(Subcategory).filter(Subcategory.deleted == False).all()


# def get_by_name_and_category(db: Session, name: str, category_id: int):
#   return (
#      db.query(Subcategory)
#     .filter(
#        Subcategory.name == name,
#       Subcategory.category_id == category_id,
#      Subcategory.deleted == False,
# )
# .first()
# )
