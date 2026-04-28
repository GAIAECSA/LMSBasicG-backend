from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.course import CourseCreate, CourseUpdate,CourseResponse
from app.services import course_service
from app.utils.jwt import require_admin
router = APIRouter()

@router.post("/", response_model=CourseResponse)
def create_course(
    data: CourseCreate = Depends(CourseCreate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    try:
        return course_service.create_course(db, data, image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    data: CourseUpdate = Depends(CourseUpdate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    try:
        return course_service.update_course(db, course_id, data, image)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    try:
        course_service.delete_course(db, course_id)
        return {"detail": "Course deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):  
    try:
        return course_service.get_course(db, course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/subcategory/{subcategory_id}", response_model=list[CourseResponse])
def get_courses_by_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    try:
        return course_service.get_courses_by_subcategory(db, subcategory_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    try:
        return course_service.get_all_courses(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    