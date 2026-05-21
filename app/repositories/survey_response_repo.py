from sqlalchemy.orm import Session

from app.models.survey_response import SurveyResponse
from app.schemas.survey_response import (
    SurveyResponseCreate,
    SurveyResponseUpdate
)


def create(
    db: Session,
    data: SurveyResponseCreate
):
    survey_response = SurveyResponse(
        **data.model_dump()
    )

    db.add(survey_response)

    db.commit()
    db.refresh(survey_response)

    return survey_response


def get_by_id(
    db: Session,
    survey_response_id: int
):
    return db.query(SurveyResponse).filter(
        SurveyResponse.id == survey_response_id,
        SurveyResponse.deleted == False
    ).first()


def get_all(db: Session):
    return db.query(SurveyResponse).filter(
        SurveyResponse.deleted == False
    ).all()


def get_all_by_enrollment(
    db: Session,
    enrollment_id: int
):
    return db.query(SurveyResponse).filter(
        SurveyResponse.enrollment_id == enrollment_id,
        SurveyResponse.deleted == False
    ).all()


def get_all_by_lesson_block(
    db: Session,
    lesson_block_id: int
):
    return db.query(SurveyResponse).filter(
        SurveyResponse.lesson_block_id == lesson_block_id,
        SurveyResponse.deleted == False
    ).all()


def update(
    db: Session,
    survey_response: SurveyResponse,
    data: SurveyResponseUpdate
):
    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(survey_response, key, value)

    db.commit()
    db.refresh(survey_response)

    return survey_response


def delete(
    db: Session,
    survey_response: SurveyResponse
):
    survey_response.deleted = True

    db.commit()
    db.refresh(survey_response)

    return survey_response