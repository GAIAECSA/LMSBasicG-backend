from sqlalchemy.orm import Session
from app.models.certificate_template import CertificateTemplate
from app.repositories import certificate_template_repo
from app.schemas.certificate_template import (
    CertificateTemplateCreate,
    CertificateTemplateUpdate
)
from fastapi import UploadFile, Request, Form
from typing import Optional
from app.utils.file_upload import save_certificate_template_image

async def create_certificate_template(
    db: Session,
    data: dict,
    background_image: UploadFile = None,
    request: Request = None
):
    print("\n========== CREATE TEMPLATE ==========")

    existing = certificate_template_repo.get_by_course(db, data["course_id"])
    if existing:
        raise Exception("Plantilla existente en el curso")

    form = await request.form()
    print("📦 FORM KEYS:", list(form.keys()))

    image_url = None
    if background_image:
        image_url = save_certificate_template_image(background_image)

    processed_fields = []

    for field in data.get("fields", []):
        field = dict(field)
        field_id = field.get("id")

        print("\n🧩 FIELD:", field)

        file_key = f"signature_{field_id}"
        file = form.get(file_key)

        print(f"🔑 file_key: {file_key} -> {file}")

        if isinstance(file, UploadFile) and file.filename:
            field["signatureImage"] = save_certificate_template_image(file)
            print("🆕 IMAGE SAVED")
        else:
            field["signatureImage"] = None
            print("❌ NO IMAGE")

        processed_fields.append(field)

    template = CertificateTemplate(
        course_id=data["course_id"],
        background_image_url=image_url,
        fields=processed_fields,
        qr_config=data.get("qr_config")
    )

    return certificate_template_repo.create(db, template)


async def update_certificate_template(
    db: Session,
    template_id: int,
    data: dict,
    background_image: UploadFile = None,
    request: Request = None
):
    print("\n========== UPDATE TEMPLATE ==========")

    template = certificate_template_repo.get_by_id(db, template_id)
    if not template:
        raise Exception("Plantilla no encontrada")

    form = await request.form()
    print("📦 FORM KEYS:", list(form.keys()))

    if background_image:
        template.background_image_url = save_certificate_template_image(background_image)

    existing_fields = template.fields or []
    incoming_fields = data.get("fields", existing_fields)

    updated_fields = []

    for field in incoming_fields:
        field = dict(field)
        field_id = field.get("id")

        print("\n🧩 FIELD:", field)

        file_key = f"signature_{field_id}"
        file = form.get(file_key)

        print(f"🔑 file_key: {file_key} -> {file}")

        if isinstance(file, UploadFile) and file.filename:
            field["signatureImage"] = save_certificate_template_image(file)
            print("🆕 NEW IMAGE")
        else:
            # 🔥 CRÍTICO: mantener imagen anterior del DB
            old = next((f for f in existing_fields if f.get("id") == field_id), {})
            field["signatureImage"] = old.get("signatureImage")
            print("♻️ KEEP OLD IMAGE")

        updated_fields.append(field)

    template.fields = updated_fields
    template.qr_config = data.get("qr_config", template.qr_config)

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