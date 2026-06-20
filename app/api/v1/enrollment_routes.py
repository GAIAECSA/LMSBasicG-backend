from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas import enrollment
from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse,
    EnrollmentUpdate,
    MassiveEnrollmentCreate,
    MassiveEnrollmentResult,
)
from app.schemas.others.auth import UserSession
from app.schemas.user import UserCreate
from app.services import course_service, enrollment_service
from app.utils.jwt import get_current_user, require_admin
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
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return enrollment_service.create_enrollment(
            db, data, current_user.business_id, image
        )

    except enrollment_service.EnrollmentPendingError as e:
        raise HTTPException(status_code=409, detail=str(e))

    except enrollment_service.EnrollmentAcceptedError as e:
        raise HTTPException(status_code=409, detail=str(e))

    except enrollment_service.EnrollmentDeniedError as e:
        raise HTTPException(status_code=409, detail=str(e))

    except course_service.CourseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(
    enrollment_id: int,
    data: EnrollmentUpdate = Depends(EnrollmentUpdate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return enrollment_service.update_enrollment(
            db, enrollment_id, data, current_user.business_id, image
        )

    except course_service.CourseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/enrollments/{enrollment_id}")
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(require_admin),
):
    try:
        enrollment_service.delete_enrollment(
            db, enrollment_id, current_user.business_id
        )
        return {"detail": "Inscripción eliminada"}
    except course_service.CourseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/enrollments/by-course-role", response_model=list[EnrollmentResponse])
def get_by_course_and_role(
    course_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return enrollment_service.get_enrollments_by_course_and_role(
            db, course_id, role_id, current_user.business_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enrollments/by-user", response_model=list[EnrollmentResponse])
def get_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return enrollment_service.get_enrollments_by_user(
            db, user_id, current_user.business_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enrollments/by-role", response_model=list[EnrollmentResponse])
def get_by_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return enrollment_service.get_enrollments_by_role(
            db, role_id, current_user.business_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return enrollment_service.get_enrollment(
            db, enrollment_id, current_user.business_id
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/enrollments/massive",
    response_model=MassiveEnrollmentResult,
)
def create_enrollments_massive(
    payload: MassiveEnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(require_admin),
):
    try:
        return enrollment_service.create_massive_enrollments(
            db=db,
            users=payload.users,
            course_id=payload.course_id,
            business_id=current_user.business_id,
        )

    except course_service.CourseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


"""
@router.post("/enrollments", response_model=EnrollmentResponse)
def create_enrollment(
    data: EnrollmentCreate = Depends(EnrollmentCreate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        enrollment = enrollment_service.create_enrollment(db, data, image)

        # if enrollment.role_id == 4:
        #   await manager.ConnectionManager.send_to_admins({
        #      "event": "new_student_enrollment",
        #     "message": "Nuevo estudiante matriculado"
        # })

        return enrollment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(
    enrollment_id: int,
    data: EnrollmentUpdate = Depends(EnrollmentUpdate.as_form),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return enrollment_service.update_enrollment(db, enrollment_id, data, image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/enrollments/{enrollment_id}")
def delete_enrollment(
    enrollment_id: int, db: Session = Depends(get_db), user=Depends(require_admin)
):
    try:
        enrollment_service.delete_enrollment(db, enrollment_id)
        return {"detail": "Inscripción eliminada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enrollments/by-course-role", response_model=list[EnrollmentResponse])
def get_by_course_and_role(
    course_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return enrollment_service.get_enrollments_by_course_and_role(
            db, course_id, role_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enrollments/by-user", response_model=list[EnrollmentResponse])
def get_by_user(
    user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    try:
        return enrollment_service.get_enrollments_by_user(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enrollments/by-role", response_model=list[EnrollmentResponse])
def get_by_role(
    role_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    try:
        return enrollment_service.get_enrollments_by_role(db, role_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(
    enrollment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    try:
        return enrollment_service.get_enrollment(db, enrollment_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/enrollments/massive",
    response_model=MassiveEnrollmentResult,
)
def create_enrollments_massive(
    payload: MassiveEnrollmentCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    try:
        return enrollment_service.create_massive_enrollments(
            db=db,
            users=payload.users,
            course_id=payload.course_id,
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
"""
