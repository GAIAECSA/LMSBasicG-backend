from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.quizz_response import (
    QuizzResponseCreate,
    QuizzResponseUpdate,
    QuizzResponseResponse
)
from app.services import quizz_response_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/quiz-responses", response_model=QuizzResponseResponse)
def create_quizz_response(data: QuizzResponseCreate, db: Session = Depends(get_db)):
    try:
        return quizz_response_service.create_quizz_response(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/quiz-responses/{quizz_response_id}", response_model=QuizzResponseResponse)
def update_quizz_response(quizz_response_id: int, data: QuizzResponseUpdate, db: Session = Depends(get_db)):
    try:
        return quizz_response_service.update_quizz_response(db, quizz_response_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/quiz-responses/enrollment/{enrollment_id}", response_model=list[QuizzResponseResponse])
def get_by_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        return quizz_response_service.get_by_enrollment(db, enrollment_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/quiz-responses/lesson-block/{lesson_block_id}", response_model=list[QuizzResponseResponse])
def get_by_block(lesson_block_id: int, db: Session = Depends(get_db)):
    try:
        return quizz_response_service.get_by_block(db, lesson_block_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/quiz-responses/{quizz_response_id}", response_model=QuizzResponseResponse)
def get_quizz_response(quizz_response_id: int, db: Session = Depends(get_db)):
    try:
        return quizz_response_service.get_quizz_response(db, quizz_response_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/quiz-responses/{quizz_response_id}")
def delete_quizz_response(quizz_response_id: int, db: Session = Depends(get_db)):
    try:
        quizz_response_service.delete_quizz_response(db, quizz_response_id)
        return {"detail": "Respuesta eliminada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))