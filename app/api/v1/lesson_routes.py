from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.lesson import LessonCreate, LessonUpdate, LessonResponse
from app.services import lesson_service
from app.utils.jwt import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/lessons", response_model=LessonResponse)
def create_lesson(data: LessonCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return lesson_service.create_lesson(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/lessons/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, data: LessonUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return lesson_service.update_lesson(db, lesson_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return lesson_service.delete_lesson(db, lesson_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return lesson_service.get_lesson(db, lesson_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/modules/{module_id}/lessons", response_model=list[LessonResponse])
def get_lessons_by_module(module_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return lesson_service.get_lessons_by_module(db, module_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))