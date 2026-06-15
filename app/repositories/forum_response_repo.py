from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.forum_response import ForumResponse
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.module import Module
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, forum_response: ForumResponse) -> ForumResponse:
    db.add(forum_response)
    db.flush()
    return forum_response


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(
    db: Session,
    forum_response_id: int,
    business_id: int,
) -> None:
    (
        db.query(ForumResponse)
        .filter(
            ForumResponse.id == forum_response_id,
            ForumResponse.business_id == business_id,
            ForumResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )

    (
        db.query(ForumResponse)
        .filter(
            ForumResponse.forum_response_id == forum_response_id,
            ForumResponse.business_id == business_id,
            ForumResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_enrollment(
    db: Session,
    enrollment_id: int,
    business_id: int,
) -> None:
    (
        db.query(ForumResponse)
        .filter(
            ForumResponse.enrollment_id == enrollment_id,
            ForumResponse.business_id == business_id,
            ForumResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson_block(
    db: Session,
    lesson_block_id: int,
    business_id: int,
) -> None:
    (
        db.query(ForumResponse)
        .filter(
            ForumResponse.lesson_block_id == lesson_block_id,
            ForumResponse.business_id == business_id,
            ForumResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson(
    db: Session,
    lesson_id: int,
    business_id: int,
) -> None:
    (
        db.query(ForumResponse)
        .filter(
            ForumResponse.business_id == business_id,
            ForumResponse.deleted.is_(False),
            ForumResponse.lesson_block_id.in_(
                db.query(LessonBlock.id).filter(
                    LessonBlock.lesson_id == lesson_id,
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_module(
    db: Session,
    module_id: int,
    business_id: int,
) -> None:
    (
        db.query(ForumResponse)
        .filter(
            ForumResponse.business_id == business_id,
            ForumResponse.deleted.is_(False),
            ForumResponse.lesson_block_id.in_(
                db.query(LessonBlock.id)
                .join(Lesson)
                .filter(
                    Lesson.module_id == module_id,
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_course(
    db: Session,
    course_id: int,
    business_id: int,
) -> None:
    (
        db.query(ForumResponse)
        .filter(
            ForumResponse.business_id == business_id,
            ForumResponse.deleted.is_(False),
            ForumResponse.lesson_block_id.in_(
                db.query(LessonBlock.id)
                .join(Lesson)
                .join(Module)
                .filter(
                    Module.course_id == course_id,
                    Module.business_id == business_id,
                    Module.deleted.is_(False),
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_subcategory(
    db: Session,
    subcategory_id: int,
    business_id: int,
) -> None:
    (
        db.query(ForumResponse)
        .filter(
            ForumResponse.business_id == business_id,
            ForumResponse.deleted.is_(False),
            ForumResponse.lesson_block_id.in_(
                db.query(LessonBlock.id)
                .join(Lesson)
                .join(Module)
                .join(Course)
                .filter(
                    Course.subcategory_id == subcategory_id,
                    Course.business_id == business_id,
                    Course.deleted.is_(False),
                    Module.business_id == business_id,
                    Module.deleted.is_(False),
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_category(
    db: Session,
    category_id: int,
    business_id: int,
) -> None:
    (
        db.query(ForumResponse)
        .filter(
            ForumResponse.business_id == business_id,
            ForumResponse.deleted.is_(False),
            ForumResponse.lesson_block_id.in_(
                db.query(LessonBlock.id)
                .join(Lesson)
                .join(Module)
                .join(Course)
                .join(Subcategory)
                .filter(
                    Subcategory.category_id == category_id,
                    Subcategory.business_id == business_id,
                    Subcategory.deleted.is_(False),
                    Course.business_id == business_id,
                    Course.deleted.is_(False),
                    Module.business_id == business_id,
                    Module.deleted.is_(False),
                    Lesson.business_id == business_id,
                    Lesson.deleted.is_(False),
                    LessonBlock.business_id == business_id,
                    LessonBlock.deleted.is_(False),
                )
            ),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


# --- Consultas (Lectura) ---


def get_by_id(db: Session, forum_response_id: int, business_id: int):
    return (
        db.query(ForumResponse)
        .filter(
            ForumResponse.id == forum_response_id,
            ForumResponse.business_id == business_id,
            ForumResponse.deleted == False,
        )
        .first()
    )


def get_all(db: Session, business_id: int):
    return (
        db.query(ForumResponse)
        .filter(
            ForumResponse.business_id == business_id, ForumResponse.deleted == False
        )
        .all()
    )


def get_all_by_enrollment(db: Session, enrollment_id: int, business_id: int):
    return (
        db.query(ForumResponse)
        .filter(
            ForumResponse.enrollment_id == enrollment_id,
            ForumResponse.business_id == business_id,
            ForumResponse.deleted == False,
        )
        .all()
    )


def get_all_by_lesson_block(db: Session, lesson_block_id: int, business_id: int):
    return (
        db.query(ForumResponse)
        .filter(
            ForumResponse.lesson_block_id == lesson_block_id,
            ForumResponse.business_id == business_id,
            ForumResponse.deleted == False,
        )
        .all()
    )


def get_all_replies(db: Session, forum_response_id: int, business_id: int):
    return (
        db.query(ForumResponse)
        .filter(
            ForumResponse.forum_response_id == forum_response_id,
            ForumResponse.business_id == business_id,
            ForumResponse.deleted == False,
        )
        .all()
    )


# Viejos
"""
def create(db: Session, data: ForumResponseCreate):
    forum_response = ForumResponse(**data.model_dump())

    db.add(forum_response)

    db.commit()
    db.refresh(forum_response)

    return forum_response


def get_by_id(db: Session, forum_response_id: int):
    return (
        db.query(ForumResponse)
        .filter(ForumResponse.id == forum_response_id, ForumResponse.deleted == False)
        .first()
    )


def get_all(db: Session):
    return db.query(ForumResponse).filter(ForumResponse.deleted == False).all()


def get_all_by_enrollment(db: Session, enrollment_id: int):
    return (
        db.query(ForumResponse)
        .filter(
            ForumResponse.enrollment_id == enrollment_id, ForumResponse.deleted == False
        )
        .all()
    )


def get_all_by_lesson_block(db: Session, lesson_block_id: int):
    return (
        db.query(ForumResponse)
        .filter(
            ForumResponse.lesson_block_id == lesson_block_id,
            ForumResponse.deleted == False,
        )
        .all()
    )


def get_all_replies(db: Session, forum_response_id: int):
    return (
        db.query(ForumResponse)
        .filter(
            ForumResponse.forum_response_id == forum_response_id,
            ForumResponse.deleted == False,
        )
        .all()
    )


def update(db: Session, forum_response: ForumResponse, data: ForumResponseUpdate):
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(forum_response, key, value)

    db.commit()
    db.refresh(forum_response)

    return forum_response


def delete(db: Session, forum_response: ForumResponse):
    forum_response.deleted = True

    db.commit()
    db.refresh(forum_response)

    return forum_response


def soft_delete_by_enrollment(db: Session, enrollment_id: int):
    db.query(ForumResponse).filter(ForumResponse.enrollment_id == enrollment_id).update(
        {"deleted": True}
    )
"""
