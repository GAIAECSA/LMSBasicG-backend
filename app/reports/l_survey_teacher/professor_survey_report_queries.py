import logging

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.lesson_block_type import LessonBlockType
from app.models.module import Module
from app.models.survey_response import SurveyResponse
from app.models.user import User

logger = logging.getLogger(__name__)


def get_survey_blocks_by_course(db: Session, course_id: int):
    logger.info(
        "[PROFESSOR_SURVEY_REPORT] Buscando encuestas para curso=%s",
        course_id,
    )

    blocks = (
        db.query(LessonBlock)
        .join(Lesson, Lesson.id == LessonBlock.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .join(LessonBlockType, LessonBlockType.id == LessonBlock.block_type_id)
        .filter(
            Module.course_id == course_id,
            Lesson.deleted.is_(False),
            Module.deleted.is_(False),
            LessonBlock.deleted.is_(False),
            LessonBlockType.key == "survey",
        )
        .order_by(
            Module.order.asc(),
            Lesson.order.asc(),
            LessonBlock.order.asc(),
        )
        .all()
    )

    logger.info(
        "[PROFESSOR_SURVEY_REPORT] Encuestas encontradas=%s",
        len(blocks),
    )
    return blocks


def get_enrollments_with_optional_survey_responses(
    db: Session,
    course_id: int,
    block_id: int,
    role_id: int,
):
    logger.info(
        "[PROFESSOR_SURVEY_REPORT] Consultando docentes curso=%s bloque=%s",
        course_id,
        block_id,
    )

    rows = (
        db.query(
            User.id.label("user_id"),
            func.concat(User.lastname, " ", User.firstname).label("user_name"),
            SurveyResponse.survey.label("survey_definition"),
            SurveyResponse.response.label("survey_answers"),
        )
        .select_from(Enrollment)
        .join(
            User,
            and_(
                Enrollment.user_id == User.id,
                User.deleted.is_(False),
            ),
        )
        .outerjoin(
            SurveyResponse,
            and_(
                SurveyResponse.enrollment_id == Enrollment.id,
                SurveyResponse.lesson_block_id == block_id,
                SurveyResponse.deleted.is_(False),
            ),
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.role_id == role_id,
            Enrollment.deleted.is_(False),
        )
        .order_by(
            User.lastname.asc(),
            User.firstname.asc(),
        )
        .all()
    )

    logger.info(
        "[PROFESSOR_SURVEY_REPORT] Docentes encontrados=%s",
        len(rows),
    )
    return rows
