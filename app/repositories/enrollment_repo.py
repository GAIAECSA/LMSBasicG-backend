from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================


# --- Crear ---
def create(db: Session, enrollment: Enrollment):
    db.add(enrollment)
    db.flush()
    return enrollment


def create_bulk(db: Session, enrollments: list[Enrollment]):
    db.add_all(enrollments)
    db.flush()
    return enrollments


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(db: Session, enrollment_id: int, business_id: int):
    db.query(Enrollment).filter(
        Enrollment.id == enrollment_id, Enrollment.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_user(db: Session, user_id: int, business_id: int):
    db.query(Enrollment).filter(
        Enrollment.user_id == user_id, Enrollment.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_course(db: Session, course_id: int, business_id: int):
    db.query(Enrollment).filter(
        Enrollment.course_id == course_id, Enrollment.business_id == business_id
    ).update({"deleted": True}, synchronize_session=False)


def delete_soft_by_subcategory(
    db: Session,
    subcategory_id: int,
    business_id: int,
):
    return (
        db.query(Enrollment)
        .join(
            Course,
            Enrollment.course_id == Course.id,
        )
        .filter(
            Course.subcategory_id == subcategory_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted == False,
        )
        .update(
            {"deleted": True},
            synchronize_session=False,
        )
    )


def delete_soft_by_category(
    db: Session,
    category_id: int,
    business_id: int,
):
    return (
        db.query(Enrollment)
        .join(
            Course,
            Enrollment.course_id == Course.id,
        )
        .join(
            Subcategory,
            Course.subcategory_id == Subcategory.id,
        )
        .filter(
            Subcategory.category_id == category_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted == False,
        )
        .update(
            {"deleted": True},
            synchronize_session=False,
        )
    )


# --- Consultas (Lectura) ---


def get_by_id(db: Session, enrollment_id: int, business_id: int):
    return (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course),
            joinedload(Enrollment.role),
        )
        .filter(
            Enrollment.id == enrollment_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted == False,
        )
        .first()
    )


def get_all_by_role(db: Session, role_id: int, business_id: int):
    return (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course),
            joinedload(Enrollment.role),
        )
        .filter(
            Enrollment.role_id == role_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted == False,
        )
        .all()
    )


def get_all_by_user(db: Session, user_id: int, business_id: int):
    return (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course),
            joinedload(Enrollment.role),
        )
        .filter(
            Enrollment.user_id == user_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted == False,
        )
    )


def get_all_by_course(db: Session, course_id: int, business_id: int):
    return (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course),
            joinedload(Enrollment.role),
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted == False,
        )
        .all()
    )


def get_all_by_course_and_role(
    db: Session, course_id: int, role_id: int, business_id: int
):
    return (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course),
            joinedload(Enrollment.role),
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.role_id == role_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted == False,
        )
        .all()
    )


def get_existing_enrollment(
    db: Session, course_id: int, user_id: int, business_id: int
):
    return (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted == False,
        )
        .first()
    )


# Viejos
# def create(db: Session, enrollment: Enrollment):
#   db.add(enrollment)
#  db.commit()
# db.refresh(enrollment)
# return enrollment


# def update(db: Session, enrollment: Enrollment):
#   db.merge(enrollment)
#  db.commit()
# db.refresh(enrollment)
# return enrollment


# def delete(db: Session, enrollment: Enrollment):
#   enrollment.deleted = True
#  db.merge(enrollment)
# db.commit()
# return enrollment


# def soft_delete(db: Session, enrollment: Enrollment):
#   enrollment.deleted = True
#  db.add(enrollment)
# db.flush()
# return enrollment


# def get_by_id(db: Session, enrollment_id: int):
#   return (
#      db.query(Enrollment)
#     .options(
#        joinedload(Enrollment.user),
#       joinedload(Enrollment.course),
#      joinedload(Enrollment.role),
# )
# .filter(Enrollment.id == enrollment_id, Enrollment.deleted == False)
# .first()
# )


# def get_all_by_course_id_and_role_id(db: Session, course_id: int, role_id: int):
#   return (
#      db.query(Enrollment)
##        joinedload(Enrollment.user),
#       joinedload(Enrollment.course),
#      joinedload(Enrollment.role),
# )
# .filter(
#   Enrollment.course_id == course_id,
#  Enrollment.role_id == role_id,
# Enrollment.deleted == False,
# )
# .all()
# )


# def get_all_by_course_id(db: Session, course_id: int):
#   return (
#      db.query(Enrollment)
#     .options(
#        joinedload(Enrollment.user),
#       joinedload(Enrollment.course),
#      joinedload(Enrollment.role),
# )
# .filter(Enrollment.course_id == course_id, Enrollment.deleted == False)
# .all()
# )


# def get_all_by_user(db: Session, user_id: int):
#   return (
#      db.query(Enrollment)
#     .options(
#        joinedload(Enrollment.user),
#       joinedload(Enrollment.course),
#      joinedload(Enrollment.role),
# )
# .filter(Enrollment.user_id == user_id, Enrollment.deleted == False)
# )


# def get_existing_enrollment(db: Session, course_id: int, user_id: int):
#   return (
#      db.query(Enrollment)
#     .filter(
#        Enrollment.user_id == user_id,
#       Enrollment.course_id == course_id,
#      Enrollment.deleted == False,
# )
#   .first()
# )#


# def get_all_by_role(db: Session, role_id: int):
#   return (
#      db.query(Enrollment)
#     .options(
#        joinedload(Enrollment.user),
#       joinedload(Enrollment.course),
#      joinedload(Enrollment.role),
# )
# .filter(Enrollment.role_id == role_id, Enrollment.deleted == False)
# .all()
# )


# def delete_by_course_id(db: Session, course_id: int):
#   enrollments = (
#      db.query(Enrollment)
#     .filter(Enrollment.course_id == course_id, Enrollment.deleted == False)
#    .all()
# )

# for enrollment in enrollments:
#   enrollment.deleted = True
#  db.merge(enrollment)

# db.commit()


# Metodos compuestos


# def create_flush(db: Session, enrollment: Enrollment):
#   db.add(enrollment)
#  db.flush()
# return enrollment
