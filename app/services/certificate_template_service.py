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
    print("\n========== CREATE TEMPLATE ==========")

    existing = certificate_template_repo.get_by_course(db, data.course_id)
    if existing:
        raise Exception("Plantilla existente en el curso")

    form = await request.form()
    print("📦 FORM KEYS:", list(form.keys()))

    image_url = None
    if background_image and isinstance(background_image, UploadFile):
        image_url = save_certificate_template_image(background_image)

    print("📄 DATA FIELDS:", data.fields)

    processed_fields = []

    for field in data.fields or []:
        field_dict = dict(field)  # safe copy
        field_id = field_dict.get("id")

        print("\n-----------------------------")
        print("🧩 FIELD RAW:", field_dict)

        file_key = f"signature_{field_id}"
        file = form.get(file_key)

        print(f"🔑 Looking for: {file_key}")
        print(f"📎 File found: {file}")

        if isinstance(file, UploadFile) and file.filename:
            field_dict["signatureImage"] = save_certificate_template_image(file)
            print("✅ IMAGE SAVED")
        else:
            field_dict["signatureImage"] = None
            print("❌ No file for:", file_key)

        processed_fields.append(field_dict)

    print("\n========== FINAL PROCESSED FIELDS ==========")
    print(processed_fields)

    template = CertificateTemplate(
        course_id=data.course_id,
        background_image_url=image_url,
        fields=processed_fields,
        qr_config=data.qr_config
    )

    return certificate_template_repo.create(db, template)

import json

async def update_certificate_template(
    db: Session,
    template_id: int,
    data: str = Form(...),
    background_image: Optional[UploadFile] = None,
    request: Request = None
):
    print("\n========== UPDATE TEMPLATE ==========")

    template = certificate_template_repo.get_by_id(db, template_id)
    if not template:
        raise Exception("Plantilla no encontrada")

    form = await request.form()
    print("📦 FORM KEYS:", list(form.keys()))

    payload = json.loads(data)
    print("📄 UPDATE PAYLOAD:", payload)

    # 🔥 background image
    if background_image and isinstance(background_image, UploadFile):
        template.background_image_url = save_certificate_template_image(background_image)
        print("🖼️ NEW BACKGROUND IMAGE SAVED")
    else:
        print("🖼️ KEEP OLD BACKGROUND")

    existing_fields = template.fields or []
    updated_fields = []

    for field in payload.get("fields", existing_fields):

        field_dict = dict(field)
        field_id = field_dict.get("id")

        print("\n-----------------------------")
        print("🧩 FIELD RAW:", field_dict)

        file_key = f"signature_{field_id}"
        file = form.get(file_key)

        print(f"🔑 Looking for: {file_key}")
        print(f"📎 File found: {file}")

        if isinstance(file, UploadFile) and file.filename:
            field_dict["signatureImage"] = save_certificate_template_image(file)
            print("🆕 NEW IMAGE SAVED")
        else:
            # 👇 importante: mantener existente
            field_dict["signatureImage"] = field_dict.get("signatureImage")
            print("♻️ KEEP OLD IMAGE")

        updated_fields.append(field_dict)

    print("\n========== FINAL UPDATED FIELDS ==========")
    print(updated_fields)

    template.fields = updated_fields
    template.qr_config = payload.get("qr_config", template.qr_config)

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