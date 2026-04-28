from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.certificate import (
    CertificateCreate,
    CertificateUpdate,
    CertificateResponse
)
from app.services import certificate_service
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.utils.jwt import require_admin, get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CertificateResponse)
def create_certificate(
    data: CertificateCreate = Depends(CertificateCreate.as_form),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    try:
        return certificate_service.create_certificate(db, data, file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{certificate_id}", response_model=CertificateResponse)
def update_certificate(
    certificate_id: int,
    data: CertificateUpdate = Depends(CertificateUpdate.as_form),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    try:
        return certificate_service.update_certificate(db, certificate_id, data, file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{certificate_id}")
def delete_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    try:
        return certificate_service.delete_certificate(db, certificate_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{certificate_id}", response_model=CertificateResponse)
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return certificate_service.get_certificate(db, certificate_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[CertificateResponse])
def get_all_certificates(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return certificate_service.get_all_certificates(db)

@router.get("/user/{user_id}", response_model=List[CertificateResponse])
def get_certificates_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return certificate_service.get_certificates_by_user(db, user_id)

@router.get("/verify/{code}", response_model=CertificateResponse)
def verify_certificate(
    code: str,
    db: Session = Depends(get_db)
):
    try:
        return certificate_service.verify_certificate(db, code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/code/{code}", response_model=CertificateResponse)
def get_certificate_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    try:
        return certificate_service.get_certificate_by_code(db, code)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/verify/{code}", response_model=CertificateResponse)
def verify_certificate(
    code: str,
    db: Session = Depends(get_db)
):
    try:
        return certificate_service.verify_certificate(db, code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
