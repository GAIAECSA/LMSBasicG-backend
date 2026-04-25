from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.block_progress import (
    BlockProgressCreate,
    BlockProgressUpdate,
    BlockProgressResponse
)
from app.services import block_progress_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/progress", response_model=BlockProgressResponse)
def create_block_progress(data: BlockProgressCreate, db: Session = Depends(get_db)):
    try:
        return block_progress_service.create_block_progress(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/progress/{progress_id}", response_model=BlockProgressResponse)
def update_block_progress(progress_id: int, data: BlockProgressUpdate, db: Session = Depends(get_db)):
    try:
        return block_progress_service.update_block_progress(db, progress_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/progress/{progress_id}", response_model=BlockProgressResponse)
def get_block_progress(progress_id: int, db: Session = Depends(get_db)):
    try:
        return block_progress_service.get_block_progress(db, progress_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/progress/enrollment/{enrollment_id}", response_model=list[BlockProgressResponse])
def get_progress_by_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        return block_progress_service.get_progress_by_enrollment(db, enrollment_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/progress/complete")
def complete_block(enrollment_id: int, lesson_block_id: int, db: Session = Depends(get_db)):
    try:
        return block_progress_service.complete_block(db, enrollment_id, lesson_block_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/progress/{progress_id}")
def delete_block_progress(progress_id: int, db: Session = Depends(get_db)):
    try:
        block_progress_service.delete_block_progress(db, progress_id)
        return {"detail": "Progreso eliminado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))