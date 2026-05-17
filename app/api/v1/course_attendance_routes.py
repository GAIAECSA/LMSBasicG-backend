from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.schemas.course_attendance import (
    CourseAttendanceCreate,
    CourseAttendanceUpdate,
    CourseAttendanceResponse
)

from app.services import course_attendance_service
from app.utils.jwt import get_current_user


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/course-attendance",
    response_model=CourseAttendanceResponse
)
def create_course_attendance(
    data: CourseAttendanceCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return course_attendance_service.create_course_attendance(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/course-attendance/{attendance_id}",
    response_model=CourseAttendanceResponse
)
def update_course_attendance(
    attendance_id: int,
    data: CourseAttendanceUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return course_attendance_service.update_course_attendance(
            db,
            attendance_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/course-attendance/{attendance_id}")
def delete_course_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        course_attendance_service.delete_course_attendance(
            db,
            attendance_id
        )

        return {"detail": "Asistencia eliminada"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/course-attendance/{attendance_id}",
    response_model=CourseAttendanceResponse
)
def get_course_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    try:
        return course_attendance_service.get_course_attendance(
            db,
            attendance_id
        )

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/course-attendance/course/{course_id}",
    response_model=list[CourseAttendanceResponse]
)
def get_all_course_attendance(
    course_id: int,
    db: Session = Depends(get_db)
):
    try:
        return course_attendance_service.get_course_attendances_by_course(
            db,
            course_id
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))