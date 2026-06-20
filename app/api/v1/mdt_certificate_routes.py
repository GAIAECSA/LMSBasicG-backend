# api/v1/mdt_certificate_routes.py

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.mdt_certificate import (
    MdtBulkCertificateCreate,
    MdtCertificateCreate,
    MdtCertificateResponse,
    MdtCertificateUpdate,
)
from app.schemas.others.auth import UserSession
from app.services import mdt_certificate_service
from app.utils.jwt import get_current_user

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/", response_model=MdtCertificateResponse)
def create_certificate(
    data: MdtCertificateCreate = Depends(MdtCertificateCreate.as_form),
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return mdt_certificate_service.create_certificate(
            db=db,
            data=data,
            business_id=current_user.business_id,
            file=file,
        )

    except mdt_certificate_service.MDTFileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bulk")
def create_certificates_bulk(
    data: MdtBulkCertificateCreate = Depends(MdtBulkCertificateCreate.as_form),
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):

    try:

        return mdt_certificate_service.create_certificates_bulk(
            db=db,
            data=data,
            business_id=current_user.business_id,
            files=files,
        )

    except mdt_certificate_service.MDTFileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{certificate_id}", response_model=MdtCertificateResponse)
def get_certificate_by_id(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):

    try:
        return mdt_certificate_service.get_certificate_by_id(
            db=db, certificate_id=certificate_id, business_id=current_user.business_id
        )
    except mdt_certificate_service.MDTFileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/course/{course_id}", response_model=list[MdtCertificateResponse])
def get_certificates_by_course_id(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):

    try:

        return mdt_certificate_service.get_certificates_by_course_id(
            db=db, course_id=course_id, business_id=current_user.business_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/id-number/{id_number}", response_model=MdtCertificateResponse)
def get_certificate_by_id_number_and_course(
    id_number: str,
    course_id: int,
    certificate_type: str,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return mdt_certificate_service.get_certificate_by_id_number_and_course(
            db=db,
            id_number=id_number,
            course_id=course_id,
            certificate_type=certificate_type,
            business_id=current_user.business_id,
        )
    except mdt_certificate_service.MDTFileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{certificate_id}", response_model=MdtCertificateResponse)
def delete_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):

    try:

        return mdt_certificate_service.delete_certificate(
            db=db, certificate_id=certificate_id, business_id=current_user.business_id
        )

    except mdt_certificate_service.MDTFileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""
@router.post(
    "/",
    response_model=MdtCertificateResponse,
)
def create_certificate(
    data: MdtCertificateCreate = Depends(MdtCertificateCreate.as_form),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    try:

        return mdt_certificate_service.create_certificate(
            db=db,
            data=data,
            file=file,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/bulk")
def create_certificates_bulk(
    data: MdtBulkCertificateCreate = Depends(MdtBulkCertificateCreate.as_form),
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):

    try:

        return mdt_certificate_service.create_certificates_bulk(
            db=db,
            data=data,
            files=files,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/{certificate_id}",
    response_model=MdtCertificateResponse,
)
def get_certificate_by_id(
    certificate_id: int,
    db: Session = Depends(get_db),
):

    try:

        return mdt_certificate_service.get_certificate_by_id(
            db=db,
            certificate_id=certificate_id,
        )

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.get(
    "/course/{course_id}",
    response_model=list[MdtCertificateResponse],
)
def get_certificates_by_course_id(
    course_id: int,
    db: Session = Depends(get_db),
):

    try:

        return mdt_certificate_service.get_certificates_by_course_id(
            db=db,
            course_id=course_id,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/id-number/{id_number}",
    response_model=MdtCertificateResponse,
)
def get_certificate_by_id_number_and_course(
    id_number: str,
    course_id: int,
    certificate_type: str,  # <-- Nuevo parámetro requerido (?certificate_type=MDT)
    db: Session = Depends(get_db),
):
    try:
        return mdt_certificate_service.get_certificate_by_id_number_and_course(
            db=db,
            id_number=id_number,
            course_id=course_id,
            certificate_type=certificate_type,  # <-- Se envía al servicio
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al procesar el certificado: {str(e)}",
        )


@router.put(
    "/{certificate_id}",
    response_model=MdtCertificateResponse,
)
def update_certificate(
    certificate_id: int,
    data: MdtCertificateUpdate = Depends(MdtCertificateUpdate.as_form),
    db: Session = Depends(get_db),
):

    try:

        return mdt_certificate_service.update_certificate(
            db=db,
            certificate_id=certificate_id,
            data=data,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete(
    "/{certificate_id}",
    response_model=MdtCertificateResponse,
)
def delete_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
):

    try:

        return mdt_certificate_service.delete_certificate(
            db=db,
            certificate_id=certificate_id,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
"""
