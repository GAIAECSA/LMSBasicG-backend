import os
from uuid import uuid4

from fastapi import UploadFile

UPLOAD_DIR_IMAGE_COURSE = "uploads/courses"
UPLOAD_DIR_IMAGE_COURSE_VOUCHER = "uploads/course_vouchers"
UPLOAD_DIR_LESSON_BLOCK_FILE = "uploads/lesson_blocks"
UPLOAD_DIR_CERTIFICATE_TEMPLATES = "uploads/certificate_templates"
UPLOAD_DIR_CERTIFICATES = "uploads/certificates"
UPLOAD_DIR_HOMEWORK_RESPONSES = "uploads/homework_responses"
UPLOAD_DIR_POLICY_PRIVACY = "uploads/policy_privacy"
UPLOAD_DIR_CERTIFICATE_MDT = "uploads/certificate_mdt"

# =====================================================================
# Helpers
# =====================================================================


def save_course_image(
    file: UploadFile,
    business_id: int,
) -> str | None:
    if not file:
        return None

    if not file.content_type or not file.content_type.startswith("image/"):
        raise ValueError("El archivo debe ser una imagen")

    business_dir = os.path.join(
        UPLOAD_DIR_IMAGE_COURSE,
        f"business_{business_id}",
    )
    os.makedirs(business_dir, exist_ok=True)

    extension = (
        file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "jpg"
    )

    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(business_dir, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return "/" + filepath.replace(os.sep, "/")


def save_course_voucher(
    file: UploadFile,
    business_id: int,
) -> str | None:
    if not file:
        return None

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "application/pdf",
    }

    if file.content_type not in allowed_types:
        raise ValueError("Solo se permiten imágenes o PDF")

    business_dir = os.path.join(
        UPLOAD_DIR_IMAGE_COURSE_VOUCHER,
        f"business_{business_id}",
    )

    os.makedirs(business_dir, exist_ok=True)

    extension = (
        file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "bin"
    )

    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(business_dir, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return "/" + filepath.replace(os.sep, "/")


def save_certificate_template_image(
    file: UploadFile,
    business_id: int,
) -> str | None:
    if not file:
        return None

    if not file.content_type.startswith("image/"):
        raise ValueError("El archivo debe ser una imagen")

    business_dir = os.path.join(
        UPLOAD_DIR_IMAGE_COURSE,
        f"business_{business_id}",
    )

    os.makedirs(
        business_dir,
        exist_ok=True,
    )

    extension = (
        file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "bin"
    )

    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(
        business_dir,
        filename,
    )

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return "/" + filepath.replace(os.sep, "/")


def save_certificate(
    file: UploadFile,
    business_id: int,
) -> str | None:
    if not file:
        return None

    if file.content_type != "application/pdf":
        raise ValueError("El archivo debe ser un PDF")

    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("El archivo debe tener extensión .pdf")

    business_dir = os.path.join(
        UPLOAD_DIR_CERTIFICATES,
        f"business_{business_id}",
    )

    os.makedirs(
        business_dir,
        exist_ok=True,
    )

    filename = f"{uuid4()}.pdf"

    filepath = os.path.join(
        business_dir,
        filename,
    )

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return "/" + filepath.replace(
        os.sep,
        "/",
    )


def save_lesson_file(file: UploadFile, business_id: int) -> dict | None:
    if not file:
        return None

    allowed_types = ["image/jpeg", "image/png", "image/webp", "application/pdf"]

    if file.content_type not in allowed_types:
        raise ValueError("Solo se permiten imágenes o PDF")

    # Crear directorio con base en el business_id
    business_dir = os.path.join(
        UPLOAD_DIR_LESSON_BLOCK_FILE,
        f"business_{business_id}",
    )
    os.makedirs(business_dir, exist_ok=True)

    extension = file.filename.split(".")[-1].lower()
    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(business_dir, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "file_url": "/" + filepath.replace(os.sep, "/"),
        "filename": file.filename,
        "stored_name": filename,
    }


def save_homework_file(file: UploadFile, business_id: int) -> dict | None:
    if not file:
        return None

    allowed_types = [
        "application/pdf",
        "application/zip",
        "application/x-zip-compressed",
    ]

    if file.content_type not in allowed_types:
        raise ValueError("Solo se permiten archivos PDF o ZIP")

    extension = file.filename.split(".")[-1].lower()
    allowed_extensions = ["pdf", "zip"]

    if extension not in allowed_extensions:
        raise ValueError("Extensión de archivo no permitida")

    # Crear directorio con base en el business_id
    business_dir = os.path.join(
        UPLOAD_DIR_HOMEWORK_RESPONSES,
        f"business_{business_id}",
    )
    os.makedirs(business_dir, exist_ok=True)

    filename = f"{uuid4()}.{extension}"
    filepath = os.path.join(business_dir, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "file_url": "/" + filepath.replace(os.sep, "/"),
        "filename": file.filename,
        "stored_name": filename,
    }


def save_policy_privacy_file(file: UploadFile, business_id: int) -> dict | None:
    if not file:
        return None

    if file.content_type != "application/pdf":
        raise ValueError("Solo se permite PDF")

    extension = file.filename.split(".")[-1].lower()
    if extension != "pdf":
        raise ValueError("El archivo debe tener extensión .pdf")

    # Crear directorio con base en el business_id
    business_dir = os.path.join(
        UPLOAD_DIR_POLICY_PRIVACY,
        f"business_{business_id}",
    )
    os.makedirs(business_dir, exist_ok=True)

    filename = f"{uuid4()}.pdf"
    filepath = os.path.join(business_dir, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "file_url": "/" + filepath.replace(os.sep, "/"),
        "filename": file.filename,
        "stored_name": filename,
    }


def save_certificate_mdt(file: UploadFile, business_id: int) -> dict | None:
    if not file:
        return None

    if file.content_type != "application/pdf":
        raise ValueError("Solo se permite PDF")

    extension = file.filename.split(".")[-1].lower()
    if extension != "pdf":
        raise ValueError("El archivo debe tener extensión .pdf")

    # Crear directorio con base en el business_id
    business_dir = os.path.join(
        UPLOAD_DIR_CERTIFICATE_MDT,
        f"business_{business_id}",
    )
    os.makedirs(business_dir, exist_ok=True)

    filename = f"{uuid4()}.pdf"
    filepath = os.path.join(business_dir, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "file_url": "/" + filepath.replace(os.sep, "/"),
        "filename": file.filename,
        "stored_name": filename,
    }


# Viejos
# def save_course_image(file: UploadFile) -> str | None:
#   if not file:
##
# if not file.content_type.startswith("image/"):
#   raise ValueError("El archivo debe ser una imagen")

# os.makedirs(UPLOAD_DIR_IMAGE_COURSE, exist_ok=True)

# extension = file.filename.split(".")[-1]
# filename = f"{uuid4()}.{extension}"

# filepath = os.path.join(UPLOAD_DIR_IMAGE_COURSE, filename)

# with open(filepath, "wb") as buffer:
#   buffer.write(file.file.read())

# return f"/{filepath}"


# def save_course_voucher(file: UploadFile) -> str | None:
#   if not file:
#      return None

# allowed_types = ["image/jpeg", "image/png", "image/webp", "application/pdf"]

# if file.content_type not in allowed_types:
#   raise ValueError("Solo se permiten imágenes o PDF")

# os.makedirs(UPLOAD_DIR_IMAGE_COURSE_VOUCHER, exist_ok=True)

# extension = file.filename.split(".")[-1].lower()

# filename = f"{uuid4()}.{extension}"
# filepath = os.path.join(UPLOAD_DIR_IMAGE_COURSE_VOUCHER, filename)

# with open(filepath, "wb") as buffer:
#   buffer.write(file.file.read())

# return f"/{filepath}"

"""
def save_lesson_file(file: UploadFile) -> dict | None:
    if not file:
        return None

    allowed_types = ["image/jpeg", "image/png", "image/webp", "application/pdf"]

    if file.content_type not in allowed_types:
        raise ValueError("Solo se permiten imágenes o PDF")

    os.makedirs(UPLOAD_DIR_LESSON_BLOCK_FILE, exist_ok=True)

    extension = file.filename.split(".")[-1].lower()

    filename = f"{uuid4()}.{extension}"
    filepath = os.path.join(UPLOAD_DIR_LESSON_BLOCK_FILE, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "file_url": f"/uploads/lesson_blocks/{filename}",
        "filename": file.filename,
        "stored_name": filename,
    }


# def save_certificate_template_image(file: UploadFile) -> str | None:
#   if not file:
#      return None

# if not file.content_type.startswith("image/"):
#    raise ValueError("El archivo debe ser una imagen")

# os.makedirs(UPLOAD_DIR_IMAGE_COURSE, exist_ok=True)

# extension = file.filename.split(".")[-1]
# filename = f"{uuid4()}.{extension}"

# filepath = os.path.join(UPLOAD_DIR_IMAGE_COURSE, filename)

# with open(filepath, "wb") as buffer:
#   buffer.write(file.file.read())

# return f"/{filepath}"


# def save_certificate(file: UploadFile) -> str | None:
#   if not file:
#      return None

# if file.content_type != "application/pdf":
#    raise ValueError("El archivo debe ser un PDF")

# if not file.filename.lower().endswith(".pdf"):
#   raise ValueError("El archivo debe tener extensión .pdf")

# os.makedirs(UPLOAD_DIR_CERTIFICATES, exist_ok=True)

# filename = f"{uuid4()}.pdf"
# filepath = os.path.join(UPLOAD_DIR_CERTIFICATES, filename)

# with open(filepath, "wb") as buffer:
#   buffer.write(file.file.read())

# return f"/{filepath}"


def save_homework_file(file: UploadFile) -> dict | None:

    if not file:
        return None

    allowed_types = [
        "application/pdf",
        "application/zip",
        "application/x-zip-compressed",
    ]

    if file.content_type not in allowed_types:
        raise ValueError("Solo se permiten archivos PDF o ZIP")

    os.makedirs(UPLOAD_DIR_HOMEWORK_RESPONSES, exist_ok=True)

    extension = file.filename.split(".")[-1].lower()

    allowed_extensions = ["pdf", "zip"]

    if extension not in allowed_extensions:
        raise ValueError("Extensión de archivo no permitida")

    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(UPLOAD_DIR_HOMEWORK_RESPONSES, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "file_url": f"/uploads/homework_responses/{filename}",
        "filename": file.filename,
        "stored_name": filename,
    }


def save_policy_privacy_file(file: UploadFile) -> dict | None:
    if not file:
        return None

    allowed_types = ["application/pdf"]

    if file.content_type not in allowed_types:
        raise ValueError("Solo se permite PDF")

    os.makedirs(UPLOAD_DIR_POLICY_PRIVACY, exist_ok=True)

    extension = file.filename.split(".")[-1].lower()

    filename = f"{uuid4()}.{extension}"
    filepath = os.path.join(UPLOAD_DIR_POLICY_PRIVACY, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "file_url": f"/uploads/policy_privacy/{filename}",
        "filename": file.filename,
        "stored_name": filename,
    }


def save_certificate_mdt(file: UploadFile) -> dict | None:
    if not file:
        return None

    allowed_types = ["application/pdf"]

    if file.content_type not in allowed_types:
        raise ValueError("Solo se permite PDF")

    os.makedirs(UPLOAD_DIR_CERTIFICATE_MDT, exist_ok=True)

    extension = file.filename.split(".")[-1].lower()

    filename = f"{uuid4()}.{extension}"
    filepath = os.path.join(UPLOAD_DIR_CERTIFICATE_MDT, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "file_url": f"/uploads/certificate_mdt/{filename}",
        "filename": file.filename,
        "stored_name": filename,
    }
"""
