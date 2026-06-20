import os
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.constants import (constants_attendance_state, constants_enrollments,
                           constants_roles)
from app.core.security import hash_password
from app.helpers import blind_index
from app.models.attendance import Attendance
from app.models.block_progress import BlockProgress
from app.models.certificate import Certificate
from app.models.enrollment import Enrollment
from app.models.user import User
from app.repositories import (attendance_repo, block_progress_repo,
                              certificate_repo, course_attendance_repo,
                              course_repo, enrollment_repo,
                              forum_response_repo, homework_response_repo,
                              lesson_block_repo, quizz_response_repo,
                              survey_response_repo, user_repo)
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate
from app.schemas.user import UserCreate
from app.services import course_service
from app.utils.file_upload import save_course_voucher

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class EnrollmentPendingError(Exception):
    pass


class EnrollmentAcceptedError(Exception):
    pass


class EnrollmentDeniedError(Exception):
    pass


class EnrollmentNotFoundError(Exception):
    pass


class EnrollmentAlreadyExistsError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def create_enrollment(
    db: Session,
    data: EnrollmentCreate,
    business_id: int,
    image: UploadFile | None = None,
):

    with db.begin():

        existing = enrollment_repo.get_existing_enrollment(
            db, data.course_id, data.user_id, business_id
        )

        if existing:
            if existing.accepted is constants_enrollments.ENROLLMENT_PENDING:
                raise EnrollmentPendingError("Matrícula en revisión")
            elif existing.accepted is constants_enrollments.ENROLLMENT_ACCEPTED:
                raise EnrollmentAcceptedError("Ya estás matriculado en este curso")
            elif existing.accepted is constants_enrollments.ENROLLMENT_DENIED:
                raise EnrollmentDeniedError(
                    "Tu solicitud de matrícula no fue aprobada."
                )

        course = course_repo.get_by_id(db, data.course_id, business_id)
        if not course:
            raise course_service.CourseNotFoundError("Curso no encontrado")

        # Enroll
        voucher_url = save_course_voucher(image, business_id) if image else None
        enrollment = Enrollment(
            **data.model_dump(), voucher_url=voucher_url, business_id=business_id
        )
        enrollment_repo.create(enrollment)
        # Certificado
        code = f"CERT-{uuid.uuid4().hex[:10].upper()}"
        certificate_repo.create(
            db,
            Certificate(
                user_id=data.user_id,
                course_id=data.course_id,
                certificate_code=code,
                business_id=business_id,
            ),
        )
        # Asistencias
        course_attendances = course_attendance_repo.get_by_course(
            db, data.course_id, business_id
        )
        if course_attendances:
            attendances = [
                Attendance(
                    enrollment_id=enrollment.id,
                    course_attendance_id=ca.id,
                    attendance_state=constants_attendance_state.ATTENDANCE_STATE_PENDING,
                    business_id=business_id,
                )
                for ca in course_attendances
            ]
            attendance_repo.create_bulk(db, attendances)
        # Progreso Bloques
        lessons_blocks = lesson_block_repo.get_no_default_by_course_id(
            db, data.course_id, business_id
        )
        if lessons_blocks:
            lessons_progress = [
                BlockProgress(
                    enrollment_id=enrollment.id,
                    lesson_block_id=lb.id,
                    business_id=business_id,
                    is_completed=False,
                )
                for lb in lessons_blocks
            ]
            block_progress_repo.create_bulk(db, lessons_progress)
        return enrollment


def update_enrollment(
    db: Session,
    enrollment_id: int,
    data: EnrollmentUpdate,
    business_id: int,
    image: UploadFile | None = None,
):
    with db.begin():
        enrollment = enrollment_repo.get_by_id(db, enrollment_id, business_id)

        if not enrollment:
            raise EnrollmentNotFoundError("Inscripción no encontrada")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(enrollment, key, value)

        if image:
            new_voucher_url = save_course_voucher(image, business_id)

            if enrollment.voucher_url:
                old_path = enrollment.voucher_url.lstrip("/")

                try:
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except OSError:
                    pass

            enrollment.voucher_url = new_voucher_url

        return enrollment


def get_enrollment(db: Session, enrollment_id: int, business_id: int):
    enrollment = enrollment_repo.get_by_id(db, enrollment_id, business_id)
    if not enrollment:
        raise EnrollmentNotFoundError("Inscripción no encontrada")
    return enrollment


