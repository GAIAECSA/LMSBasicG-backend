from fastapi import APIRouter

from app.api.v1 import (
    role_routes as role,
    user_routes as user,
    category_routes as category,
    subcategory_routes as subcategory,
    course_routes as course,
    module_routes as module,
    lesson_routes as lesson,
    lesson_block_routes as lesson_block,
    block_progress_routes as block_progress,
    lesson_block_type_routes as lesson_block_type,
    enrollment_routes as enrollment,
    websocket_routes as websocket
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

router.include_router(
    lesson_block.router,
    prefix="/lesson-blocks",
    tags=["lesson-blocks"]
)

router.include_router(
    block_progress.router,
    prefix="/blocks-progress",
    tags=["blocks-progress"]
)

router.include_router(
    lesson_block_type.router,
    prefix="/lesson-block-types",
    tags=["lesson-block-types"]
)

router.include_router(
    enrollment.router,
    prefix="/enrollments",
    tags=["enrollments"]
)

# Websocket

router.include_router(
    websocket.router,
    prefix="/websockets",
    tags=["websocket"]
)