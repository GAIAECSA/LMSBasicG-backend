from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.lesson_block_type import LessonBlockTypeCreate, LessonBlockTypeUpdate, LessonBlockTypeResponse
from app.services import lesson_block_type_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@router.post("/lesson-block-types", response_model=LessonBlockTypeResponse)
#def create_lesson_block_type(data: LessonBlockTypeCreate, db: Session = Depends(get_db)):
    #try:
        #return lesson_block_type_service.create_lesson_block_type(db, data)
    #except Exception as e:
        #raise HTTPException(status_code=400, detail=str(e))
    
#@router.put("/lesson-block-types/{lesson_block_type_id}", response_model=LessonBlockTypeResponse)
#def update_lesson_block_type(lesson_block_type_id: int, data: LessonBlockTypeUpdate, db: Session = Depends(get_db)):
    #try:
        #return lesson_block_type_service.update_lesson_block_type(db, lesson_block_type_id, data)
    #except Exception as e:
        #raise HTTPException(status_code=400, detail=str(e))
    
#@router.delete("/lesson-block-types/{lesson_block_type_id}")
#def delete_lesson_block_type(lesson_block_type_id: int, db: Session = Depends(get_db)):
    #try:
        #lesson_block_type_service.delete_lesson_block_type(db, lesson_block_type_id)
        #return {"detail": "Tipo de bloque de lección eliminado"}
    #except Exception as e:
        #raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/lesson-block-types/{lesson_block_type_id}", response_model=LessonBlockTypeResponse)
def get_lesson_block_type(lesson_block_type_id: int, db: Session = Depends(get_db)):
    try:
        return lesson_block_type_service.get_lesson_block_type(db, lesson_block_type_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/lesson-block-types", response_model=list[LessonBlockTypeResponse])
def get_all_lesson_block_types(db: Session = Depends(get_db)):
    try:
        return lesson_block_type_service.get_all_lesson_block_types(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
