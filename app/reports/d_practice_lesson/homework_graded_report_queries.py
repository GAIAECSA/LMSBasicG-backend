from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.homework_response import HomeworkResponse
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.module import Module
from app.models.user import User


def get_all_graded_homeworks_matrix(
    db: Session,
    course_id: int,
    business_id: int,
):
    return (
        db.query(
            User.id.label("student_id"),
            func.concat(
                User.firstname,
                " ",
                User.lastname,
            ).label("student_name"),
            LessonBlock.id.label("block_id"),
            LessonBlock.content.label("block_content"),
            LessonBlock.order.label("block_order"),
            HomeworkResponse.id.label("response_id"),
            HomeworkResponse.score.label("score"),
            HomeworkResponse.created_at.label("submitted_at"),
            HomeworkResponse.status.label("submission_status"),
        )
        .select_from(Enrollment)
        .join(
            User,
            and_(
                User.id == Enrollment.user_id,
                User.business_id == business_id,
                User.deleted.is_(False),
            ),
        )
        .join(
            Module,
            and_(
                Module.course_id == Enrollment.course_id,
                Module.business_id == business_id,
                Module.deleted.is_(False),
            ),
        )
        .join(
            Lesson,
            and_(
                Lesson.module_id == Module.id,
                Lesson.business_id == business_id,
                Lesson.deleted.is_(False),
            ),
        )
        .join(
            LessonBlock,
            and_(
                LessonBlock.lesson_id == Lesson.id,
                LessonBlock.business_id == business_id,
                LessonBlock.counts_toward_grade.is_(True),
                LessonBlock.is_active.is_(True),
                LessonBlock.deleted.is_(False),
                LessonBlock.default.is_(False),
                LessonBlock.block_type_id == 6,
            ),
        )
        .outerjoin(
            HomeworkResponse,
            and_(
                HomeworkResponse.enrollment_id == Enrollment.id,
                HomeworkResponse.lesson_block_id == LessonBlock.id,
                HomeworkResponse.business_id == business_id,
                HomeworkResponse.deleted.is_(False),
            ),
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.business_id == business_id,
            Enrollment.role_id == 4,
            Enrollment.deleted.is_(False),
        )
        .order_by(
            User.lastname.asc(),
            User.firstname.asc(),
            Module.order.asc(),
            Lesson.order.asc(),
            LessonBlock.order.asc(),
        )
        .all()
    )
