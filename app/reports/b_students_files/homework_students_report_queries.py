from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.homework_response import HomeworkResponse
from app.models.lesson_block import LessonBlock
from app.models.user import User


def get_homework_block_id_by_title(
    db: Session, course_id: int, title: str
) -> int | None:
    """Busca el ID del bloque de lección por curso y título dentro de su contenido JSONB."""
    row = (
        db.query(LessonBlock.id)
        .filter(
            LessonBlock.course_id == course_id,
            LessonBlock.content["title"].astext == title,
            LessonBlock.deleted.is_(False),
        )
        .first()
    )
    return row[0] if row else None


def get_students_homework_submissions(
    db: Session, course_id: int, lesson_block_id: int | None
):
    """Obtiene la lista de todos los estudiantes y sus estados de entrega para un bloque específico."""
    return (
        db.query(
            User.id.label("student_id"),
            func.concat(User.firstname, " ", User.lastname).label("student_name"),
            HomeworkResponse.id.label("response_id"),
            HomeworkResponse.created_at.label("submitted_at"),
            HomeworkResponse.status.label("submission_status"),
        )
        .join(
            Enrollment,
            and_(
                Enrollment.user_id == User.id,
                Enrollment.course_id == course_id,
                Enrollment.role_id == 4,  # Estudiante
                Enrollment.deleted.is_(False),
            ),
        )
        .outerjoin(
            HomeworkResponse,
            and_(
                HomeworkResponse.enrollment_id == Enrollment.id,
                HomeworkResponse.lesson_block_id == lesson_block_id,
                HomeworkResponse.deleted.is_(False),
            ),
        )
        .filter(User.deleted.is_(False))
        .order_by(
            User.lastname.asc(),
            User.firstname.asc(),
        )
        .all()
    )
