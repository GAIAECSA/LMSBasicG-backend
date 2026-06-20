from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.others.auth import UserSession
from app.schemas.survey_response import SurveyResponseCreate, SurveyResponseResponse
from app.services import survey_response_service
from app.utils.jwt import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=SurveyResponseResponse)
def create_survey_response(
    data: SurveyResponseCreate,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return survey_response_service.create_survey_response(
            db, data, current_user.business_id
        )
    except survey_response_service.SurveyResponseAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=list[SurveyResponseResponse])
def get_all_survey_responses(
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return survey_response_service.get_all_survey_responses(
            db, current_user.business_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{survey_response_id}", response_model=SurveyResponseResponse)
def get_survey_response(
    survey_response_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return survey_response_service.get_survey_response(
            db, survey_response_id, current_user.business_id
        )
    except survey_response_service.SurveyResponseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/enrollment/{enrollment_id}", response_model=list[SurveyResponseResponse])
def get_all_by_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return survey_response_service.get_all_by_enrollment(
            db, enrollment_id, current_user.business_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get(
    "/lesson-block/{lesson_block_id}", response_model=list[SurveyResponseResponse]
)
def get_all_by_lesson_block(
    lesson_block_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return survey_response_service.get_all_by_lesson_block(
            db, lesson_block_id, current_user.business_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


"""

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
"""
