from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.enrollment import Enrollment
from app.models.zoom_meeting import ZoomMeeting

from .config_zoom import settings
from .schemas_zoom import ZoomMeetingCreate, ZoomMeetingUpdate
from .zoom_api_client import zoom_client


def _validate_positive_integer(
    value: int,
    label: str,
) -> int:
    numeric_value = int(value)

    if numeric_value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{label} no válido.",
        )

    return numeric_value


def _get_active_enrollment(
    db: Session,
    user_id: int,
    course_id: int,
) -> Enrollment | None:
    return (
        db.query(Enrollment)
        .options(joinedload(Enrollment.user))
        .filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
            Enrollment.deleted.is_(False),
        )
        .first()
    )


def validate_course_access(
    db: Session,
    user_id: int,
    course_id: int,
) -> Enrollment:
    valid_user_id = _validate_positive_integer(user_id, "Usuario")
    valid_course_id = _validate_positive_integer(course_id, "Curso")

    enrollment = _get_active_enrollment(
        db=db,
        user_id=valid_user_id,
        course_id=valid_course_id,
    )

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes una matrícula activa en este curso.",
        )

    return enrollment


def validate_teacher_access(
    db: Session,
    user_id: int,
    course_id: int,
) -> Enrollment:
    enrollment = validate_course_access(
        db=db,
        user_id=user_id,
        course_id=course_id,
    )

    if enrollment.role_id != settings.TEACHER_ROLE_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el docente puede realizar esta acción.",
        )

    return enrollment


def _to_utc(value: datetime) -> datetime:
    return value.astimezone(timezone.utc)


def _format_zoom_start_time(
    start_time: datetime,
    timezone_name: str,
) -> str:
    """
    Zoom recibe start_time como fecha local y timezone separado.
    Ejemplo: 2026-06-09T10:00:00 + America/Guayaquil.
    """
    local_timezone = ZoneInfo(timezone_name)
    local_start_time = start_time.astimezone(local_timezone)

    return local_start_time.replace(
        tzinfo=None,
        microsecond=0,
    ).isoformat()


def _build_zoom_create_payload(
    payload: ZoomMeetingCreate,
) -> dict[str, Any]:
    zoom_payload: dict[str, Any] = {
        "topic": payload.topic,
        "type": 2,
        "start_time": _format_zoom_start_time(
            payload.start_time,
            payload.timezone,
        ),
        "duration": payload.duration,
        "timezone": payload.timezone,
        "settings": {
            "join_before_host": False,
            "waiting_room": True,
            "mute_upon_entry": True,
            "approval_type": 2,
            "audio": "both",
            "auto_recording": "none",
        },
    }

    if payload.password:
        zoom_payload["password"] = payload.password

    return zoom_payload


def _build_zoom_update_payload(
    meeting: ZoomMeeting,
    payload: ZoomMeetingUpdate,
) -> dict[str, Any]:
    zoom_payload: dict[str, Any] = {}

    fields_set = payload.model_fields_set

    next_timezone = (
        payload.timezone
        if "timezone" in fields_set and payload.timezone is not None
        else meeting.timezone
    )

    if "topic" in fields_set and payload.topic is not None:
        zoom_payload["topic"] = payload.topic

    if "start_time" in fields_set and payload.start_time is not None:
        zoom_payload["start_time"] = _format_zoom_start_time(
            payload.start_time,
            next_timezone,
        )

    if "duration" in fields_set and payload.duration is not None:
        zoom_payload["duration"] = payload.duration

    if "timezone" in fields_set and payload.timezone is not None:
        zoom_payload["timezone"] = payload.timezone

    if "password" in fields_set and payload.password is not None:
        zoom_payload["password"] = payload.password

    if not zoom_payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay campos válidos para actualizar.",
        )

    return zoom_payload


def _get_meeting_or_404(
    db: Session,
    business_id: int,
    meeting_id: str,
) -> ZoomMeeting:
    cleaned_meeting_id = str(meeting_id).strip()

    filters = [
        ZoomMeeting.zoom_meeting_id == cleaned_meeting_id,
    ]

    if cleaned_meeting_id.isdigit():
        filters.append(ZoomMeeting.id == int(cleaned_meeting_id))

    meeting = (
        db.query(ZoomMeeting)
        .filter(
            ZoomMeeting.business_id == business_id,
            or_(*filters),
            ZoomMeeting.deleted.is_(False),
        )
        .first()
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La reunión no existe.",
        )

    return meeting


