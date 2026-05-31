from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.lesson_block import LessonBlock
from app.models.survey_response import SurveyResponse
from app.models.user import User

STUDENT_ROLE_ID = 4


def get_survey_blocks_with_responses(db: Session, course_id: int):
    """
    Obtiene todos los bloques de tipo encuesta del curso que ya cuentan
    con al menos una respuesta registrada.
    """
    return (
        db.query(LessonBlock)
        .join(SurveyResponse, LessonBlock.id == SurveyResponse.lesson_block_id)
        .filter(
            LessonBlock.course_id == course_id,
            LessonBlock.deleted.is_(False),
            SurveyResponse.deleted.is_(False),
        )
        .distinct()
        .order_by(LessonBlock.order.asc())
        .all()
    )


def get_course_survey_responses_matrix(db: Session, course_id: int):
    """
    Recupera los alumnos matriculados y sus respuestas (JSONB) correspondientes
    a las encuestas del curso.
    """
    return (
        db.query(
            User.id.label("student_id"),
            func.concat(User.firstname, " ", User.lastname).label("student_name"),
            LessonBlock.id.label("block_id"),
            SurveyResponse.survey.label("survey_definition"),
            SurveyResponse.response.label("survey_answers"),
        )
        .select_from(Enrollment)
        .join(User, and_(User.id == Enrollment.user_id, User.deleted.is_(False)))
        .join(
            LessonBlock,
            and_(
                LessonBlock.course_id == Enrollment.course_id,
                LessonBlock.deleted.is_(False),
            ),
        )
        .join(
            SurveyResponse,
            and_(
                SurveyResponse.enrollment_id == Enrollment.id,
                SurveyResponse.lesson_block_id == LessonBlock.id,
                SurveyResponse.deleted.is_(False),
            ),
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.role_id == STUDENT_ROLE_ID,
            Enrollment.deleted.is_(False),
        )
        .order_by(User.lastname.asc(), User.firstname.asc())
        .all()
    )
