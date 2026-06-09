from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.utils.jwt import get_current_user

from . import zoom_service
from .schemas_zoom import ZoomMeetingCreate, ZoomMeetingOut, ZoomMeetingUpdate, ZoomStartUrlOut

logger = logging.getLogger(__name__)

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def _extract_user_id(user: Any) -> int:
    raw_user_id = None

    if isinstance(user, dict):
        raw_user_id = user.get("user_id") or user.get("id")
    else:
        raw_user_id = getattr(user, "user_id", None) or getattr(user, "id", None)

    try:
        user_id = int(raw_user_id)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No fue posible identificar al usuario autenticado.",
        ) from exc

    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inválido.",
        )

    return user_id


@router.post(
    "/meetings",
    response_model=ZoomMeetingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_zoom_meeting(
    payload: ZoomMeetingCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    POST /api/v1/zoom/meetings

    Solo docente.
    Crea reunión en Zoom y guarda join_url en la base.
    No guarda start_url.
    """

    user_id = _extract_user_id(user)

    try:
        return zoom_service.create_meeting(
            db=db,
            user_id=user_id,
            payload=payload,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error creando reunión Zoom.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible crear la reunión Zoom.",
        ) from exc


@router.get(
    "/courses/{course_id}/meetings",
    response_model=list[ZoomMeetingOut],
)
def list_zoom_meetings_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    GET /api/v1/zoom/courses/{course_id}/meetings

    Docente y estudiantes matriculados.
    Los estudiantes usan join_url para entrar.
    """

    user_id = _extract_user_id(user)

    try:
        return zoom_service.list_course_meetings(
            db=db,
            user_id=user_id,
            course_id=course_id,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error listando reuniones Zoom.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible listar las reuniones Zoom.",
        ) from exc


@router.get(
    "/meetings/{meeting_id}",
    response_model=ZoomMeetingOut,
)
def get_zoom_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    GET /api/v1/zoom/meetings/{meeting_id}

    meeting_id puede ser el id interno o zoom_meeting_id.
    """

    user_id = _extract_user_id(user)

    try:
        return zoom_service.get_meeting(
            db=db,
            user_id=user_id,
            meeting_id=meeting_id,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error obteniendo reunión Zoom.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible obtener la reunión Zoom.",
        ) from exc


@router.get(
    "/meetings/{meeting_id}/start",
    response_model=ZoomStartUrlOut,
)
def start_zoom_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    GET /api/v1/zoom/meetings/{meeting_id}/start

    Solo docente.
    Consulta Zoom en tiempo real y devuelve start_url actualizado.
    """

    user_id = _extract_user_id(user)

    try:
        return zoom_service.get_start_url(
            db=db,
            user_id=user_id,
            meeting_id=meeting_id,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error obteniendo start_url Zoom.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible obtener el enlace de inicio Zoom.",
        ) from exc


@router.put(
    "/meetings/{meeting_id}",
    response_model=ZoomMeetingOut,
)
def update_zoom_meeting(
    meeting_id: str,
    payload: ZoomMeetingUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    PUT /api/v1/zoom/meetings/{meeting_id}

    Tu backend expone PUT, pero internamente Zoom usa PATCH.
    Solo docente.
    """

    user_id = _extract_user_id(user)

    try:
        return zoom_service.update_meeting(
            db=db,
            user_id=user_id,
            meeting_id=meeting_id,
            payload=payload,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error actualizando reunión Zoom.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible actualizar la reunión Zoom.",
        ) from exc


@router.delete(
    "/meetings/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_zoom_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    DELETE /api/v1/zoom/meetings/{meeting_id}

    Solo docente.
    Elimina en Zoom y marca deleted=True en la base.
    """

    user_id = _extract_user_id(user)

    try:
        zoom_service.delete_meeting(
            db=db,
            user_id=user_id,
            meeting_id=meeting_id,
        )

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error eliminando reunión Zoom.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible eliminar la reunión Zoom.",
        ) from exc
