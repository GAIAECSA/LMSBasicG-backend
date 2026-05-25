# app/api/v1/privacy_policy_routes.py

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal

from app.schemas.privacy_policy import (
    PrivacyPolicyCreate,
    PrivacyPolicyUpdate,
    PrivacyPolicyResponse,
)

from app.services import privacy_policy_service

from app.utils.jwt import require_admin, get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/", response_model=PrivacyPolicyResponse)
def create_privacy_policy(
    data: PrivacyPolicyCreate = Depends(PrivacyPolicyCreate.as_form),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    try:

        return privacy_policy_service.create_privacy_policy(db, data, file)

    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{privacy_policy_id}", response_model=PrivacyPolicyResponse)
def get_privacy_policy(
    privacy_policy_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:

        return privacy_policy_service.get_privacy_policy(db, privacy_policy_id)

    except Exception as e:

        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[PrivacyPolicyResponse])
def get_all_privacy_policies(
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return privacy_policy_service.get_all_privacy_policies(db)


@router.get("/active/current", response_model=PrivacyPolicyResponse)
def get_active_privacy_policy(db: Session = Depends(get_db)):
    try:

        return privacy_policy_service.get_active_privacy_policy(db)

    except Exception as e:

        raise HTTPException(status_code=404, detail=str(e))
