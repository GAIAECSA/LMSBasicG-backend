from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.lesson_block import LessonBlock
from app.models.survey_response import SurveyResponse
from app.models.user import User

PROFESSOR_ROLE_ID = 3


def get_professor_survey_blocks_by_course(db: Session, course_id: int):
    """
    Obtiene todos los bloques de tipo encuesta del curso de manera híbrida.
    """
    responses_subquery = (
        db.query(SurveyResponse.lesson_block_id)
        .filter(SurveyResponse.deleted.is_(False))
        .subquery()
    )

    return (
        db.query(LessonBlock)
        .filter(
            LessonBlock.course_id == course_id,
            LessonBlock.deleted.is_(False),
            or_(LessonBlock.block_type_id == 7, LessonBlock.id.in_(responses_subquery)),
        )
        .order_by(LessonBlock.order.asc())
        .all()
    )


def get_professor_enrollments_with_optional_responses(
    db: Session, course_id: int, block_id: int
):
    """
    Garantiza traer a TODOS los profesores matriculados en el curso haciendo LEFT JOIN.
    """
    return (
        db.query(
            User.id.label("user_id"),
            func.concat(User.lastname, " ", User.firstname).label("user_name"),
            SurveyResponse.survey.label("survey_definition"),
            SurveyResponse.response.label("survey_answers"),
        )
        .select_from(Enrollment)
        .join(User, and_(Enrollment.user_id == User.id, User.deleted.is_(False)))
        .left_join(
            SurveyResponse,
            and_(
                SurveyResponse.enrollment_id == Enrollment.id,
                SurveyResponse.lesson_block_id == block_id,
                SurveyResponse.deleted.is_(False),
            ),
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.role_id == PROFESSOR_ROLE_ID,
            Enrollment.deleted.is_(False),
        )
        .order_by(User.lastname.asc(), User.firstname.asc())
        .all()
    )
