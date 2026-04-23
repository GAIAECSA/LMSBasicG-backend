import os
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_DIR_IMAGE_COURSE = "uploads/courses"
UPLOAD_DIR_IMAGE_COURSE_VOUCHER = "uploads/course_vouchers"


def save_course_image(file: UploadFile) -> str | None:
    if not file:
        return None

    if not file.content_type.startswith("image/"):
        raise ValueError("El archivo debe ser una imagen")

    os.makedirs(UPLOAD_DIR_IMAGE_COURSE, exist_ok=True)

    extension = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(UPLOAD_DIR_IMAGE_COURSE, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return f"/{filepath}"

def save_course_voucher(file: UploadFile) -> str | None:
    if not file:
        return None

    if not file.content_type.startswith("image/"):
        raise ValueError("El archivo debe ser una imagen")

    os.makedirs(UPLOAD_DIR_IMAGE_COURSE_VOUCHER, exist_ok=True)

    extension = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(UPLOAD_DIR_IMAGE_COURSE_VOUCHER, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return f"/{filepath}"