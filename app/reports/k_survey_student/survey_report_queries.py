import logging

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.lesson_block import LessonBlock
from app.models.survey_response import SurveyResponse
from app.models.user import User

logger = logging.getLogger(__name__)


def get_survey_blocks_by_course(db: Session, course_id: int):
    logger.info(
        "[SURVEY_REPORT] Buscando bloques de encuesta para course_id=%s",
        course_id,
    )

    responses_subquery = (
        db.query(SurveyResponse.lesson_block_id)
        .filter(SurveyResponse.deleted.is_(False))
        .subquery()
    )

    blocks = (
        db.query(LessonBlock)
        .filter(
            LessonBlock.course_id == course_id,
            LessonBlock.deleted.is_(False),
            or_(
                LessonBlock.block_type_id == 7,
                LessonBlock.id.in_(responses_subquery),
            ),
        )
        .order_by(LessonBlock.order.asc())
        .all()
    )

    logger.info(
        "[SURVEY_REPORT] Se encontraron %s bloques",
        len(blocks),
    )

    for block in blocks:
        logger.info(
            "[SURVEY_REPORT] block_id=%s type_id=%s course_id=%s",
            block.id,
            block.block_type_id,
            block.course_id,
        )

    return blocks


def get_enrollments_with_optional_survey_responses(
    db: Session,
    course_id: int,
    block_id: int,
    role_id: int,
):
    logger.info(
        "[SURVEY_REPORT] Consultando estudiantes "
        "course_id=%s block_id=%s role_id=%s",
        course_id,
        block_id,
        role_id,
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
        .order_by(User.lastname.asc(), User.firstname.asc())
        .all()
    )

    logger.info(
        "[SURVEY_REPORT] Registros encontrados para bloque %s: %s",
        block_id,
        len(rows),
    )

    for idx, row in enumerate(rows):
        logger.info(
            "[SURVEY_REPORT] row=%s user='%s' survey=%s response=%s",
            idx + 1,
            row.user_name,
            row.survey_definition is not None,
            row.survey_answers is not None,
        )

    return rows
