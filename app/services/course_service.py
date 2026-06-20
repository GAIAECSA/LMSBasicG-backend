import os
import uuid

from fastapi import UploadFile
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.constants import constants_default_blocks_mdt
from app.models.block_progress import BlockProgress
from app.models.certificate import Certificate
from app.models.certificate_template import CertificateTemplate
from app.models.course import Course
from app.models.course_attendance import CourseAttendance
from app.models.enrollment import Enrollment
from app.models.forum_response import ForumResponse
from app.models.homework_response import HomeworkResponse
from app.models.lesson import Lesson
from app.models.lesson_block import LessonBlock
from app.models.mdt_certificate import MdtCertificate
from app.models.module import Module
from app.models.quizz_response import QuizzResponse
from app.models.survey_response import SurveyResponse
from app.repositories import (
    attendance_repo,
    block_progress_repo,
    certificate_repo,
    certificate_template_repo,
    course_attendance_repo,
    course_repo,
    enrollment_repo,
    forum_response_repo,
    homework_response_repo,
    lesson_block_repo,
    lesson_repo,
    mdt_certificate_repo,
    module_repo,
    quizz_response_repo,
    survey_response_repo,
)
from app.schemas.course import CourseCreate, CourseUpdate
from app.utils.file_upload import save_course_image

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class CourseNotFoundError(Exception):
    pass


class CourseAlreadyExistsError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def create_course(
    db: Session, data: CourseCreate, business_id: int, image: UploadFile | None = None
):
    with db.begin():
        existing = course_repo.get_by_name_and_subcategory(
            db, data.name, data.subcategory_id, business_id
        )
        if existing:
            raise CourseAlreadyExistsError("El curso ya existe")

        image_url = save_course_image(image, business_id) if image else None

        course = Course(
            **data.model_dump(), image_url=image_url, business_id=business_id
        )
        course_repo.create(course)
        lesson_block_repo.create_bulk(db, create_default_blocks(course.id, business_id))
        return course


def update_course(
    db: Session,
    course_id: int,
    data: CourseUpdate,
    business_id: int,
    image: UploadFile | None = None,
):
    with db.begin():
        course = course_repo.get_by_id(
            db=db,
            course_id=course_id,
            business_id=business_id,
        )

        if not course:
            raise CourseNotFoundError("Curso no encontrado")

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data:
            subcategory_id = update_data.get(
                "subcategory_id",
                course.subcategory_id,
            )

            existing = course_repo.get_by_name_and_subcategory(
                db=db,
                name=update_data["name"],
                subcategory_id=subcategory_id,
            )

            if existing and existing.id != course.id:
                raise CourseAlreadyExistsError("El curso ya existe")

        for key, value in update_data.items():
            setattr(course, key, value)

        if image:
            new_image = save_course_image(
                file=image,
                business_id=business_id,
            )

            if course.image_url:
                old_path = course.image_url.lstrip("/")

                try:
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except OSError:
                    pass

            course.image_url = new_image

        return course


def get_course(db: Session, course_id: int, business_id: int):
    return course_repo.get_by_id(db, course_id, business_id)


def get_courses_by_subcategory(db: Session, subcategory_id: int, business_id: int):
    return course_repo.get_by_subcategory_id(db, subcategory_id, business_id)


def get_all_courses(db: Session, business_id: int):
    return course_repo.get_all(db, business_id)


def delete_course(db: Session, course_id: int, business_id: int):
    with db.begin():
        course = course_repo.get_by_id(db, course_id, business_id)

        if not course:
            raise CourseNotFoundError("Curso no encontrado")
        cascade_steps = [
            # Blocks
            homework_response_repo.delete_soft_by_course(),
            forum_response_repo.delete_soft_by_course(),
            survey_response_repo.delete_soft_by_course(),
            quizz_response_repo.delete_soft_by_course(),
            # Navigation
            lesson_block_repo.delete_soft_by_course(),
            lesson_repo.delete_soft_by_course(),
            module_repo.delete_soft_by_course(),
            # Certificates
            certificate_repo.delete_soft_by_course(),
            mdt_certificate_repo.delete_soft_by_course(),
            certificate_template_repo.delete_soft_by_course(),
            # Attendance
            attendance_repo.delete_soft_by_course(),
            course_attendance_repo.delete_soft_by_course(),
            # Enrollments
            enrollment_repo.delete_soft_by_course(),
            # Block Progress
            block_progress_repo.delete_soft_by_course(),
        ]
        for step in cascade_steps:
            step(db, course_id, business_id)

        course_repo.delete_soft_by_id(course_id)


