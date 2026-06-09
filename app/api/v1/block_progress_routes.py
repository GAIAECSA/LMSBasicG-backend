from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.block_progress import (
    BlockProgressCreate,
    BlockProgressResponse,
    BlockProgressUpdate,
)
from app.services import block_progress_service
from app.utils.jwt import get_current_user, require_admin

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/progress/{progress_id}", response_model=BlockProgressResponse)
def get_block_progress(
    progress_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    try:
        return block_progress_service.get_block_progress(db, progress_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/progress/enrollment/{enrollment_id}", response_model=list[BlockProgressResponse]
)
def get_progress_by_enrollment(
    enrollment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    try:
        return block_progress_service.get_progress_by_enrollment(db, enrollment_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/progress/complete")
def complete_block(
    enrollment_id: int,
    lesson_block_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return block_progress_service.complete_block(db, enrollment_id, lesson_block_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
