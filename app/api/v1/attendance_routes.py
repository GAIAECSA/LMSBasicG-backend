from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.attendance import (AttendanceUpdate,AttendanceResponse,AttendanceWithEnrollmentResponse)
from app.services import attendance_service
from app.utils.jwt import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put("/attendance/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: int, data: AttendanceUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return attendance_service.update_attendance(db, attendance_id, data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/attendance/{attendance_id}", response_model=AttendanceWithEnrollmentResponse)
def get_attendance(attendance_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return attendance_service.get_attendance(db, attendance_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/attendance/course-attendance/{course_attendance_id}", response_model=list[AttendanceWithEnrollmentResponse])
def get_all_attendance_by_course_attendance(course_attendance_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return attendance_service.get_all_attendance_by_course_attendance(db, course_attendance_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))