def create_meeting(
    db: Session,
    business_id: int,
    user_id: int,
    payload: ZoomMeetingCreate,
) -> ZoomMeeting:
    with db.begin():
        enrollment = validate_teacher_access(
            db=db,
            user_id=user_id,
            course_id=payload.course_id,
        )

        zoom_payload = _build_zoom_create_payload(payload)

        zoom_response = zoom_client.create_meeting(
            user_id=settings.ZOOM_HOST_EMAIL,
            payload=zoom_payload,
        )

        zoom_meeting_id = zoom_response.get("id")
        join_url = zoom_response.get("join_url")

        if not zoom_meeting_id or not join_url:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Zoom no devolvió id o join_url.",
            )

        meeting = ZoomMeeting(
            business_id=business_id,
            course_id=enrollment.course_id,
            teacher_id=enrollment.user_id,
            zoom_meeting_id=str(zoom_meeting_id),
            zoom_host_user_id=zoom_response.get("host_id"),
            topic=payload.topic,
            start_time=_to_utc(payload.start_time),
            duration=payload.duration,
            timezone=payload.timezone,
            password=zoom_response.get("password") or payload.password,
            join_url=join_url,
        )

        db.add(meeting)

    db.refresh(meeting)
    return meeting


def list_course_meetings(
    db: Session,
    business_id: int,
    user_id: int,
    course_id: int,
) -> list[ZoomMeeting]:
    with db.begin():
        validate_course_access(
            db=db,
            user_id=user_id,
            course_id=course_id,
        )

        return (
            db.query(ZoomMeeting)
            .filter(
                ZoomMeeting.business_id == business_id,
                ZoomMeeting.course_id == course_id,
                ZoomMeeting.deleted.is_(False),
            )
            .order_by(
                ZoomMeeting.start_time.asc(),
                ZoomMeeting.id.asc(),
            )
            .all()
        )


def get_meeting(
    db: Session,
    business_id: int,
    user_id: int,
    meeting_id: str,
) -> ZoomMeeting:
    with db.begin():
        meeting = _get_meeting_or_404(
            db=db,
            business_id=business_id,
            meeting_id=meeting_id,
        )

        validate_course_access(
            db=db,
            user_id=user_id,
            course_id=meeting.course_id,
        )

        return meeting


def get_start_url(
    db: Session,
    business_id: int,
    user_id: int,
    meeting_id: str,
) -> dict[str, Any]:
    with db.begin():
        meeting = _get_meeting_or_404(
            db=db,
            business_id=business_id,
            meeting_id=meeting_id,
        )

        validate_teacher_access(
            db=db,
            user_id=user_id,
            course_id=meeting.course_id,
        )

        zoom_response = zoom_client.get_meeting(
            meeting.zoom_meeting_id,
        )

        start_url = zoom_response.get("start_url")

        if not start_url:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Zoom no devolvió start_url.",
            )

        return {
            "meeting_id": meeting.id,
            "zoom_meeting_id": meeting.zoom_meeting_id,
            "start_url": start_url,
        }


def update_meeting(
    db: Session,
    business_id: int,
    user_id: int,
    meeting_id: str,
    payload: ZoomMeetingUpdate,
) -> ZoomMeeting:
    with db.begin():
        meeting = _get_meeting_or_404(
            db=db,
            business_id=business_id,
            meeting_id=meeting_id,
        )

        validate_teacher_access(
            db=db,
            user_id=user_id,
            course_id=meeting.course_id,
        )

        zoom_payload = _build_zoom_update_payload(
            meeting=meeting,
            payload=payload,
        )

        zoom_response = zoom_client.update_meeting(
            meeting_id=meeting.zoom_meeting_id,
            payload=zoom_payload,
        )

        fields_set = payload.model_fields_set

        if "topic" in fields_set and payload.topic is not None:
            meeting.topic = payload.topic

        if "start_time" in fields_set and payload.start_time is not None:
            meeting.start_time = _to_utc(payload.start_time)

        if "duration" in fields_set and payload.duration is not None:
            meeting.duration = payload.duration

        if "timezone" in fields_set and payload.timezone is not None:
            meeting.timezone = payload.timezone

        if "password" in fields_set and payload.password is not None:
            meeting.password = zoom_response.get("password") or payload.password

        if zoom_response.get("join_url"):
            meeting.join_url = zoom_response["join_url"]

    db.refresh(meeting)
    return meeting


def delete_meeting(
    db: Session,
    business_id: int,
    user_id: int,
    meeting_id: str,
) -> None:
    with db.begin():
        meeting = _get_meeting_or_404(
            db=db,
            business_id=business_id,
            meeting_id=meeting_id,
        )

        validate_teacher_access(
            db=db,
            user_id=user_id,
            course_id=meeting.course_id,
        )

        try:
            zoom_client.delete_meeting(
                meeting.zoom_meeting_id,
            )
        except HTTPException as exc:
            if exc.status_code != status.HTTP_404_NOT_FOUND:
                raise

        meeting.deleted = True
