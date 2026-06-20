from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.utils.jwt import get_current_user

from . import zoom_service
from .schemas_zoom import (
    ZoomMeetingCreate,
    ZoomMeetingOut,
    ZoomMeetingUpdate,
    ZoomStartUrlOut,
)

# Asegúrate de importar el tipo de tu sesión. Ajusta la ruta si es necesario.
# from app.schemas.auth import UserSession


logger = logging.getLogger(__name__)

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def _extract_session_data(current_user: Any) -> tuple[int, int]:
    business_id = getattr(current_user, "business_id", None)
    user_id = getattr(current_user, "user_id", getattr(current_user, "id", None))

    if not business_id or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No fue posible identificar la sesión del usuario o el negocio.",
        )
    return int(business_id), int(user_id)


@router.post(
    "/meetings",
    response_model=ZoomMeetingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_zoom_meeting(
    payload: ZoomMeetingCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),  # current_user: UserSession
):
    """
    POST /api/v1/zoom/meetings

    Solo docente.
    Crea reunión en Zoom y guarda join_url en la base.
    No guarda start_url.
    """
    business_id, user_id = _extract_session_data(current_user)

    try:
        return zoom_service.create_meeting(
            db=db,
            business_id=business_id,
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
    current_user: Any = Depends(get_current_user),
):
    """
    GET /api/v1/zoom/courses/{course_id}/meetings

    Docente y estudiantes matriculados.
    Los estudiantes usan join_url para entrar.
    """
    business_id, user_id = _extract_session_data(current_user)

    try:
        return zoom_service.list_course_meetings(
            db=db,
            business_id=business_id,
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
    current_user: Any = Depends(get_current_user),
):
    """
    GET /api/v1/zoom/meetings/{meeting_id}

    meeting_id puede ser el id interno o zoom_meeting_id.
    """
    business_id, user_id = _extract_session_data(current_user)

    try:
        return zoom_service.get_meeting(
            db=db,
            business_id=business_id,
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
    current_user: Any = Depends(get_current_user),
):
    """
    GET /api/v1/zoom/meetings/{meeting_id}/start

    Solo docente.
    Consulta Zoom en tiempo real y devuelve start_url actualizado.
    """
    business_id, user_id = _extract_session_data(current_user)

    try:
        return zoom_service.get_start_url(
            db=db,
            business_id=business_id,
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
    current_user: Any = Depends(get_current_user),
):
    """
    PUT /api/v1/zoom/meetings/{meeting_id}

    Tu backend expone PUT, pero internamente Zoom usa PATCH.
    Solo docente.
    """
    business_id, user_id = _extract_session_data(current_user)

    try:
        return zoom_service.update_meeting(
            db=db,
            business_id=business_id,
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
    current_user: Any = Depends(get_current_user),
):
    """
    DELETE /api/v1/zoom/meetings/{meeting_id}

    Solo docente.
    Elimina en Zoom y marca deleted=True en la base.
    """
    business_id, user_id = _extract_session_data(current_user)

    try:
        zoom_service.delete_meeting(
            db=db,
            business_id=business_id,
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
