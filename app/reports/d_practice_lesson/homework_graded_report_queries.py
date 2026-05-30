from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.homework_response import HomeworkResponse
from app.models.lesson_block import LessonBlock
from app.models.user import User


def get_all_graded_homeworks_matrix(db: Session, course_id: int):
    """
    Obtiene la combinación de cada estudiante matriculado con cada bloque
    de tarea del curso que tenga 'counts_toward_grade' en True.
    """
    return (
        db.query(
            User.id.label("student_id"),
            func.concat(User.firstname, " ", User.lastname).label("student_name"),
            LessonBlock.id.label("block_id"),
            LessonBlock.content.label("block_content"),
            HomeworkResponse.id.label("response_id"),
            HomeworkResponse.score.label("score"),
            HomeworkResponse.created_at.label("submitted_at"),
            HomeworkResponse.status.label("submission_status"),
        )
        .select_from(
            Enrollment
        )  # <-- Establece explícitamente el origen izquierdo de la consulta
        .join(
            User,
            and_(
                User.id == Enrollment.user_id,
                User.deleted.is_(False),
            ),
        )
        .join(
            LessonBlock,
            and_(
                LessonBlock.course_id
                == Enrollment.course_id,  # Multiplica cada alumno por cada bloque del curso
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
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.role_id == 4,  # Rol Estudiante
            Enrollment.deleted.is_(False),
        )
        .order_by(
            User.lastname.asc(),
            User.firstname.asc(),
            LessonBlock.order.asc(),
        )
        .all()
    )