def get_enrollments_by_course_and_role(
    db: Session, course_id: int, role_id: int, business_id: int
):
    return enrollment_repo.get_all_by_course_and_role(
        db, course_id, role_id, business_id
    )


def get_enrollments_by_user(db: Session, user_id: int, business_id: int):
    return enrollment_repo.get_all_by_user(db, user_id, business_id)


def get_enrollments_by_role(db: Session, role_id: int, business_id: int):
    return enrollment_repo.get_all_by_role(db, role_id, business_id)


def get_enrollment_by_user_and_course(
    db: Session, user_id: int, course_id: int, business_id: int
):
    enrollment = enrollment_repo.get_existing_enrollment(
        db, course_id, user_id, business_id
    )
    if not enrollment:
        raise EnrollmentNotFoundError("Inscripción no encontrada")
    return enrollment


def delete_enrollment(db: Session, enrollment_id: int, business_id: int):
    with db.begin():
        enrollment = enrollment_repo.get_by_id(db, enrollment_id, business_id)
        if not enrollment:
            raise EnrollmentNotFoundError("Inscripción no encontrada")
        cascade_steps = [
            # Blocks
            homework_response_repo.delete_soft_by_enrollment(),
            forum_response_repo.delete_soft_by_enrollment(),
            survey_response_repo.delete_soft_by_enrollment(),
            quizz_response_repo.delete_soft_by_enrollment(),
            # Attendance
            attendance_repo.delete_soft_by_enrollment(),
            # Progress
            block_progress_repo.delete_soft_by_enrollment(),
        ]
        for step in cascade_steps:
            step(db, enrollment_id, business_id)

        enrollment_repo.delete_soft_by_id(enrollment_id)


def create_massive_enrollments(
    db: Session,
    users: list[UserCreate],
    course_id: int,
    business_id: int,
):
    created = []
    skipped = []
    failed = []

    with db.begin():

        course = course_repo.get_by_id(db, course_id, business_id)

        if not course:
            raise course_service.CourseNotFoundError("Curso no encontrado")

        course_attendances = course_attendance_repo.get_by_course(
            db, course_id, business_id
        )

        lessons_blocks = lesson_block_repo.get_no_default_by_course_id(
            db, course_id, business_id
        )

        for user_data in users:
            try:
                with db.begin_nested():

                    current_idnumber_hash = (
                        blind_index.generate_blind_index(user_data.idnumber)
                        if user_data.idnumber
                        else None
                    )

                    existing_user = user_repo.get_by_email_or_idnumber_hash_or_username(
                        db,
                        user_data.email,
                        current_idnumber_hash,
                        user_data.username,
                        business_id,
                    )
                    # Crea porque no existe usuario
                    if not existing_user:
                        user_dict = user_data.model_dump(
                            exclude={"password", "role_id"}
                        )

                        current_phone_hash = (
                            blind_index.generate_blind_index(user_data.phone_number)
                            if user_data.phone_number
                            else None
                        )

                        existing_user = user_repo.create(
                            db,
                            User(
                                **user_dict,
                                idnumber_hash=current_idnumber_hash,
                                phone_number_hash=current_phone_hash,
                                password=hash_password(user_data.password),
                                role_id=constants_roles.VISITOR_ROLE,
                                business_id=business_id,
                            ),
                        )

                    existing_enrollment = enrollment_repo.get_existing_enrollment(
                        db,
                        course_id,
                        existing_user.id,
                        business_id,
                    )

                    if existing_enrollment:

                        if (
                            existing_enrollment.accepted
                            is constants_enrollments.ENROLLMENT_PENDING
                        ):
                            raise EnrollmentPendingError("Matrícula en revisión")

                        elif (
                            existing_enrollment.accepted
                            is constants_enrollments.ENROLLMENT_ACCEPTED
                        ):
                            raise EnrollmentAcceptedError(
                                "Ya estás matriculado en este curso"
                            )

                        elif (
                            existing_enrollment.accepted
                            is constants_enrollments.ENROLLMENT_DENIED
                        ):
                            raise EnrollmentDeniedError(
                                "Tu solicitud de matrícula no fue aprobada."
                            )

                    enrollment = enrollment_repo.create(
                        db,
                        Enrollment(
                            accepted=constants_enrollments.ENROLLMENT_ACCEPTED,
                            user_id=existing_user.id,
                            course_id=course_id,
                            role_id=constants_roles.STUDENT_ROLE,
                            business_id=business_id,
                        ),
                    )

                    code = f"CERT-{uuid.uuid4().hex[:10].upper()}"

                    certificate_repo.create(
                        db,
                        Certificate(
                            user_id=existing_user.id,
                            course_id=course_id,
                            certificate_code=code,
                            business_id=business_id,
                        ),
                    )

                    if course_attendances:
                        attendances = [
                            Attendance(
                                enrollment_id=enrollment.id,
                                course_attendance_id=ca.id,
                                attendance_state=constants_attendance_state.ATTENDANCE_STATE_PENDING,
                                business_id=business_id,
                            )
                            for ca in course_attendances
                        ]

                        attendance_repo.create_bulk(
                            db,
                            attendances,
                        )

                    if lessons_blocks:
                        lessons_progress = [
                            BlockProgress(
                                enrollment_id=enrollment.id,
                                lesson_block_id=lb.id,
                                business_id=business_id,
                                is_completed=False,
                            )
                            for lb in lessons_blocks
                        ]

                        block_progress_repo.create_bulk(
                            db,
                            lessons_progress,
                        )

                    created.append(
                        {
                            "email": user_data.email,
                            "user_id": existing_user.id,
                            "enrollment_id": enrollment.id,
                        }
                    )

            except (
                EnrollmentPendingError,
                EnrollmentAcceptedError,
                EnrollmentDeniedError,
            ) as e:

                skipped.append(
                    {
                        "email": user_data.email,
                        "reason": str(e),
                    }
                )

            except Exception as e:

                failed.append(
                    {
                        "email": user_data.email,
                        "error": str(e),
                    }
                )

    return {
        "created": created,
        "skipped": skipped,
        "failed": failed,
        "summary": {
            "created": len(created),
            "skipped": len(skipped),
            "failed": len(failed),
            "total": len(users),
        },
    }


