from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.course import CourseCreate, CourseUpdate,CourseResponse
from app.services import course_service

router = APIRouter()

@router.post("/courses", response_model=CourseResponse)
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    try:
        return course_service.create_course(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, data: CourseUpdate, db: Session = Depends(get_db)):
    try:
        return course_service.update_course(db, course_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        course_service.delete_course(db, course_id)
        return {"detail": "Curso eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return course

@router.get("/subcategory/{subcategory_id}/courses/", response_model=list[CourseResponse])
def get_courses_by_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    return course_service.get_courses_by_subcategory(db, subcategory_id)

@router.get("/courses/", response_model=list[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    return course_service.get_all_courses(db)