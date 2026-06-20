from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.module import Module
from app.models.quizz_response import QuizzResponse
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, quizz_reponse: QuizzResponse):
    db.add(quizz_reponse)
    db.flush()
    return quizz_reponse


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(
    db: Session,
    quizz_response_id: int,
    business_id: int,
) -> None:
    (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.id == quizz_response_id,
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_enrollment(
    db: Session,
    enrollment_id: int,
    business_id: int,
) -> None:
    (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.enrollment_id == enrollment_id,
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_user(
    db: Session,
    user_id: int,
    business_id: int,
) -> None:
    (
        db.query(QuizzResponse)
        .join(
            Enrollment,
            QuizzResponse.enrollment_id == Enrollment.id,
        )
        .filter(
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted.is_(False),
            Enrollment.user_id == user_id,
            Enrollment.business_id == business_id,
            Enrollment.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson_block(
    db: Session,
    lesson_block_id: int,
    business_id: int,
) -> None:
    (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.lesson_block_id == lesson_block_id,
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson(
    db: Session,
    lesson_id: int,
    business_id: int,
) -> None:
    (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted.is_(False),
            QuizzResponse.lesson_block_id.in_(
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
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted.is_(False),
            QuizzResponse.lesson_block_id.in_(
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
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted.is_(False),
            QuizzResponse.lesson_block_id.in_(
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
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted.is_(False),
            QuizzResponse.lesson_block_id.in_(
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
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted.is_(False),
            QuizzResponse.lesson_block_id.in_(
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


def get_by_id(db: Session, quizz_response_id: int, business_id: int):
    return (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.id == quizz_response_id,
            QuizzResponse.business_id == business_id,
            QuizzResponse.deleted == False,
        )
        .first()
    )


def get_by_enrollment_and_lesson_block(
    db: Session, enrollment_id: int, lesson_block_id: int, business_id: int
):
    return (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.deleted == False,
            QuizzResponse.enrollment_id == enrollment_id,
            QuizzResponse.lesson_block_id == lesson_block_id,
            QuizzResponse.business_id == business_id,
        )
        .first()
    )


def get_all_by_enrollment(db: Session, enrollment_id: int, business_id: int):
    return (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.deleted == False,
            QuizzResponse.enrollment_id == enrollment_id,
            QuizzResponse.business_id == business_id,
        )
        .all()
    )


def get_all_by_enrollment_count_towards_grade(
    db: Session, enrollment_id: int, business_id: int
):
    return (
        db.query(QuizzResponse)
        .join(QuizzResponse.lesson_block)
        .filter(
            # Filtros de QuizzResponse
            QuizzResponse.deleted == False,
            QuizzResponse.enrollment_id == enrollment_id,
            QuizzResponse.business_id == business_id,
            # Filtros de LessonBlock
            LessonBlock.counts_toward_grade == True,
            LessonBlock.deleted == False,
            LessonBlock.business_id == business_id,
        )
        .all()
    )


def get_all_by_lesson_block(db: Session, lesson_block_id: int, business_id: int):
    return (
        db.query(QuizzResponse)
        .options(
            joinedload(QuizzResponse.lesson_block), joinedload(QuizzResponse.enrollment)
        )
        .filter(
            QuizzResponse.lesson_block_id == lesson_block_id,
            QuizzResponse.deleted == False,
            QuizzResponse.business_id == business_id,
        )
        .all()
    )


def get_by_enrollment(db: Session, enrollment_id: int, business_id: int):
    quizz_response = (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.deleted == False,
            QuizzResponse.enrollment_id == enrollment_id,
            QuizzResponse.business_id == business_id,
        )
        .first()
    )
    return quizz_response


# def create(db: Session, quizz_response: QuizzResponse):
#   db.add(quizz_response)
#  db.commit()
# db.refresh(quizz_response)
# return quizz_response


# def create_flush(db: Session, quizz_response: QuizzResponse):
#   db.add(quizz_response)
#  db.flush()
# db.refresh(quizz_response)
# return quizz_response


# def delete(db: Session, quizz_response: QuizzResponse):
#   quizz_response.deleted = True
#  db.merge(quizz_response)
# db.commit()
# return quizz_response


# def soft_delete_by_enrollment(db: Session, enrollment_id: int):
#   db.query(QuizzResponse).filter(QuizzResponse.enrollment_id == enrollment_id).update(
#      {"deleted": True}
# )

"""
def get_by_id(db: Session, quizz_response_id: int):
    return (
        db.query(QuizzResponse)
        .filter(QuizzResponse.id == quizz_response_id, QuizzResponse.deleted == False)
        .first()
    )


def get_by_enrollment_and_lesson_block(
    db: Session, enrollment_id: int, lesson_block_id: int
):
    return (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.deleted == False,
            QuizzResponse.enrollment_id == enrollment_id,
            QuizzResponse.lesson_block_id == lesson_block_id,
        )
        .first()
    )


def get_all_by_enrollment(db: Session, enrollment_id: int):
    return (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.deleted == False, QuizzResponse.enrollment_id == enrollment_id
        )
        .all()
    )


def get_all_by_lesson_block(db: Session, lesson_block_id: int):
    return (
        db.query(QuizzResponse)
        .options(
            joinedload(QuizzResponse.lesson_block), joinedload(QuizzResponse.enrollment)
        )
        .filter(
            QuizzResponse.lesson_block_id == lesson_block_id,
            QuizzResponse.deleted == False,
        )
        .all()
    )


def get_by_enrollment(db: Session, enrollment_id: int):
    quizz_response = (
        db.query(QuizzResponse)
        .filter(
            QuizzResponse.deleted == False, QuizzResponse.enrollment_id == enrollment_id
        )
        .first()
    )
    return quizz_response


# Metodos compuestos

"""
# def update(db: Session, quizz_response: QuizzResponse):
#   db.add(quizz_response)
#  db.flush()
# db.refresh(quizz_response)
# return quizz_response