"""
def create_enrollment(
    db: Session, data: EnrollmentCreate, image: UploadFile | None = None
):

    with db.begin():

        existing = enrollment_repo.get_existing_enrollment(
            db, data.course_id, data.user_id
        )

        if existing:
            if existing.accepted is None:
                raise Exception("Matrícula en revisión")
            elif existing.accepted is True:
                raise Exception("Ya estás matriculado en este curso")
            elif existing.accepted is False:
                raise Exception("Tu solicitud de matrícula no fue aprobada.")

        voucher_url = save_course_voucher(image) if image else None

        enrollment = Enrollment(**data.model_dump(), voucher_url=voucher_url)
        enrollment = enrollment_repo.create_flush(db, enrollment)

        role = enrollment.role
        course = course_repo.get_by_id(db, data.course_id)
        if not course:
            raise Exception("Curso no encontrado")
        code = f"CERT-{uuid.uuid4().hex[:10].upper()}"
        certificate_repo.create(
            db,
            Certificate(
                user_id=data.user_id,
                course_id=data.course_id,
                certificate_code=code,
            ),
        )

        course_attendances = course_attendance_repo.get_by_course(db, data.course_id)

        if course_attendances:
            attendances = [
                Attendance(
                    enrollment_id=enrollment.id,
                    course_attendance_id=ca.id,
                    attendance_state="PENDIENTE",
                )
                for ca in course_attendances
            ]

            attendance_repo.create_many(db, attendances)

        return enrollment


def update_enrollment(
    db: Session,
    enrollment_id: int,
    data: EnrollmentUpdate,
    image: UploadFile | None = None,
):
    enrollment = enrollment_repo.get_by_id(db, enrollment_id)
    if not enrollment:
        raise Exception("Inscripción no encontrada")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(enrollment, key, value)

    if image:
        if enrollment.voucher_url:
            old_path = enrollment.voucher_url.lstrip("/")
            if os.path.exists(old_path):
                os.remove(old_path)

        enrollment.voucher_url = save_course_voucher(image)

    return enrollment_repo.update(db, enrollment)


def delete_enrollment(db: Session, enrollment_id: int):
    enrollment = enrollment_repo.get_by_id(db, enrollment_id)
    if not enrollment:
        raise Exception("Inscripción no encontrada")

    return enrollment_repo.delete(db, enrollment)


def get_enrollment(db: Session, enrollment_id: int):
    enrollment = enrollment_repo.get_by_id(db, enrollment_id)
    if not enrollment:
        raise Exception("Inscripción no encontrada")
    return enrollment


def get_enrollments_by_course_and_role(db: Session, course_id: int, role_id: int):
    return enrollment_repo.get_all_by_course_id_and_role_id(db, course_id, role_id)


def get_enrollments_by_user(db: Session, user_id: int):
    return enrollment_repo.get_all_by_user(db, user_id)


def get_enrollments_by_role(db: Session, role_id: int):
    return enrollment_repo.get_all_by_role(db, role_id)


def get_enrollment_by_user_and_course(db: Session, user_id: int, course_id: int):
    enrollment = enrollment_repo.get_existing_enrollment(db, course_id, user_id)
    if not enrollment:
        raise Exception("Inscripción no encontrada")
    return enrollment


def create_massive_enrollments(
    db: Session,
    users: list[UserCreate],
    course_id: int,
):
    created = []
    skipped = []
    failed = []

    with db.begin():
        course_attendances = course_attendance_repo.get_by_course(db, course_id)
        course = course_repo.get_by_id(db, course_id)

        if not course:
            raise Exception("Curso no encontrado")

        for user_data in users:
            try:
                with db.begin_nested():
                    # 1. Generar el hash de la cédula para poder buscar al usuario
                    current_idnumber_hash = (
                        blind_index.generate_blind_index(user_data.idnumber)
                        if user_data.idnumber
                        else None
                    )

                    # 2. Buscar usando el hash (NO el texto plano)
                    existing_user = user_repo.get_by_email_or_idnumber_hash_or_username(
                        db,
                        user_data.email,
                        current_idnumber_hash,
                        user_data.username
                    )

                    if not existing_user:
                        # 3. Extraer datos excluyendo password y rol para inyectarlos de forma segura
                        user_dict = user_data.model_dump(
                            exclude={"password", "role_id"}
                        )

                        # Generar el hash del teléfono
                        current_phone_hash = (
                            blind_index.generate_blind_index(user_data.phone_number)
                            if user_data.phone_number
                            else None
                        )

                        # 4. Crear el usuario inyectando los hashes y la contraseña cifrada
                        user_model = User(
                            **user_dict,
                            idnumber_hash=current_idnumber_hash,
                            phone_number_hash=current_phone_hash,
                            password=hash_password(user_data.password),
                            role_id=2,
                        )

                        existing_user = user_repo.create_flush(
                            db,
                            user_model,
                        )

                    existing_enrollment = enrollment_repo.get_existing_enrollment(
                        db,
                        course_id,
                        existing_user.id,
                    )

                    if existing_enrollment:
                        skipped.append(
                            {
                                "email": user_data.email,
                                "reason": "El usuario ya está matriculado",
                            }
                        )
                        continue

                    enrollment = enrollment_repo.create_flush(
                        db,
                        Enrollment(
                            accepted=True,
                            user_id=existing_user.id,
                            course_id=course_id,
                            role_id=4,
                        ),
                    )

                    if course_attendances:
                        attendances = [
                            Attendance(
                                enrollment_id=enrollment.id,
                                course_attendance_id=ca.id,
                                attendance_state="PENDIENTE",
                            )
                            for ca in course_attendances
                        ]

                        attendance_repo.create_many(
                            db,
                            attendances,
                        )

                    if enrollment.role_id == 4 and not course.is_mdt:
                        code = f"CERT-{uuid.uuid4().hex[:10].upper()}"

                        certificate_repo.create(
                            db,
                            Certificate(
                                user_id=existing_user.id,
                                course_id=course_id,
                                certificate_code=code,
                            ),
                        )

                    created.append(
                        {
                            "email": user_data.email,
                            "enrollment_id": enrollment.id,
                            "user_id": existing_user.id,
                        }
                    )

            except Exception as e:
                failed.append(
                    {
                        "email": user_data.email,
                        "error": str(e),
                    }
                )

    return {
        "created": created,
        "skipped": skipped,
        "failed": failed,
        "summary": {
            "created": len(created),
            "skipped": len(skipped),
            "failed": len(failed),
            "total": len(users),
        },
    }
"""
