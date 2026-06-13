from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, course: Course):
    db.add(course)
    db.flush()
    return course


def create_bulk(db: Session, courses: list[Course]):
    db.add_all(courses)
    db.flush()
    return courses


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(db: Session, course_id: int):
    db.query(Course).filter(Course.id == course_id).update(
        {"deleted": True}, synchronize_session=False
    )


def delete_soft_by_subcategory(db: Session, subcategory_id: int):
    db.query(Course).filter(Course.subcategory_id == subcategory_id).update(
        {"deleted": True}, synchronize_session=False
    )


def delete_soft_by_category(db: Session, category_id: int) -> None:
    db.query(Course).filter(
        Course.subcategory_id.in_(
            db.query(Subcategory.id).filter(Subcategory.category_id == category_id)
        )
    ).update({"deleted": True}, synchronize_session=False)


# --- Consultas (Lectura) ---


def get_by_id(db: Session, course_id: int):
    return (
        db.query(Course).filter(Course.id == course_id, Course.deleted == False).first()
    )


def get_by_subcategory_id(db: Session, subcategory_id: int):
    return (
        db.query(Course)
        .filter(Course.subcategory_id == subcategory_id, Course.deleted == False)
        .all()
    )


def get_all(db: Session):
    return db.query(Course).filter(Course.deleted == False).all()


def get_by_name_and_subcategory(db: Session, name: str, subcategory_id: int):
    return (
        db.query(Course)
        .filter(
            Course.name == name,
            Course.subcategory_id == subcategory_id,
            Course.deleted == False,
        )
        .first()
    )


# Viejitos
# def delete(db: Session, course: Course):
#   course.deleted = True
#  db.merge(course)
# db.commit()
# return course


# Metodos compuestos


# def create(db: Session, course: Course):
#   db.add(course)
#  db.flush()
# return course


# def update(db: Session, course: Course):

#   course = db.merge(course)

# db.flush()
#  db.refresh(course)

# return course