def create_default_blocks(course_id: int, business_id: int):

    return [
        build_lesson_block(
            content=block["content"],
            order=block["order"],
            completion_type=block["completion_type"],
            is_active=block["is_active"],
            course_id=course_id,
            block_type_id=block["type"],
            business_id=business_id,
        )
        for block in constants_default_blocks_mdt.DEFAULT_MDT_BLOCKS
    ]


def build_lesson_block(
    content: dict,
    order: int,
    completion_type: str,
    is_active: bool,
    course_id: int,
    block_type_id: int,
):
    return LessonBlock(
        content=content,
        completion_type=completion_type,
        completion_value=0,
        order=order,
        default=True,
        lesson_id=None,
        block_type_id=block_type_id,
        course_id=course_id,
        date_available=None,
        is_active=is_active,
        deleted=False,
    )


# Viejos
# def create_course(
#   db: Session,
#  data: CourseCreate,
#   image: UploadFile | None = None,
# ):

#   with db.begin():

#      existing = course_repo.get_by_name_and_subcategory(
#         db,
#        data.name,
#       data.subcategory_id,
#  )

# if existing:
#    raise ValueError("El curso ya existe en esta subcategoría")

# image_url = save_course_image(image) if image else None

# course = Course(
#   **data.model_dump(),
#  image_url=image_url,
# )

# course_repo.create(db, course)

# lesson_block_repo.create_all(
#   db,
#  create_default_blocks(course.id),
# )

# return course


# def update_course(
#   db: Session,
#  course_id: int,
# data: CourseUpdate,
# image: UploadFile | None = None,
# ):
#   new_image_url = None
#  if image:
#     new_image_url = save_course_image(image)

# with db.begin():
#   course = course_repo.get_by_id(db, course_id)

#  if not course:
#     raise ValueError("Curso no encontrado")

# update_data = data.model_dump(exclude_unset=True)

# if "name" in update_data and update_data["name"] != course.name:
#   existing = course_repo.get_by_name_and_subcategory(
#      db,
#     update_data["name"],
#    course.subcategory_id,
# )
# if existing:
#   raise ValueError("El curso ya existe en esta subcategoría")

# old_is_mdt = course.is_mdt
# new_is_mdt = update_data.get("is_mdt", old_is_mdt)

# for key, value in update_data.items():
#   setattr(course, key, value)

# if new_image_url:
#   if course.image_url:
#      old_path = course.image_url.lstrip("/")
#     if os.path.exists(old_path):
#        try:
#           os.remove(old_path)
#      except Exception as e:
#         print(f"Error al eliminar imagen antigua: {e}")

# course.image_url = new_image_url

# handle_mdt_blocks_transition(
#   db=db,
#  course=course,
# old_is_mdt=old_is_mdt,
# new_is_mdt=new_is_mdt,
# )

# if old_is_mdt and not new_is_mdt:
#   enrollments = enrollment_repo.get_all_by_course_id(db, course.id)

#  existing_certs = certificate_repo.get_all_by_course(db, course.id)
# users_with_certs = {cert.user_id for cert in existing_certs}

# new_certificates = []
# for enrollment in enrollments:
#   if (
#      enrollment.role_id == 4
#     and enrollment.user_id not in users_with_certs
# ):
#   code = f"CERT-{uuid.uuid4().hex[:10].upper()}"
#  new_certificates.append(
#     Certificate(
#        user_id=enrollment.user_id,
#       course_id=course.id,
#      certificate_code=code,
# )
# )

# if new_certificates:
#   db.add_all(new_certificates)

# return course_repo.update(db, course)


# def delete_course(db: Session, course_id: int):
#   course = course_repo.get_by_id(db, course_id)

#  if not course:
#     raise Exception("Curso no encontrado")

# enrollment_repo.delete_by_course_id(db, course_id)
# return course_repo.delete(db, course)


