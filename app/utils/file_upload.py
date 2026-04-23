import os
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_DIR = "uploads/courses"


def save_course_image(file: UploadFile) -> str | None:
    if not file:
        return None

    # validar que sea imagen
    if not file.content_type.startswith("image/"):
        raise ValueError("El archivo debe ser una imagen")

    # crear carpeta si no existe
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # generar nombre único
    extension = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(UPLOAD_DIR, filename)

    # guardar archivo
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    # devolver ruta para guardar en BD
    return f"/{filepath}"