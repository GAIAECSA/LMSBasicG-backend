from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, Form, HTTPException, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.utils.jwt import get_current_user

from . import zoom_service
from .config_zoom import settings
from .security_zoom import consume_launch_ticket, create_launch_ticket

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
    except (
        TypeError,
        ValueError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=("No fue posible identificar " "al usuario autenticado."),
        ) from exc

    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inválido.",
        )

    return user_id


@router.get("/jwks")
def jwks():
    """
    Zoom consulta este endpoint para validar
    las firmas JWT emitidas por ATHENA.
    """

    try:
        return zoom_service.get_lti_jwks()

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception("Error generando JWKS.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No fue posible generar el JWKS.",
        ) from exc


@router.get("/zoom/launch/{course_id}")
def launch_tool(
    course_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Lanzamiento directo usando JWT.
    """

    user_id = _extract_user_id(user)

    try:
        return zoom_service.initiate_launch(
            db=db,
            course_id=course_id,
            user_id=user_id,
        )

    except Exception as exc:
        logger.exception("Error iniciando Zoom.")

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


@router.post("/zoom/launch-ticket/{course_id}")
def create_zoom_launch_ticket(
    course_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Genera ticket temporal para abrir Zoom
    en una pestaña nueva sin exponer JWT.
    """

    user_id = _extract_user_id(user)

    try:
        zoom_service.validate_course_access(
            db=db,
            user_id=user_id,
            course_id=course_id,
        )

        ticket = create_launch_ticket(
            user_id=user_id,
            course_id=course_id,
        )

        launch_url = (
            f"{settings.LTI_PUBLIC_ROOT_URL}" f"/zoom/launch-by-ticket/{ticket}"
        )

        return {
            "launch_url": launch_url,
            "expires_in": settings.LTI_LAUNCH_TICKET_TTL_SECONDS,
        }

    except Exception as exc:
        logger.exception("Error creando launch ticket.")

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


@router.get(
    "/zoom/launch-by-ticket/{ticket}",
    response_class=RedirectResponse,
)
def launch_zoom_by_ticket(
    ticket: str,
    db: Session = Depends(get_db),
):
    """
    Consume ticket temporal.
    """

    try:
        ticket_data = consume_launch_ticket(
            ticket,
        )

        return zoom_service.initiate_launch(
            db=db,
            course_id=ticket_data.course_id,
            user_id=ticket_data.user_id,
        )

    except Exception as exc:
        logger.exception("Error consumiendo ticket.")

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


@router.get("/zoom/login")
def lti_login_init(
    iss: str,
    login_hint: str,
    target_link_uri: str,
    lti_message_hint: str | None = None,
    client_id: str | None = None,
):
    """
    Endpoint requerido por LTI 1.3.
    """

    return {
        "status": "ready",
        "issuer": iss,
        "target_link_uri": target_link_uri,
        "has_login_hint": bool(login_hint),
        "lti_message_hint": lti_message_hint,
        "client_id": client_id,
    }


@router.get(
    "/zoom/authorize",
    response_class=HTMLResponse,
)
def lti_authorize(
    client_id: str,
    redirect_uri: str,
    response_type: str,
    state: str,
    nonce: str,
    login_hint: str,
    lti_message_hint: str,
    scope: str = Query(
        default="openid",
    ),
    response_mode: str = Query(
        default="form_post",
    ),
    prompt: str = Query(
        default="none",
    ),
    db: Session = Depends(get_db),
):
    """
    Zoom retorna aquí para solicitar
    el id_token firmado.
    """

    del prompt

    try:
        return zoom_service.process_authorization(
            db=db,
            client_id=client_id,
            redirect_uri=redirect_uri,
            response_type=response_type,
            state=state,
            nonce=nonce,
            login_hint=login_hint,
            lti_message_hint=lti_message_hint,
            scope=scope,
            response_mode=response_mode,
        )

    except Exception as exc:
        logger.exception("Error en authorize.")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/token")
def lti_token(
    grant_type: str = Form(...),
    client_assertion_type: str = Form(...),
    client_assertion: str = Form(...),
    scope: str = Form(""),
):
    """
    Endpoint OAuth2 para servicios
    LTI Advantage.
    """

    try:
        return zoom_service.generate_access_token(
            grant_type=grant_type,
            client_assertion_type=client_assertion_type,
            client_assertion=client_assertion,
            scope=scope,
        )

    except Exception as exc:
        logger.exception("Error generando token.")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
