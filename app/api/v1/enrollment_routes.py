from app.schemas import enrollment
from app.websockets import manager
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse
from app.services import enrollment_service
from app.websockets import manager

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/enrollments", response_model=EnrollmentResponse)
def create_enrollment(
        data: EnrollmentCreate = Depends(EnrollmentCreate.as_form),
        image: UploadFile = File(None),
        db: Session = Depends(get_db)
    ):
    try:
        enrollment = enrollment_service.create_enrollment(db, data, image)

        #if enrollment.role_id == 4:
         #   await manager.ConnectionManager.send_to_admins({
          #      "event": "new_student_enrollment",
           #     "message": "Nuevo estudiante matriculado"
            #})

        return enrollment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(enrollment_id: int, data: EnrollmentUpdate = Depends(EnrollmentUpdate.as_form), image: UploadFile = File(None), db: Session = Depends(get_db)):
    try:
        return enrollment_service.update_enrollment(db, enrollment_id, data, image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        enrollment_service.delete_enrollment(db, enrollment_id)
        return {"detail": "Inscripción eliminada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/enrollments/by-course-role", response_model=list[EnrollmentResponse])
def get_by_course_and_role(course_id: int, role_id: int, db: Session = Depends(get_db)):
    try:
        return enrollment_service.get_enrollments_by_course_and_role(db, course_id, role_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/enrollments/by-role", response_model=list[EnrollmentResponse])
def get_by_role(role_id: int, db: Session = Depends(get_db)):
    try:
        return enrollment_service.get_enrollments_by_role(db, role_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        return enrollment_service.get_enrollment(db, enrollment_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))