from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request, Form
from sqlalchemy.orm import Session
import json
from app.db.session import get_db
from app.schemas.certificate_template import (
    CertificateTemplateCreate,
    CertificateTemplateUpdate,
    CertificateTemplateResponse
)
from app.services import certificate_template_service

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.utils.jwt import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CertificateTemplateResponse)
async def create_template(
    request: Request,
    data: str = Form(...),
    background_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    payload = json.loads(data)

    return await certificate_template_service.create_certificate_template(
        db=db,
        data=payload,
        background_image=background_image,
        request=request
    )


@router.put("/{template_id}", response_model=CertificateTemplateResponse)
async def update_template(
    template_id: int,
    request: Request,
    data: str = Form(...),
    background_image: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    payload = json.loads(data)

    return await certificate_template_service.update_certificate_template(
        db=db,
        template_id=template_id,
        data=payload,
        background_image=background_image,
        request=request
    )
    


@router.delete("/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    try:
        return certificate_template_service.delete_certificate_template(
            db, template_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[CertificateTemplateResponse])
def get_all_templates(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return certificate_template_service.get_all_certificate_templates(db)


@router.get("/course/{course_id}", response_model=CertificateTemplateResponse)
def get_template_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return certificate_template_service.get_certificate_template_by_course(
        db, course_id
    )

@router.get("/{template_id}", response_model=CertificateTemplateResponse)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return certificate_template_service.get_certificate_template(
            db, template_id
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))