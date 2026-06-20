from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.schemas.others.auth import UserSession
from app.services import course_service
from app.utils.jwt import get_current_user, require_admin

router = APIRouter()


@router.post("/", response_model=CourseResponse)
def create_course(
    data: CourseCreate = Depends(CourseCreate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(require_admin),
):
    try:
        return course_service.create_course(db, data, current_user.business_id, image)
    except course_service.CourseAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    data: CourseUpdate = Depends(CourseUpdate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(require_admin),
):
    try:
        return course_service.update_course(
            db, course_id, data, current_user.business_id, image
        )
    except course_service.CourseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except course_service.CourseAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(require_admin),
):
    try:
        course_service.delete_course(db, course_id, current_user.business_id)
        return {"detail": "Course deleted successfully"}
    except course_service.CourseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return course_service.get_course(db, course_id, current_user.business_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/subcategory/{subcategory_id}", response_model=list[CourseResponse])
def get_courses_by_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return course_service.get_courses_by_subcategory(
            db, subcategory_id, current_user.business_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CourseResponse])
def get_all_courses(
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return course_service.get_all_courses(db, current_user.business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


"""
@router.post("/", response_model=CourseResponse)
def create_course(
    data: CourseCreate = Depends(CourseCreate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(require_admin),
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
    user=Depends(require_admin),
):
    try:
        return course_service.update_course(db, course_id, data, image)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{course_id}")
def delete_course(
    course_id: int, db: Session = Depends(get_db), user=Depends(require_admin)
):
    try:
        course_service.soft_delete_course_cascade(db, course_id)
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
"""
