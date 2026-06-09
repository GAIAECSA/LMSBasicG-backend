from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .config_zoom import settings


def validate_timezone_name(value: str) -> str:
    normalized_value = value.strip()

    try:
        ZoneInfo(normalized_value)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Zona horaria no válida: {value}") from exc

    return normalized_value


def validate_timezone_aware_datetime(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(
            "start_time debe incluir zona horaria. "
            "Ejemplo: 2026-06-09T15:00:00-05:00"
        )

    return value


class ZoomMeetingCreate(BaseModel):
    course_id: int = Field(..., gt=0)
    topic: str = Field(..., min_length=3, max_length=255)
    start_time: datetime
    duration: int = Field(
        default=settings.ZOOM_DEFAULT_DURATION_MINUTES,
        ge=1,
        le=1440,
    )
    timezone: str = Field(default=settings.ZOOM_DEFAULT_TIMEZONE, max_length=64)
    password: str | None = Field(default=None, min_length=1, max_length=10)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        return value.strip()

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        return validate_timezone_name(value)

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, value: datetime) -> datetime:
        return validate_timezone_aware_datetime(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized_value = value.strip()

        if not normalized_value:
            return None

        return normalized_value


class ZoomMeetingUpdate(BaseModel):
    topic: str | None = Field(default=None, min_length=3, max_length=255)
    start_time: datetime | None = None
    duration: int | None = Field(default=None, ge=1, le=1440)
    timezone: str | None = Field(default=None, max_length=64)
    password: str | None = Field(default=None, min_length=1, max_length=10)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip()

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_timezone_name(value)

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None

        return validate_timezone_aware_datetime(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized_value = value.strip()

        if not normalized_value:
            return None

        return normalized_value

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "ZoomMeetingUpdate":
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo para actualizar.")

        return self


class ZoomMeetingOut(BaseModel):
    id: int
    course_id: int
    teacher_id: int

    zoom_meeting_id: str
    zoom_host_user_id: str | None = None

    topic: str
    start_time: datetime
    duration: int
    timezone: str
    password: str | None = None
    join_url: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ZoomStartUrlOut(BaseModel):
    meeting_id: int
    zoom_meeting_id: str
    start_url: str
