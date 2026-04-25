from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.lesson_block import LessonBlockCreate, LessonBlockUpdate, LessonBlockResponse
from app.services import lesson_block_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/lesson-blocks")
def create_lesson_block(
    data: LessonBlockCreate = Depends(LessonBlockCreate.as_form),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        return lesson_block_service.create_lesson_block(db, data, file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/lesson-blocks/{lesson_block_id}", response_model=LessonBlockResponse)
def update_lesson_block(lesson_block_id: int, data: LessonBlockUpdate = Depends(LessonBlockUpdate.as_form), file: UploadFile = File(None), db: Session = Depends(get_db)):
    try:
        return lesson_block_service.update_lesson_block(db, lesson_block_id, data, file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/lesson-blocks/{lesson_block_id}")
def delete_lesson_block(lesson_block_id: int, db: Session = Depends(get_db)):
    try:
        lesson_block_service.delete_lesson_block(db, lesson_block_id)
        return {"detail": "Bloque eliminado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/lesson-blocks/{lesson_block_id}", response_model=LessonBlockResponse)
def get_lesson_block(lesson_block_id: int, db: Session = Depends(get_db)):
    try:
        return lesson_block_service.get_lesson_block(db, lesson_block_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/lesson/{lesson_id}/lesson-blocks", response_model=list[LessonBlockResponse])
def get_by_lesson(lesson_id: int,db: Session = Depends(get_db)):
    try:
        return lesson_block_service.get_by_lesson(db, lesson_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))