from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.survey_response import (
    SurveyResponseCreate,
    SurveyResponseUpdate,
    SurveyResponseResponse,
)
from app.services import survey_response_service

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/", response_model=SurveyResponseResponse)
def create_survey_response(data: SurveyResponseCreate, db: Session = Depends(get_db)):
    try:
        return survey_response_service.create_survey_response(db, data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[SurveyResponseResponse])
def get_all_survey_responses(db: Session = Depends(get_db)):
    try:
        return survey_response_service.get_all_survey_responses(db)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{survey_response_id}", response_model=SurveyResponseResponse)
def get_survey_response(survey_response_id: int, db: Session = Depends(get_db)):
    try:
        return survey_response_service.get_survey_response(db, survey_response_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/enrollment/{enrollment_id}", response_model=list[SurveyResponseResponse])
def get_all_by_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        return survey_response_service.get_all_by_enrollment(db, enrollment_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/lesson-block/{lesson_block_id}", response_model=list[SurveyResponseResponse]
)
def get_all_by_lesson_block(lesson_block_id: int, db: Session = Depends(get_db)):
    try:
        return survey_response_service.get_all_by_lesson_block(db, lesson_block_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
