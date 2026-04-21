from fastapi import APIRouter

from app.api.v1 import (
    role_routes as role,
    user_routes as user,
    category_routes as category
)

router = APIRouter()

router.include_router(
    role.router,
    prefix="/roles",
    tags=["roles"]
)

router.include_router(
    user.router,
    prefix="/users",
    tags=["users"]
)

router.include_router(
    category.router,
    prefix="/categories",
    tags=["categories"]
)
