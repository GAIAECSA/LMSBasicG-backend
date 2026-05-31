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
from app.services import mdt_certificate_service

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


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
    response_model=MdtCertificateResponse,  # Ahora devuelve un solo objeto
)
def get_certificate_by_id_number_and_course(
    id_number: str,
    course_id: int,  # Nuevo parámetro requerido (?course_id=X)
    db: Session = Depends(get_db),
):
    try:
        return mdt_certificate_service.get_certificate_by_id_and_course(
            db=db,
            id_number=id_number,
            course_id=course_id,
        )
    except ValueError as e:
        # Si el certificado no existe para esa combinación, disparamos 404
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
