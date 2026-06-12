from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import business_lms_config_service
from app.utils.jwt import get_current_user

router = APIRouter()


@router.get("/me/modules")
def get_my_modules(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    business = getattr(
        request.state,
        "business",
        None,
    )

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Empresa no encontrada para este dominio",
        )

    return business_lms_config_service.get_enabled_configs(
        db,
        business.id,
    )
