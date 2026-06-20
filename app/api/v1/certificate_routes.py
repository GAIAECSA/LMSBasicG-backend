from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_db
from app.schemas.certificate import (
    CertificateCreate,
    CertificateResponse,
    CertificateUpdate,
)
from app.schemas.others.auth import UserSession
from app.services import business_service, certificate_service
from app.utils.jwt import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put("/{certificate_id}", response_model=CertificateResponse)
def update_certificate(
    certificate_id: int,
    data: CertificateUpdate = Depends(CertificateUpdate.as_form),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return certificate_service.update_certificate(
            db, certificate_id, data, current_user.business_id, file
        )
    except certificate_service.CertificateAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{certificate_id}", response_model=CertificateResponse)
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return certificate_service.get_certificate(
            db, certificate_id, current_user.business_id
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[CertificateResponse])
def get_all_certificates(
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    return certificate_service.get_all_certificates(db, current_user.business_id)


@router.get("/user/{user_id}", response_model=List[CertificateResponse])
def get_certificates_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    return certificate_service.get_certificates_by_user(
        db, user_id, current_user.business_id
    )


@router.get(
    "/verify/{code}",
    response_model=CertificateResponse,
)
def verify_certificate(
    code: str,
    domain: str,
    db: Session = Depends(get_db),
):
    try:
        return certificate_service.verify_certificate(
            db=db,
            code=code,
            domain=domain,
        )
    except business_service.BusinessNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except certificate_service.CertificateNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get(
    "/code/{code}",
    response_model=CertificateResponse,
)
def get_certificate_by_code(
    code: str,
    domain: str,
    db: Session = Depends(get_db),
):
    try:
        return certificate_service.get_certificate_by_code(
            db=db,
            code=code,
            domain=domain,
        )
    except business_service.BusinessNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except certificate_service.CertificateNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


"""
@router.put("/{certificate_id}", response_model=CertificateResponse)
def update_certificate(
    certificate_id: int,
    data: CertificateUpdate = Depends(CertificateUpdate.as_form),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return certificate_service.update_certificate(db, certificate_id, data, file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{certificate_id}", response_model=CertificateResponse)
def get_certificate(
    certificate_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
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
    user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return certificate_service.get_certificates_by_user(db, user_id)


@router.get("/verify/{code}", response_model=CertificateResponse)
def verify_certificate(code: str, db: Session = Depends(get_db)):
    try:
        return certificate_service.verify_certificate(db, code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/code/{code}", response_model=CertificateResponse)
def get_certificate_by_code(code: str, db: Session = Depends(get_db)):
    try:
        return certificate_service.get_certificate_by_code(db, code)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
"""
