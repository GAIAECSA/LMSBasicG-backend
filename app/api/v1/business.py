from fastapi import APIRouter, Depends, Request

from app.utils.jwt import get_current_user

router = APIRouter()


@router.get("/me/modules")
def get_my_modules(
    request: Request,
    user=Depends(get_current_user),
):
    return request.state.enabled_modules