# def get_course(db: Session, course_id: int):
#   return course_repo.get_by_id(db, course_id)


# def get_courses_by_subcategory(db: Session, subcategory_id: int):
#   return course_repo.get_by_subcategory_id(db, subcategory_id)


# def get_all_courses(db: Session):
#   return course_repo.get_all(db)

'''
def create_default_blocks(course_id: int, business_id: int):

    return [
        build_lesson_block(
            content=block["content"],
            order=block["order"],
            completion_type=block["completion_type"],
            is_active=block["is_active"],
            course_id=course_id,
            block_type_id=block["type"],
            business_id=business_id,
        )
        for block in constants_default_blocks_mdt.DEFAULT_MDT_BLOCKS
    ]


def build_lesson_block(
    content: dict,
    order: int,
    completion_type: str,
    is_active: bool,
    course_id: int,
    block_type_id: int,
):
    return LessonBlock(
        content=content,
        completion_type=completion_type,
        completion_value=0,
        order=order,
        default=True,
        lesson_id=None,
        block_type_id=block_type_id,
        course_id=course_id,
        date_available=None,
        is_active=is_active,
        deleted=False,
    )


def soft_delete_course_cascade(db: Session, course_id: int) -> bool:
    """
    Realiza un borrado lógico (soft delete) de un curso y todas sus
    entidades dependientes en un solo flujo transaccional usando context manager.
    """
    # 1. Subconsultas para identificar los IDs relacionados
    enrollments_subq = select(Enrollment.id).where(Enrollment.course_id == course_id)
    modules_subq = select(Module.id).where(Module.course_id == course_id)
    lessons_subq = select(Lesson.id).where(Lesson.module_id.in_(modules_subq))

    # El context manager db.begin() maneja el commit y rollback automáticamente
    with db.begin():

        # 2. Borrado lógico de Respuestas e Interacciones (Dependientes de Enrollment)
        db.execute(
            update(BlockProgress)
            .where(BlockProgress.enrollment_id.in_(enrollments_subq))
            .values(deleted=True)
        )
        db.execute(
            update(HomeworkResponse)
            .where(HomeworkResponse.enrollment_id.in_(enrollments_subq))
            .values(deleted=True)
        )
        db.execute(
            update(SurveyResponse)
            .where(SurveyResponse.enrollment_id.in_(enrollments_subq))
            .values(deleted=True)
        )
        db.execute(
            update(QuizzResponse)
            .where(QuizzResponse.enrollment_id.in_(enrollments_subq))
            .values(deleted=True)
        )
        db.execute(
            update(ForumResponse)
            .where(ForumResponse.enrollment_id.in_(enrollments_subq))
            .values(deleted=True)
        )

        # 3. Borrado lógico de Enrollments
        db.execute(
            update(Enrollment)
            .where(Enrollment.course_id == course_id)
            .values(deleted=True)
        )

        # 4. Borrado lógico del Contenido del Curso (LessonBlocks, Lessons, Modules)
        db.execute(
            update(LessonBlock)
            .where(
                (LessonBlock.lesson_id.in_(lessons_subq))
                | (LessonBlock.course_id == course_id)
            )
            .values(deleted=True)
        )

        db.execute(
            update(Lesson)
            .where(Lesson.module_id.in_(modules_subq))
            .values(deleted=True)
        )

        db.execute(
            update(Module).where(Module.course_id == course_id).values(deleted=True)
        )

        # 5. Borrado lógico de otros adjuntos del curso
        db.execute(
            update(CourseAttendance)
            .where(CourseAttendance.course_id == course_id)
            .values(deleted=True)
        )
        db.execute(
            update(CertificateTemplate)
            .where(CertificateTemplate.course_id == course_id)
            .values(deleted=True)
        )
        db.execute(
            update(Certificate)
            .where(Certificate.course_id == course_id)
            .values(deleted=True)
        )
        db.execute(
            update(MdtCertificate)
            .where(MdtCertificate.course_id == course_id)
            .values(deleted=True)
        )

        # 6. Borrado lógico del Curso Padre
        db.execute(update(Course).where(Course.id == course_id).values(deleted=True))

    # Si llegamos aquí, el commit ya se realizó con éxito
    return True
'''
