from fastapi import APIRouter

from app.api.v1 import (
    role_routes as role,
    user_routes as user,
    category_routes as category,
    subcategory_routes as subcategory,
    course_routes as course,
    module_routes as module,
    lesson_routes as lesson,
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

router.include_router(
    subcategory.router,
    prefix="/subcategories",
    tags=["subcategories"]
)

router.include_router(
    course.router,
    prefix="/courses",
    tags=["courses"]
)

router.include_router(
    module.router,
    prefix="/modules",
    tags=["modules"]
)

router.include_router(
    lesson.router,
    prefix="/lessons",
    tags=["lessons"]
)