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
        course_id: int = Form(...),
        fields: Optional[str] = Form(None),
        qr_config: Optional[str] = Form(None),
    ):
        return cls(
            course_id=course_id,
            fields=json.loads(fields) if fields else None,
            qr_config=json.loads(qr_config) if qr_config else None,
        )

    @field_validator("fields")
    def validate_fields(cls, v):
        if v is not None and not isinstance(v, list):
            raise ValueError("fields debe ser una lista")
        return v


class CertificateTemplateUpdate(BaseModel):
    background_image_url: Optional[str] = None
    fields: Optional[List[Dict[str, Any]]] = None
    qr_config: Optional[Dict[str, Any]] = None

    @classmethod
    def as_form(
        cls,
        fields: Optional[str] = Form(None),
        qr_config: Optional[str] = Form(None),
    ):
        return cls(
            fields=json.loads(fields) if fields else None,
            qr_config=json.loads(qr_config) if qr_config else None,
        )

    @field_validator("fields")
    def validate_fields(cls, v):
        if v is not None and not isinstance(v, list):
            raise ValueError("fields debe ser una lista")
        return v


class CertificateTemplateResponse(BaseModel):
    id: int
    course_id: int
    background_image_url: Optional[str]
    fields: Optional[List[Dict[str, Any]]]
    qr_config: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True