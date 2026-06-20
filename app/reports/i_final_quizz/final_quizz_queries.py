from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.module import Module
from app.models.quizz_response import QuizzResponse
from app.models.user import User

STUDENT_ROLE_ID = 4


def get_final_quizzes_headers(db: Session, course_id: int, business_id: int):
    """
    Recupera los bloques de cuestionarios del curso que SÍ entran en la nota final,
    filtrados por business_id.
    """
    return (
        db.query(LessonBlock)
        .join(
            Lesson,
            and_(Lesson.id == LessonBlock.lesson_id, Lesson.business_id == business_id),
        )
        .join(
            Module, and_(Module.id == Lesson.module_id, Module.course_id == course_id)
        )
        .filter(
            LessonBlock.business_id == business_id,
            Module.business_id == business_id,
            LessonBlock.block_type_id == 2,  # Tipo de bloque: Quizz
            LessonBlock.counts_toward_grade.is_(True),  # SÍ cuenta para la nota final
            LessonBlock.is_active.is_(True),
            LessonBlock.deleted.is_(False),
            Lesson.deleted.is_(False),
            Module.deleted.is_(False),
        )
        .order_by(Module.order.asc(), Lesson.order.asc(), LessonBlock.order.asc())
        .all()
    )


def get_students_final_quizzes_matrix(db: Session, course_id: int, business_id: int):
    """
    Obtiene la lista de estudiantes matriculados junto con el score y estado de aprobación
    de los quizzes finales, filtrando por business_id.
    """
    # 1. Subconsulta para aislar el mejor intento
    best_quizz_responses = (
        db.query(QuizzResponse)
        .distinct(QuizzResponse.enrollment_id, QuizzResponse.lesson_block_id)
        .filter(
            QuizzResponse.business_id == business_id, QuizzResponse.deleted.is_(False)
        )
        .order_by(
            QuizzResponse.enrollment_id,
            QuizzResponse.lesson_block_id,
            QuizzResponse.score.desc(),
            QuizzResponse.id.desc(),
        )
        .subquery()
    )

    # 2. Consulta principal
    return (
        db.query(
            User.id.label("student_id"),
            func.concat(User.firstname, " ", User.lastname).label("student_name"),
            LessonBlock.id.label("block_id"),
            best_quizz_responses.c.score.label("score"),
            best_quizz_responses.c.is_passed.label("is_passed"),
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
                LessonBlock.block_type_id == 2,
                LessonBlock.counts_toward_grade.is_(True),
                LessonBlock.is_active.is_(True),
                LessonBlock.deleted.is_(False),
            ),
        )
        .outerjoin(
            best_quizz_responses,
            and_(
                best_quizz_responses.c.enrollment_id == Enrollment.id,
                best_quizz_responses.c.lesson_block_id == LessonBlock.id,
            ),
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.business_id == business_id,
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
