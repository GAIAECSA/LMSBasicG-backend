from sqlalchemy.orm import Session, joinedload
from app.models.enrollment import Enrollment

def create(db: Session, enrollment: Enrollment):
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

def update(db: Session, enrollment: Enrollment):
    db.merge(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

def delete(db: Session, enrollment: Enrollment):
    enrollment.deleted = True
    db.merge(enrollment)
    db.commit()
    return enrollment

def get_by_id(db: Session, enrollment_id: int):
    return (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course),
            joinedload(Enrollment.role)
        )
        .filter(
            Enrollment.id == enrollment_id,
            Enrollment.deleted == False
        )
        .first()
    )

def get_all_by_course_id_and_role_id(db: Session, course_id: int, role_id: int):
    return (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course),
            joinedload(Enrollment.role)
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.role_id == role_id,
            Enrollment.deleted == False
        )
        .all()
    )

def get_all_by_user(db: Session, user_id):
    return (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course),
            joinedload(Enrollment.role)
        )
        .filter(Enrollment.user_id == user_id, Enrollment.deleted == False)
    )

def get_all_by_role(db: Session, role_id: int):
    return (
        db.query(Enrollment)
        .options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course),
            joinedload(Enrollment.role)
        )
        .filter(Enrollment.role_id == role_id, Enrollment.deleted == False)
        .all()
    )

