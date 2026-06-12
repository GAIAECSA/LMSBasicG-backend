from fastapi import APIRouter

from app.api.v1 import attendance_routes as attendance
from app.api.v1 import block_progress_routes as block_progress
from app.api.v1 import category_routes as category
from app.api.v1 import certificate_routes as certificate
from app.api.v1 import certificate_template_routes as certificate_template
from app.api.v1 import course_attendance_routes as course_attendance
from app.api.v1 import course_routes as course
from app.api.v1 import enrollment_routes as enrollment
from app.api.v1 import forum_response_routes as forum_response
from app.api.v1 import homework_response_routes as homework_response
from app.api.v1 import lesson_block_routes as lesson_block
from app.api.v1 import lesson_block_type_routes as lesson_block_type
from app.api.v1 import lesson_routes as lesson
from app.api.v1 import mdt_certificate_routes as mdt_certificate
from app.api.v1 import module_routes as module
from app.api.v1 import privacy_policy_routes as privacy_policy
from app.api.v1 import quizz_response_routes as quizz_response
from app.api.v1 import role_routes as role
from app.api.v1 import subcategory_routes as subcategory
from app.api.v1 import survey_response_router as survey_response
from app.api.v1 import user_privacy_policy_routes as user_privacy_policy
from app.api.v1 import user_routes as user
from app.api.v1 import websocket_routes as websocket
from app.api.v1.business_lms_config import business_lms_config_service

# features
from app.features.zoom import zoom_routes as zoom
from app.reports import reports as reports

router = APIRouter()

router.include_router(role.router, prefix="/roles", tags=["roles"])

router.include_router(user.router, prefix="/users", tags=["users"])

router.include_router(category.router, prefix="/categories", tags=["categories"])

router.include_router(
    subcategory.router, prefix="/subcategories", tags=["subcategories"]
)

router.include_router(course.router, prefix="/courses", tags=["courses"])

router.include_router(module.router, prefix="/modules", tags=["modules"])

router.include_router(lesson.router, prefix="/lessons", tags=["lessons"])

router.include_router(
    lesson_block.router, prefix="/lesson-blocks", tags=["lesson-blocks"]
)

router.include_router(
    block_progress.router, prefix="/blocks-progress", tags=["blocks-progress"]
)

router.include_router(
    lesson_block_type.router, prefix="/lesson-block-types", tags=["lesson-block-types"]
)

router.include_router(enrollment.router, prefix="/enrollments", tags=["enrollments"])

router.include_router(
    certificate_template.router,
    prefix="/certificate_templates",
    tags=["certificate_templates"],
)

router.include_router(certificate.router, prefix="/certificates", tags=["certificates"])

router.include_router(
    course_attendance.router, prefix="/course_attendance", tags=["course_attendance"]
)

router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])

router.include_router(
    privacy_policy.router, prefix="/privacy-policy", tags=["privacy-policy"]
)

router.include_router(
    mdt_certificate.router, prefix="/mdt-certificates", tags=["mdt-certificates"]
)

router.include_router(reports.router, prefix="/reports", tags=["reports"])
# User response

router.include_router(
    quizz_response.router, prefix="/quizz-response", tags=["quizz-response"]
)

router.include_router(
    homework_response.router, prefix="/homework-response", tags=["homework-response"]
)

router.include_router(
    survey_response.router, prefix="/survey-response", tags=["survey-response"]
)

router.include_router(
    forum_response.router, prefix="/forum-response", tags=["forum-response"]
)

router.include_router(
    user_privacy_policy.router,
    prefix="/user-privacy-policy",
    tags=["user-privacy-policy"],
)
# Websocket

router.include_router(websocket.router, prefix="/websockets", tags=["websocket"])

# Features
router.include_router(zoom.router, prefix="/zoom", tags=["zoom"])

# Business
router.include_router(
    business_lms_config_service.router,
    prefix="/business-lms-config",
    tags=["business-lms-config"],
)
