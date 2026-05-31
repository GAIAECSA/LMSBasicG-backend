from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.homework_response import HomeworkResponse
from app.models.lesson_block import LessonBlock
from app.models.quizz_response import QuizzResponse
from app.models.user import User

STUDENT_ROLE_ID = 4


def get_evaluable_blocks(db: Session, course_id: int):
    """
    Obtiene todos los bloques de lección evaluables del curso en orden.
    """
    return (
        db.query(LessonBlock)
        .filter(
            LessonBlock.course_id == course_id,
            LessonBlock.counts_toward_grade.is_(True),
            LessonBlock.is_active.is_(True),
            LessonBlock.deleted.is_(False),
        )
        .order_by(LessonBlock.order.asc())
        .all()
    )


def get_students_grades_matrix(db: Session, course_id: int):
    """
    Obtiene la combinación de estudiantes con sus respectivas notas unificadas
    de tareas o cuestionarios. Si no existe entrega, devuelve None.
    """
    return (
        db.query(
            User.id.label("student_id"),
            func.concat(User.firstname, " ", User.lastname).label("student_name"),
            LessonBlock.id.label("block_id"),
            func.coalesce(HomeworkResponse.score, QuizzResponse.score).label("score"),
        )
        .select_from(Enrollment)
        .join(User, and_(User.id == Enrollment.user_id, User.deleted.is_(False)))
        .join(
            LessonBlock,
            and_(
                LessonBlock.course_id == Enrollment.course_id,
                LessonBlock.counts_toward_grade.is_(True),
                LessonBlock.is_active.is_(True),
                LessonBlock.deleted.is_(False),
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
            LessonBlock.order.asc(),
        )
        .all()
    )
