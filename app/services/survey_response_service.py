from sqlalchemy.orm import Session

from app.models.survey_response import SurveyResponse
from app.repositories import survey_response_repo
from app.schemas.survey_response import SurveyResponseCreate

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class SurveyResponseNotFoundError(Exception):
    pass


class SurveyResponseAlreadyExistsError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def create_survey_response(db: Session, data: SurveyResponseCreate, business_id: int):
    with db.begin():
        existing_response = survey_response_repo.get_by_enrollment_lesson_block(
            db, data.enrollment_id, data.lesson_block_id, business_id
        )

        if existing_response:
            raise SurveyResponseAlreadyExistsError(
                "El usuario ya ha enviado una respuesta para esta encuesta"
            )

        survey_response = SurveyResponse(
            **data.model_dump(exclude_unset=True), business_id=business_id
        )
        return survey_response_repo.create(db, survey_response)


def get_survey_response(db: Session, survey_response_id: int, business_id: int):
    survey_response = survey_response_repo.get_by_id(
        db, survey_response_id, business_id
    )

    if not survey_response:
        raise SurveyResponseNotFoundError("Respuesta de encuesta no encontrada")

    return survey_response


def get_all_survey_responses(db: Session, business_id: int):
    return survey_response_repo.get_all(db, business_id)


def get_all_by_enrollment(db: Session, enrollment_id: int, business_id: int):
    return survey_response_repo.get_all_by_enrollment(db, enrollment_id, business_id)


def get_all_by_lesson_block(db: Session, lesson_block_id: int, business_id: int):
    return survey_response_repo.get_all_by_lesson_block(
        db, lesson_block_id, business_id
    )


"""
def create_survey_response(db: Session, data: SurveyResponseCreate):
    return survey_response_repo.create(db, data)


def get_survey_response(db: Session, survey_response_id: int):
    survey_response = survey_response_repo.get_by_id(db, survey_response_id)

    if not survey_response:
        raise Exception("Survey response not found")

    return survey_response


def get_all_survey_responses(db: Session):
    return survey_response_repo.get_all(db)


def get_all_by_enrollment(db: Session, enrollment_id: int):
    return survey_response_repo.get_all_by_enrollment(db, enrollment_id)


def get_all_by_lesson_block(db: Session, lesson_block_id: int):
    return survey_response_repo.get_all_by_lesson_block(db, lesson_block_id)


def update_survey_response(
    db: Session, survey_response_id: int, data: SurveyResponseUpdate
):
    survey_response = get_survey_response(db, survey_response_id)

    return survey_response_repo.update(db, survey_response, data)


def delete_survey_response(db: Session, survey_response_id: int):
    survey_response = get_survey_response(db, survey_response_id)

    return survey_response_repo.delete(db, survey_response)
"""
