# app/schemas/privacy_policy.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from fastapi import Form


class PrivacyPolicyCreate(BaseModel):
    title: str
    version: str

    is_active: bool = True
    mandatory: bool = True

    effective_date: datetime

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        version: str = Form(...),
        is_active: bool = Form(True),
        mandatory: bool = Form(True),
        effective_date: datetime = Form(...),
    ):
        return cls(
            title=title,
            version=version,
            is_active=is_active,
            mandatory=mandatory,
            effective_date=effective_date,
        )


class PrivacyPolicyUpdate(BaseModel):
    title: Optional[str] = None
    version: Optional[str] = None

    is_active: Optional[bool] = None
    mandatory: Optional[bool] = None

    effective_date: Optional[datetime] = None

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(None),
        version: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(None),
        mandatory: Optional[bool] = Form(None),
        effective_date: Optional[datetime] = Form(None),
    ):
        return cls(
            title=title,
            version=version,
            is_active=is_active,
            mandatory=mandatory,
            effective_date=effective_date,
        )


class PrivacyPolicyResponse(BaseModel):
    id: int

    title: str
    version: str

    pdf_url: Optional[str] = None

    is_active: bool
    mandatory: bool

    effective_date: datetime

    deleted: bool

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
