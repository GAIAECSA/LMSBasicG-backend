from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any
from fastapi import Form
import json


class CertificateTemplateCreate(BaseModel):
    course_id: int
    background_image_url: Optional[str] = None
    fields: Optional[List[Dict[str, Any]]] = None
    qr_config: Optional[Dict[str, Any]] = None

    @classmethod
    def as_form(
        cls,
        data: str = Form(...)
    ):
        payload = json.loads(data)

        return cls(
            course_id=payload.get("course_id"),
            fields=payload.get("fields"),
            qr_config=payload.get("qr_config"),
            background_image_url=None
        )

    @field_validator("fields")
    def validate_fields(cls, v):
        if v is not None and not isinstance(v, list):
            raise ValueError("fields debe ser una lista")
        return v


class CertificateTemplateUpdate(BaseModel):
    course_id: Optional[int] = None
    fields: Optional[List[Dict[str, Any]]] = None
    qr_config: Optional[Dict[str, Any]] = None

    @classmethod
    def as_form(
        cls,
        data: str = Form(...)
    ):
        payload = json.loads(data)

        return cls(
            course_id=payload.get("course_id"),
            fields=payload.get("fields"),
            qr_config=payload.get("qr_config")
        )


class CertificateTemplateResponse(BaseModel):
    id: int
    course_id: int
    background_image_url: Optional[str]
    fields: Optional[List[Dict[str, Any]]]
    qr_config: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True