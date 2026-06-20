from sqlalchemy.orm import Session

from app.helpers import recalculate_enrollment_certificate
from app.models.quizz_response import QuizzResponse
from app.repositories import course_repo, quizz_response_repo
from app.schemas.quizz_response import QuizzResponseCreate, QuizzResponseUpdate

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class QuizzAlreadyExits(Exception):
    pass


class QuizzNotFound(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class QuizzScoreDecreaseNotAllowed(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================
def create_quizz_response(db: Session, data: QuizzResponseCreate, business_id: int):

    with db.begin():

        existing = quizz_response_repo.get_by_enrollment_and_lesson_block(
            db, data.enrollment_id, data.lesson_block_id, business_id
        )

        if existing:
            raise QuizzAlreadyExits("Registro existente")

        quizz_response = QuizzResponse(**data.model_dump(), business_id=business_id)

        response = quizz_response_repo.create(
            db,
            quizz_response,
        )

        if response.score is not None:
            course_id = quizz_response.lesson_block.lesson.module.course_id
            course = course_repo.get_by_id(db, course_id, business_id)
            if not course:
                raise CourseNotFoundError("Curso no encontrado")
            if not course.is_mdt:
                recalculate_enrollment_certificate.recalculate_enrollment_certificate_MOOC(
                    db=db, enrollment=response.enrollment, business_id=business_id
                )

    return response


def update_quizz_response(
    db: Session,
    quizz_response_id: int,
    data: QuizzResponseUpdate,
    business_id: int,
):
    with db.begin():

        quizz_response = quizz_response_repo.get_by_id(
            db,
            quizz_response_id,
            business_id,
        )

        if not quizz_response:
            raise QuizzNotFound("Prueba no encontrada")

        data_dict = data.model_dump(exclude_unset=True)

        new_score = data_dict.get("score")

        if (
            new_score is not None
            and quizz_response.score is not None
            and new_score <= quizz_response.score
        ):
            raise QuizzScoreDecreaseNotAllowed(
                "La nueva calificación debe ser mayor a la actual"
            )

        for key, value in data_dict.items():
            setattr(quizz_response, key, value)

        course_id = quizz_response.lesson_block.lesson.module.course_id

        course = course_repo.get_by_id(
            db,
            course_id,
            business_id,
        )

        if not course:
            raise CourseNotFoundError("Curso no encontrado")

        if not course.is_mdt:
            recalculate_enrollment_certificate.recalculate_enrollment_certificate_MOOC(
                db=db,
                enrollment=quizz_response.enrollment,
                business_id=business_id,
            )

        return quizz_response


def delete_quizz_response(db: Session, quizz_response_id: int, business_id: int):
    quizz_response = quizz_response_repo.get_by_id(db, quizz_response_id, business_id)
    if not quizz_response:
        raise QuizzNotFound("Respuestas no encontradas")

    course_id = quizz_response.lesson_block.lesson.module.course_id
    course = course_repo.get_by_id(db, course_id, business_id)
    if not course:
        raise CourseNotFoundError("Curso no encontrado")

    if not course.is_mdt:
        recalculate_enrollment_certificate.recalculate_enrollment_certificate_MOOC(
            db=db, enrollment=quizz_response.enrollment, business_id=business_id
        )
    return quizz_response_repo.delete_soft_by_id(db, quizz_response_id, business_id)


def get_quizz_response(db: Session, quizz_response_id: int, business_id: int):
    quizz_response = quizz_response_repo.get_by_id(db, quizz_response_id, business_id)
    if not quizz_response:
        raise QuizzNotFound("Respuestas no encontradas")
    return quizz_response


def get_by_enrollment(db: Session, enrollment_id: int, business_id: int):
    quizzes = quizz_response_repo.get_all_by_enrollment_count_towards_grade(
        db, enrollment_id, business_id
    )
    return quizzes


def get_by_block(db: Session, lesson_block_id: int, business_id: int):
    return quizz_response_repo.get_all_by_lesson_block(db, lesson_block_id, business_id)


def get_one_by_enrollment(db: Session, enrollment_id: int, business_id: int):
    quizz_response = quizz_response_repo.get_by_enrollment(
        db, enrollment_id, business_id
    )

    if not quizz_response:
        raise QuizzNotFound("Respuestas no encontradas")

    return quizz_response


"""
def create_quizz_response(
    db: Session,
    data: QuizzResponseCreate,
):

    with db.begin():

        existing = quizz_response_repo.get_by_enrollment_and_lesson_block(
            db,
            data.enrollment_id,
            data.lesson_block_id,
        )

        if existing:
            raise Exception("Registro existente")

        quizz_response = QuizzResponse(**data.model_dump())

        response = quizz_response_repo.create_flush(
            db,
            quizz_response,
        )

        if response.score is not None or response.is_passed is not None:

            recalculate_enrollment_certificate(
                db=db,
                enrollment=response.enrollment,
            )

    return response


def update_quizz_response(
    db: Session,
    quizz_response_id: int,
    data: QuizzResponseUpdate,
):

    with db.begin():

        quizz_response = quizz_response_repo.get_by_id(
            db,
            quizz_response_id,
        )

        if not quizz_response:
            raise Exception("Respuestas no encontradas")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(quizz_response, key, value)

        response = quizz_response_repo.update(
            db,
            quizz_response,
        )

        course = COU_get_by_id(
            db,
            response.enrollment.course_id,
        )

        should_recalculate = (
            course
            and not course.is_mdt
            and (data.score is not None or data.is_passed is not None)
        )

        if should_recalculate:

            recalculate_enrollment_certificate(
                db=db,
                enrollment=response.enrollment,
            )

    return response


def delete_quizz_response(db: Session, quizz_response_id: int):
    quizz_response = quizz_response_repo.get_by_id(db, quizz_response_id)
    if not quizz_response:
        raise Exception("Respuestas no encontradas")

    return quizz_response_repo.delete(db, quizz_response)


def get_quizz_response(db: Session, quizz_response_id: int):
    quizz_response = quizz_response_repo.get_by_id(db, quizz_response_id)
    if not quizz_response:
        raise Exception("Respuestas no encontradas")
    return quizz_response


def get_by_enrollment(db: Session, enrollment_id: int):
    quizzes = quizz_response_repo.get_all_by_enrollment(db, enrollment_id)
    return [
        quizz
        for quizz in quizzes
        if (lesson_block := LES_BLO_get_by_id(db, quizz.lesson_block_id))
        and lesson_block.counts_toward_grade
    ]


def get_by_block(db: Session, lesson_block_id: int):
    return quizz_response_repo.get_all_by_lesson_block(db, lesson_block_id)


def get_one_by_enrollment(db: Session, enrollment_id: int):
    quizz_response = quizz_response_repo.get_by_enrollment(db, enrollment_id)

    if not quizz_response:
        raise Exception("Respuestas no encontradas")

    return quizz_response
"""
