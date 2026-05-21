from fastapi import (APIRouter,Depends,HTTPException,UploadFile,File)

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.homework_response import (HomeworkResponseCreate,HomeworkResponseUpdate,HomeworkResponseGrade,HomeworkResponseResponse)
from app.services import homework_response_service
from app.utils.jwt import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/homework-response",response_model=HomeworkResponseResponse)
def create_homework_response(
    data: HomeworkResponseCreate = Depends(HomeworkResponseCreate.as_form),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return homework_response_service.create_homework_response(db,data,file)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


@router.put("/homework-response/{homework_response_id}",response_model=HomeworkResponseResponse)
def update_homework_response(
    homework_response_id: int,
    data: HomeworkResponseUpdate = Depends(HomeworkResponseUpdate.as_form),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return homework_response_service.update_homework_response(db,homework_response_id,data,file)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


@router.put("/homework-response/{homework_response_id}/grade",response_model=HomeworkResponseResponse)
def grade_homework_response(
    homework_response_id: int,
    data: HomeworkResponseGrade = Depends(HomeworkResponseGrade.as_form),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return homework_response_service.grade_homework_response(db,homework_response_id,data)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.delete("/homework-response/{homework_response_id}",response_model=HomeworkResponseResponse)
def delete_homework_response(
    homework_response_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return homework_response_service.delete_homework_response(db,homework_response_id)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/homework-response/{homework_response_id}",response_model=HomeworkResponseResponse)
def get_homework_response(
    homework_response_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return homework_response_service.get_homework_response(db,homework_response_id)
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))

@router.get("/homework-response/enrollment/{enrollment_id}",response_model=list[HomeworkResponseResponse])
def get_homework_responses_by_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return (homework_response_service.get_homework_responses_by_enrollment(db,enrollment_id))
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/homework-response/lesson-block/{lesson_block_id}",response_model=list[HomeworkResponseResponse])
def get_homework_responses_by_lesson_block(
    lesson_block_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return (homework_response_service.get_homework_responses_by_lesson_block(db,lesson_block_id))
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/homework-response/enrollment/{enrollment_id}/lesson-block/{lesson_block_id}",response_model=HomeworkResponseResponse)
def get_homework_response_by_enrollment_and_block(
    enrollment_id: int,
    lesson_block_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return (homework_response_service.get_homework_response_by_enrollment_and_block(db,enrollment_id,lesson_block_id))
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))