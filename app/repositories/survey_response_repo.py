from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.module import Module
from app.models.subcategory import Subcategory
from app.models.survey_response import SurveyResponse

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================

# --- Crear ---


def create(db: Session, survey_response: SurveyResponse) -> SurveyResponse:
    db.add(survey_response)
    db.flush()
    return survey_response


# --- Eliminaciones (Updates/Deletes masivos) ---


def delete_soft_by_id(
    db: Session,
    survey_response_id: int,
    business_id: int,
) -> None:
    (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.id == survey_response_id,
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_enrollment(
    db: Session,
    enrollment_id: int,
    business_id: int,
) -> None:
    (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.enrollment_id == enrollment_id,
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_user(
    db: Session,
    user_id: int,
    business_id: int,
) -> None:
    (
        db.query(SurveyResponse)
        .join(
            Enrollment,
            SurveyResponse.enrollment_id == Enrollment.id,
        )
        .filter(
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted.is_(False),
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
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.lesson_block_id == lesson_block_id,
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted.is_(False),
        )
        .update({"deleted": True}, synchronize_session=False)
    )


def delete_soft_by_lesson(
    db: Session,
    lesson_id: int,
    business_id: int,
) -> None:
    (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted.is_(False),
            SurveyResponse.lesson_block_id.in_(
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
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted.is_(False),
            SurveyResponse.lesson_block_id.in_(
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
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted.is_(False),
            SurveyResponse.lesson_block_id.in_(
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
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted.is_(False),
            SurveyResponse.lesson_block_id.in_(
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
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted.is_(False),
            SurveyResponse.lesson_block_id.in_(
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


def get_by_id(db: Session, survey_response_id: int, business_id: int):
    return (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.id == survey_response_id,
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted == False,
        )
        .first()
    )


def get_all(db: Session, business_id: int):
    return (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.business_id == business_id, SurveyResponse.deleted == False
        )
        .all()
    )


def get_all_by_enrollment(db: Session, enrollment_id: int, business_id: int):
    return (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.enrollment_id == enrollment_id,
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted == False,
        )
        .all()
    )


def get_all_by_lesson_block(db: Session, lesson_block_id: int, business_id: int):
    return (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.lesson_block_id == lesson_block_id,
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted == False,
        )
        .all()
    )


def get_by_enrollment_lesson_block(
    db: Session, enrollment_id: int, lesson_block_id: int, business_id: int
):
    return (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.lesson_block_id == lesson_block_id,
            SurveyResponse.enrollment_id == enrollment_id,
            SurveyResponse.business_id == business_id,
            SurveyResponse.deleted == False,
        )
        .all()
    )


# def create(db: Session, data: SurveyResponseCreate):
#   survey_response = SurveyResponse(**data.model_dump())

#  db.add(survey_response)

# db.commit()
# db.refresh(survey_response)

# return survey_response

"""
def get_by_id(db: Session, survey_response_id: int):
    return (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.id == survey_response_id, SurveyResponse.deleted == False
        )
        .first()
    )


def get_all(db: Session):
    return db.query(SurveyResponse).filter(SurveyResponse.deleted == False).all()


def get_all_by_enrollment(db: Session, enrollment_id: int):
    return (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.enrollment_id == enrollment_id,
            SurveyResponse.deleted == False,
        )
        .all()
    )


def get_all_by_lesson_block(db: Session, lesson_block_id: int):
    return (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.lesson_block_id == lesson_block_id,
            SurveyResponse.deleted == False,
        )
        .all()
    )
"""

# def update(db: Session, survey_response: SurveyResponse, data: SurveyResponseUpdate):
#   update_data = data.model_dump(exclude_unset=True)
#
#   for key, value in update_data.items():
#      setattr(survey_response, key, value)

# db.commit()
# db.refresh(survey_response)

# return survey_response


# def delete(db: Session, survey_response: SurveyResponse):
#   survey_response.deleted = True

#  db.commit()
# db.refresh(survey_response)

# return survey_response


# def soft_delete_by_enrollment(db: Session, enrollment_id: int):
#   db.query(SurveyResponse).filter(
#      SurveyResponse.enrollment_id == enrollment_id
# ).update({"deleted": True})
