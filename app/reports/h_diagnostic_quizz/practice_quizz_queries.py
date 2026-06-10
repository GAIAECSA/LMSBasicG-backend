from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.lesson_block import LessonBlock
from app.models.quizz_response import QuizzResponse
from app.models.user import User

STUDENT_ROLE_ID = 4


def get_practice_quizzes_headers(db: Session, course_id: int):
    """
    Recupera los bloques de cuestionarios del curso que NO entran en la nota final.
    """
    return (
        db.query(LessonBlock)
        .filter(
            LessonBlock.course_id == course_id,
            LessonBlock.counts_toward_grade.is_(False),
            LessonBlock.is_active.is_(True),
            LessonBlock.deleted.is_(False),
        )
        .order_by(LessonBlock.order.asc())
        .all()
    )


def get_students_practice_quizzes_matrix(db: Session, course_id: int):
    """
    Obtiene la lista de estudiantes matriculados junto con el score y estado de aprobación
    de los quizzes que no cuentan para la nota final, controlando intentos múltiples.
    """
    # 1. Subconsulta para aislar el mejor intento (o el más reciente) por cada inscripción y bloque
    best_quizz_responses = (
        db.query(QuizzResponse)
        .distinct(QuizzResponse.enrollment_id, QuizzResponse.lesson_block_id)
        .filter(QuizzResponse.deleted.is_(False))
        .order_by(
            QuizzResponse.enrollment_id,
            QuizzResponse.lesson_block_id,
            QuizzResponse.score.desc(),  # PRIORIDAD: Trae el intento con la nota más alta.
            QuizzResponse.id.desc(),  # Desempate: El intento más reciente si las notas son iguales.
        )
        .subquery()
    )

    # 2. Consulta principal unida a la subconsulta limpia
    return (
        db.query(
            User.id.label("student_id"),
            func.concat(User.firstname, " ", User.lastname).label("student_name"),
            LessonBlock.id.label("block_id"),
            best_quizz_responses.c.score.label("score"),
            best_quizz_responses.c.is_passed.label("is_passed"),
        )
        .select_from(Enrollment)
        .join(User, and_(User.id == Enrollment.user_id, User.deleted.is_(False)))
        .join(
            LessonBlock,
            and_(
                LessonBlock.course_id == Enrollment.course_id,
                LessonBlock.counts_toward_grade.is_(False),
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
