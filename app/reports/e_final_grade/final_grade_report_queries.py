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


def get_course_students(db: Session, course_id: int):
    """
    Obtiene todos los estudiantes matriculados en el curso.
    """
    return (
        db.query(
            Enrollment.id.label("enrollment_id"),
            User.id.label("student_id"),
            func.concat(User.firstname, " ", User.lastname).label("student_name"),
        )
        .join(User, User.id == Enrollment.user_id)
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.role_id == STUDENT_ROLE_ID,
            Enrollment.deleted.is_(False),
            User.deleted.is_(False),
        )
        .order_by(
            User.lastname.asc(),
            User.firstname.asc(),
        )
        .all()
    )


def get_homework_scores(db: Session, course_id: int):
    """
    Obtiene todas las calificaciones de tareas para un curso específico.
    """
    return (
        db.query(
            HomeworkResponse.enrollment_id,
            HomeworkResponse.lesson_block_id,
            HomeworkResponse.score,
        )
        .join(Enrollment, Enrollment.id == HomeworkResponse.enrollment_id)
        .filter(
            Enrollment.course_id == course_id,
            HomeworkResponse.deleted.is_(False),
        )
        .all()
    )


def get_quizz_scores(db: Session, course_id: int):
    """
    Obtiene todas las calificaciones de cuestionarios para un curso específico.
    """
    return (
        db.query(
            QuizzResponse.enrollment_id,
            QuizzResponse.lesson_block_id,
            QuizzResponse.score,
        )
        .join(Enrollment, Enrollment.id == QuizzResponse.enrollment_id)
        .filter(
            Enrollment.course_id == course_id,
            QuizzResponse.deleted.is_(False),
        )
        .all()
    )
