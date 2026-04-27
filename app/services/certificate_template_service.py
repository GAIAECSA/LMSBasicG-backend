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
    print("\n\n========== CREATE TEMPLATE ==========")

    existing = certificate_template_repo.get_by_course(db, data.course_id)
    if existing:
        raise Exception("Plantilla existente en el curso")

    form = await request.form()

    print("📦 FORM KEYS:", list(form.keys()))
    print("📄 DATA FIELDS:", data.fields)

    # 🔹 background image
    image_url = None
    if isinstance(background_image, UploadFile):
        print("🖼️ Background image:", background_image.filename)
        image_url = save_certificate_template_image(background_image)
    else:
        print("🖼️ No background image")

    processed_fields = []

    for field in data.fields:
        print("\n-----------------------------")
        print("🧩 FIELD RAW:", field)

        field_dict = field.copy()
        field_id = field_dict.get("id")

        file_key = f"signature_{field_id}"
        print("🔑 Looking for:", file_key)

        file = form.get(file_key)
        print("📎 File found:", file)

        if isinstance(file, UploadFile) and file.filename:
            print("✅ Saving file...")
            url = save_certificate_template_image(file)
            field_dict["signatureImage"] = url
            print("💾 URL:", url)
        else:
            print("❌ No file for:", file_key)
            field_dict["signatureImage"] = None

        processed_fields.append(field_dict)

    print("\n========== FINAL PROCESSED FIELDS ==========")
    print(processed_fields)

    template = CertificateTemplate(
        course_id=data.course_id,
        background_image_url=image_url,
        fields=processed_fields,
        qr_config=data.qr_config
    )

    result = certificate_template_repo.create(db, template)

    print("🎉 TEMPLATE CREATED")

    return result


async def update_certificate_template(
    db: Session,
    template_id: int,
    data: CertificateTemplateUpdate,
    background_image: Optional[UploadFile] = None,
    request: Request = None
):
    print("\n\n========== UPDATE TEMPLATE ==========")

    template = certificate_template_repo.get_by_id(db, template_id)
    if not template:
        raise Exception("Plantilla no encontrada")

    form = await request.form()

    print("📦 FORM KEYS:", list(form.keys()))
    print("📄 EXISTING FIELDS:", template.fields)
    print("📄 UPDATE DATA FIELDS:", data.fields)

    # 🔹 background image
    if isinstance(background_image, UploadFile):
        print("🖼️ New background image:", background_image.filename)
        template.background_image_url = save_certificate_template_image(background_image)

    updated_fields = []

    # 🔥 IMPORTANTE: usamos fields existentes si data.fields no viene completo
    base_fields = data.fields if data.fields else template.fields

    for field in base_fields:
        print("\n-----------------------------")
        print("🧩 FIELD:", field)

        field_dict = field.copy()
        field_id = field_dict.get("id")

        file_key = f"signature_{field_id}"
        print("🔑 Looking for:", file_key)

        file = form.get(file_key)
        print("📎 File found:", file)

        if isinstance(file, UploadFile) and file.filename:
            print("✅ Updating file...")
            url = save_certificate_template_image(file)
            field_dict["signatureImage"] = url
            print("💾 New URL:", url)
        else:
            print("⏭️ Keeping existing signatureImage")
            field_dict["signatureImage"] = field_dict.get("signatureImage")

        updated_fields.append(field_dict)

    print("\n========== FINAL UPDATED FIELDS ==========")
    print(updated_fields)

    template.fields = updated_fields

    if data.qr_config:
        template.qr_config = data.qr_config

    result = certificate_template_repo.update(db, template)

    print("🎉 TEMPLATE UPDATED")

    return result


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