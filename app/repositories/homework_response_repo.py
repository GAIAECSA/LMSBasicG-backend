from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.homework_response import HomeworkResponse
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.module import Module
from app.models.subcategory import Subcategory

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, homework_response: HomeworkResponse) -> HomeworkResponse:
    db.add(homework_response)
    db.flush()
    return homework_response


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(
    db: Session,
    homework_response_id: int,
    business_id: int,
) -> None:
    (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.id == homework_response_id,
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_enrollment(
    db: Session,
    enrollment_id: int,
    business_id: int,
) -> None:
    (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.enrollment_id == enrollment_id,
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson_block(
    db: Session,
    lesson_block_id: int,
    business_id: int,
) -> None:
    (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.lesson_block_id == lesson_block_id,
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson(
    db: Session,
    lesson_id: int,
    business_id: int,
) -> None:
    (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted.is_(False),
            HomeworkResponse.lesson_block_id.in_(
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
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted.is_(False),
            HomeworkResponse.lesson_block_id.in_(
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
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted.is_(False),
            HomeworkResponse.lesson_block_id.in_(
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
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted.is_(False),
            HomeworkResponse.lesson_block_id.in_(
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
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted.is_(False),
            HomeworkResponse.lesson_block_id.in_(
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


def get_by_id(db: Session, homework_response_id: int, business_id: int):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.id == homework_response_id,
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted == False,
        )
        .first()
    )


def get_all_by_enrollment(db: Session, enrollment_id: int, business_id: int):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.deleted == False,
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.enrollment_id == enrollment_id,
        )
        .all()
    )


def get_all_by_lesson_block(db: Session, lesson_block_id: int, business_id: int):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.deleted == False,
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.lesson_block_id == lesson_block_id,
        )
        .all()
    )


def get_by_enrollment_and_lesson_block(
    db: Session, enrollment_id: int, lesson_block_id: int, business_id: int
):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.deleted == False,
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.enrollment_id == enrollment_id,
            HomeworkResponse.lesson_block_id == lesson_block_id,
        )
        .first()
    )


def get_by_course_id_default(
    db: Session,
    course_id: int,
    business_id: int,
):
    return (
        db.query(HomeworkResponse)
        .join(
            Enrollment,
            HomeworkResponse.enrollment_id == Enrollment.id,
        )
        .join(
            LessonBlock,
            HomeworkResponse.lesson_block_id == LessonBlock.id,
        )
        .filter(
            Enrollment.course_id == course_id,
            HomeworkResponse.business_id == business_id,
            HomeworkResponse.deleted.is_(False),
            LessonBlock.business_id == business_id,
            LessonBlock.deleted.is_(False),
            LessonBlock.counts_toward_grade.is_(True),
        )
        .all()
    )


# def delete(db: Session, homework_response: HomeworkResponse):
#   homework_response.deleted = True
#  db.merge(homework_response)
# db.commit()
# return homework_response


# def soft_delete_by_enrollment(db: Session, enrollment_id: int):
#   db.query(HomeworkResponse).filter(
#      HomeworkResponse.enrollment_id == enrollment_id
# ).update({"deleted": True})

"""
def get_by_id(db: Session, homework_response_id: int):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.id == homework_response_id,
            HomeworkResponse.deleted == False,
        )
        .first()
    )


def get_all_by_enrollment(db: Session, enrollment_id: int):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.deleted == False,
            HomeworkResponse.enrollment_id == enrollment_id,
        )
        .all()
    )


def get_all_by_lesson_block(db: Session, lesson_block_id: int):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.deleted == False,
            HomeworkResponse.lesson_block_id == lesson_block_id,
        )
        .all()
    )


def get_by_enrollment_and_lesson_block(
    db: Session, enrollment_id: int, lesson_block_id: int
):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.deleted == False,
            HomeworkResponse.enrollment_id == enrollment_id,
            HomeworkResponse.lesson_block_id == lesson_block_id,
        )
        .first()
    )


def get_by_course_id_default(
    db: Session,
    course_id: int,
):

    return (
        db.query(HomeworkResponse)
        .join(
            Enrollment,
            HomeworkResponse.enrollment_id == Enrollment.id,
        )
        .join(
            LessonBlock,
            HomeworkResponse.lesson_block_id == LessonBlock.id,
        )
        .filter(
            Enrollment.course_id == course_id,
            HomeworkResponse.deleted.is_(False),
            LessonBlock.counts_toward_grade.is_(True),
        )
        .all()
    )
"""

#


# def create(
#   db: Session,
#  homework_response: HomeworkResponse,
# ):
#   db.add(homework_response)
#  db.flush()
# db.refresh(homework_response)

# return homework_response


# def update(
#   db: Session,
#  homework_response: HomeworkResponse,
# ):
#   homework_response = db.merge(homework_response)

#  db.flush()
# db.refresh(homework_response)

# return homework_response
