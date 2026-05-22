from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.schemas.user_privacy_policy import (
    UserPrivacyPolicyResponse,
)

from app.services import user_privacy_policy_service

from app.utils.jwt import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/accept/{privacy_policy_id}", response_model=UserPrivacyPolicyResponse)
def accept_privacy_policy(
    privacy_policy_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return user_privacy_policy_service.accept_privacy_policy(
            db, current_user["user_id"], privacy_policy_id
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
