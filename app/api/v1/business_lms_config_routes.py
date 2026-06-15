from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import business_lms_config_service
from app.utils.jwt import get_current_user

router = APIRouter()


@router.get("/me/modules")
def get_my_modules(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return business_lms_config_service.get_enabled_configs(
        db,
        user["domain"],
    )
