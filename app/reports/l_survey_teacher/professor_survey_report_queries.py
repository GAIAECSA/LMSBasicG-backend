from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.lesson_block import LessonBlock
from app.models.survey_response import SurveyResponse
from app.models.user import User

PROFESSOR_ROLE_ID = 3


def get_professor_survey_blocks_by_course(db: Session, course_id: int):
    """
    Obtiene TODOS los bloques de tipo encuesta creados en el curso
    (block_type_id = 7), sin importar si tienen respuestas o no.
    """
    return (
        db.query(LessonBlock)
        .filter(
            LessonBlock.course_id == course_id,
            LessonBlock.block_type_id == 7,
            LessonBlock.deleted == False,
        )
        .order_by(LessonBlock.order.asc())
        .all()
    )


def get_professor_enrollments_with_optional_responses(
    db: Session, course_id: int, block_id: int
):
    """
    Garantiza traer a TODOS los profesores matriculados en el curso.
    Hace un LEFT JOIN hacia SurveyResponse para el bloque en cuestión,
    permitiendo traer al usuario aunque la respuesta sea nula.
    """
    return (
        db.query(
            User.id.label("user_id"),
            func.concat(User.lastname, " ", User.firstname).label("user_name"),
            SurveyResponse.survey.label("survey_definition"),
            SurveyResponse.response.label("survey_answers"),
        )
        .select_from(Enrollment)
        .join(User, and_(Enrollment.user_id == User.id, User.deleted == False))
        .left_join(
            SurveyResponse,
            and_(
                SurveyResponse.enrollment_id == Enrollment.id,
                SurveyResponse.lesson_block_id == block_id,
                SurveyResponse.deleted == False,
            ),
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.role_id == PROFESSOR_ROLE_ID,
            Enrollment.deleted == False,
        )
        .order_by(User.lastname.asc(), User.firstname.asc())
        .all()
    )
