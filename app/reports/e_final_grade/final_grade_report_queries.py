from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.homework_response import HomeworkResponse
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.module import Module
from app.models.quizz_response import QuizzResponse
from app.models.user import User

STUDENT_ROLE_ID = 4


def get_evaluable_blocks(db: Session, course_id: int):
    """
    Obtiene todos los bloques evaluables del curso respetando la jerarquía:
    Course -> Module -> Lesson -> LessonBlock
    """
    return (
        db.query(LessonBlock)
        .join(
            Lesson,
            and_(
                Lesson.id == LessonBlock.lesson_id,
                Lesson.deleted.is_(False),
            ),
        )
        .join(
            Module,
            and_(
                Module.id == Lesson.module_id,
                Module.course_id == course_id,
                Module.deleted.is_(False),
            ),
        )
        .filter(
            LessonBlock.counts_toward_grade.is_(True),
            LessonBlock.is_active.is_(True),
            LessonBlock.deleted.is_(False),
            LessonBlock.default.is_(False),
        )
        .order_by(
            Module.order.asc(),
            Lesson.order.asc(),
            LessonBlock.order.asc(),
        )
        .all()
    )


def get_students_grades_matrix(db: Session, course_id: int):
    """
    Obtiene la matriz completa:
    estudiante × bloque evaluable

    La nota puede provenir de HomeworkResponse o QuizzResponse.
    """
    return (
        db.query(
            User.id.label("student_id"),
            func.concat(
                User.firstname,
                " ",
                User.lastname,
            ).label("student_name"),
            LessonBlock.id.label("block_id"),
            func.coalesce(
                HomeworkResponse.score,
                QuizzResponse.score,
            ).label("score"),
        )
        .select_from(Enrollment)
        .join(
            User,
            and_(
                User.id == Enrollment.user_id,
                User.deleted.is_(False),
            ),
        )
        .join(
            Module,
            and_(
                Module.course_id == Enrollment.course_id,
                Module.deleted.is_(False),
            ),
        )
        .join(
            Lesson,
            and_(
                Lesson.module_id == Module.id,
                Lesson.deleted.is_(False),
            ),
        )
        .join(
            LessonBlock,
            and_(
                LessonBlock.lesson_id == Lesson.id,
                LessonBlock.counts_toward_grade.is_(True),
                LessonBlock.is_active.is_(True),
                LessonBlock.deleted.is_(False),
                LessonBlock.default.is_(False),
            ),
        )
        .outerjoin(
            HomeworkResponse,
            and_(
                HomeworkResponse.enrollment_id == Enrollment.id,
                HomeworkResponse.lesson_block_id == LessonBlock.id,
                HomeworkResponse.deleted.is_(False),
            ),
        )
        .outerjoin(
            QuizzResponse,
            and_(
                QuizzResponse.enrollment_id == Enrollment.id,
                QuizzResponse.lesson_block_id == LessonBlock.id,
                QuizzResponse.deleted.is_(False),
            ),
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.role_id == STUDENT_ROLE_ID,
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
