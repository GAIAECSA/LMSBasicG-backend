# schemas/mdt_certificate.py

from datetime import datetime
from typing import Literal, Optional

from fastapi import Form
from pydantic import BaseModel, Field


class MdtCertificateCreate(BaseModel):
    course_id: int = Field(..., gt=0)

    id_number: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    certificate_type: Literal["MDT", "INSTITUTIONAL"]

    @classmethod
    def as_form(
        cls,
        course_id: int = Form(...),
        id_number: str = Form(...),
        certificate_type: Literal["MDT", "INSTITUTIONAL"] = Form(...),
    ):
        return cls(
            course_id=course_id,
            id_number=id_number,
            certificate_type=certificate_type,
        )


class MdtBulkCertificateCreate(BaseModel):
    course_id: int = Field(..., gt=0)
    certificate_type: Literal["MDT", "INSTITUTIONAL"]

    @classmethod
    def as_form(
        cls,
        course_id: int = Form(...),
        certificate_type: Literal["MDT", "INSTITUTIONAL"] = Form(...),
    ):
        return cls(
            course_id=course_id,
            certificate_type=certificate_type,
        )


class MdtCertificateUpdate(BaseModel):
    deleted: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        deleted: Optional[bool] = Form(None),
    ):
        return cls(
            deleted=deleted,
        )


class MdtCertificateResponse(BaseModel):
    id: int

    course_id: int

    file_url: str
    file_name: str

    id_number: str

    certificate_type: str

    deleted: bool

    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
