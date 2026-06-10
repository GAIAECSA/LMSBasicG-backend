from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.lesson import Lesson  # IMPORTANTE: Agregar esta importación
from app.models.lesson_block import LessonBlock
from app.models.module import Module  # IMPORTANTE: Agregar esta importación
from app.models.quizz_response import QuizzResponse
from app.models.user import User

STUDENT_ROLE_ID = 4


def get_practice_quizzes_headers(db: Session, course_id: int):
    """
    Recupera los bloques de cuestionarios del curso que NO entran en la nota final.
    Navega a través de Module y Lesson para evitar problemas con LessonBlock.course_id nulo.
    """
    return (
        db.query(LessonBlock)
        .join(Lesson, Lesson.id == LessonBlock.lesson_id)
        .join(Module, Module.id == Lesson.module_id)
        .filter(
            Module.course_id == course_id,
            LessonBlock.block_type_id
            == 2,  # Especificamos que el tipo de bloque sea Quizz
            LessonBlock.counts_toward_grade.is_(False),
            LessonBlock.is_active.is_(True),
            LessonBlock.deleted.is_(False),
            Lesson.deleted.is_(
                False
            ),  # Buena práctica: asegurar que el padre no esté borrado
            Module.deleted.is_(False),
        )
        .order_by(Module.order.asc(), Lesson.order.asc(), LessonBlock.order.asc())
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
        # Navegamos Enrollment -> Module -> Lesson para llegar al LessonBlock de forma segura
        .join(
            Module,
            and_(Module.course_id == Enrollment.course_id, Module.deleted.is_(False)),
        )
        .join(Lesson, and_(Lesson.module_id == Module.id, Lesson.deleted.is_(False)))
        .join(
            LessonBlock,
            and_(
                LessonBlock.lesson_id == Lesson.id,
                LessonBlock.block_type_id == 2,  # Filtro estricto de Quizz
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
            Module.order.asc(),
            Lesson.order.asc(),
            LessonBlock.order.asc(),
        )
        .all()
    )
