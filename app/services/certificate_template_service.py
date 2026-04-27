from sqlalchemy.orm import Session
from app.models.certificate_template import CertificateTemplate
from app.repositories import certificate_template_repo
from app.schemas.certificate_template import (
    CertificateTemplateCreate,
    CertificateTemplateUpdate
)
from fastapi import UploadFile, Request
from typing import Optional
from app.utils.file_upload import save_certificate_template_image

async def create_certificate_template(
    db: Session,
    data: CertificateTemplateCreate,
    background_image: Optional[UploadFile] = None,
    request: Request = None
):
    existing = certificate_template_repo.get_by_course(db, data.course_id)
    if existing:
        raise Exception("Plantilla existente en el curso")

    form = await request.form()

    # 🔹 background image
    image_url = None
    if isinstance(background_image, UploadFile):
        image_url = save_certificate_template_image(background_image)

    processed_fields = []

    for field in data.fields:
        field_dict = field.copy()
        field_id = field_dict.get("id")

        file_key = f"signature_{field_id}"
        file = form.get(file_key)

        # 🔥 solo si realmente llegó archivo
        if isinstance(file, UploadFile) and file.filename:
            field_dict["signatureImage"] = save_certificate_template_image(file)
        else:
            field_dict["signatureImage"] = None

        processed_fields.append(field_dict)

    template = CertificateTemplate(
        course_id=data.course_id,
        background_image_url=image_url,
        fields=processed_fields,
        qr_config=data.qr_config
    )

    return certificate_template_repo.create(db, template)


dasync def update_certificate_template(
    db: Session,
    template_id: int,
    data: CertificateTemplateUpdate,
    background_image: Optional[UploadFile] = None,
    request: Request = None
):
    template = certificate_template_repo.get_by_id(db, template_id)
    if not template:
        raise Exception("Plantilla no encontrada")

    form = await request.form()

    # 🔹 background image
    if isinstance(background_image, UploadFile):
        template.background_image_url = save_certificate_template_image(background_image)

    updated_fields = []

    for field in data.fields:
        field_dict = field.copy()
        field_id = field_dict.get("id")

        file_key = f"signature_{field_id}"
        file = form.get(file_key)

        # 🔥 actualizar solo si llega archivo nuevo
        if isinstance(file, UploadFile) and file.filename:
            field_dict["signatureImage"] = save_certificate_template_image(file)
        else:
            # mantener lo existente si no se envía nuevo archivo
            field_dict["signatureImage"] = field_dict.get("signatureImage")

        updated_fields.append(field_dict)

    template.fields = updated_fields
    template.qr_config = data.qr_config

    return certificate_template_repo.update(db, template)


def delete_certificate_template(db: Session, certificate_template_id: int):
    template = certificate_template_repo.get_by_id(db, certificate_template_id)

    if not template:
        raise Exception("Plantilla no encontrada")

    return certificate_template_repo.delete(db, template)


def get_certificate_template(db: Session, certificate_template_id: int):
    template = certificate_template_repo.get_by_id(db, certificate_template_id)

    if not template:
        raise Exception("Plantilla no encontrada")

    return template


def get_all_certificate_templates(db: Session):
    return certificate_template_repo.get_all(db)


def get_certificate_template_by_course(db: Session, course_id: int):
    return certificate_template_repo.get_by_course(db, course_id)