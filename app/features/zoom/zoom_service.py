from __future__ import annotations

from datetime import datetime, timedelta, timezone
from html import escape
from urllib.parse import urlencode
from uuid import uuid4

from fastapi import HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload

from app.models.enrollment import Enrollment

from .config_zoom import settings
from .security_zoom import (
    CLIENT_ASSERTION_TYPE,
    create_login_hint,
    decode_login_hint,
    get_jwks,
    issue_service_access_token,
    sign_lti_jwt,
    validate_requested_scopes,
    validate_zoom_client_assertion,
)

INSTRUCTOR_ROLE = "http://purl.imsglobal.org" "/vocab/lis/v2/membership#Instructor"

LEARNER_ROLE = "http://purl.imsglobal.org" "/vocab/lis/v2/membership#Learner"

MEMBER_ROLE = "http://purl.imsglobal.org" "/vocab/lis/v2/membership#Member"

COURSE_SECTION_TYPE = "http://purl.imsglobal.org" "/vocab/lis/v2/course#CourseSection"


def get_lti_jwks() -> dict:
    return get_jwks()


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
    """
    Obtiene la matrícula activa real del usuario.
    También carga el perfil requerido para crear claims.
    """

    return (
        db.query(Enrollment)
        .options(
            joinedload(
                Enrollment.user,
            ),
        )
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
    valid_user_id = _validate_positive_integer(
        user_id,
        "Usuario",
    )

    valid_course_id = _validate_positive_integer(
        course_id,
        "Curso",
    )

    enrollment = _get_active_enrollment(
        db=db,
        user_id=valid_user_id,
        course_id=valid_course_id,
    )

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=("No tienes una matrícula activa " "en este curso."),
        )

    return enrollment


def _get_lti_roles(
    role_id: int,
) -> list[str]:
    if role_id == 3:
        return [
            INSTRUCTOR_ROLE,
        ]

    if role_id == 4:
        return [
            LEARNER_ROLE,
        ]

    return [
        MEMBER_ROLE,
    ]


def initiate_launch(
    db: Session,
    course_id: int,
    user_id: int,
) -> RedirectResponse:
    """
    Paso inicial:
    ATHENA redirige el navegador hacia el Login
    Initiation URL entregado por Zoom LTI Pro.
    """

    enrollment = validate_course_access(
        db=db,
        user_id=user_id,
        course_id=course_id,
    )

    signed_login_hint = create_login_hint(
        user_id=enrollment.user_id,
        course_id=enrollment.course_id,
    )

    params = {
        "iss": settings.LMS_ISSUER,
        "target_link_uri": (settings.ZOOM_TARGET_LINK_URI),
        "login_hint": signed_login_hint,
        "lti_message_hint": str(
            enrollment.course_id,
        ),
        "client_id": (settings.ZOOM_LTI_CLIENT_ID),
    }

    query_string = urlencode(
        params,
    )

    login_url = f"{settings.ZOOM_LOGIN_INIT_URI}" f"?{query_string}"

    return RedirectResponse(
        url=login_url,
        status_code=status.HTTP_302_FOUND,
        headers={
            "Cache-Control": "no-store",
            "Pragma": "no-cache",
        },
    )


def process_authorization(
    db: Session,
    client_id: str,
    redirect_uri: str,
    response_type: str,
    state: str,
    nonce: str,
    login_hint: str,
    lti_message_hint: str,
    scope: str = "openid",
    response_mode: str = "form_post",
) -> HTMLResponse:
    """
    Zoom devuelve el control hacia ATHENA.

    ATHENA valida la solicitud, firma el id_token y
    lo publica nuevamente hacia Zoom usando un
    formulario HTML autoenviado.
    """

    if client_id != settings.ZOOM_LTI_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El client_id no coincide.",
        )

    if redirect_uri.rstrip("/") != settings.ZOOM_OAUTH_REDIRECT_URI.rstrip("/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El redirect_uri no está autorizado.",
        )

    if response_type != "id_token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("El response_type debe ser id_token."),
        )

    if scope != "openid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El scope debe ser openid.",
        )

    if response_mode != "form_post":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("El response_mode debe ser form_post."),
        )

    if not state.strip() or not nonce.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="state y nonce son obligatorios.",
        )

    login_data = decode_login_hint(
        login_hint,
    )

    valid_course_id = _validate_positive_integer(
        int(lti_message_hint),
        "Curso",
    )

    if login_data.course_id != valid_course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("El contexto del curso fue modificado " "durante el lanzamiento."),
        )

    enrollment = validate_course_access(
        db=db,
        user_id=login_data.user_id,
        course_id=login_data.course_id,
    )

    if not enrollment.user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("La matrícula no tiene un usuario asociado."),
        )

    firstname = (enrollment.user.firstname or "").strip()

    lastname = (enrollment.user.lastname or "").strip()

    email = (enrollment.user.email or "").strip()

    full_name = (f"{firstname} {lastname}").strip()

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("El usuario debe tener un correo " "electrónico registrado."),
        )

    now = int(
        datetime.now(
            timezone.utc,
        ).timestamp()
    )

    payload = {
        "iss": settings.LMS_ISSUER,
        "aud": client_id,
        "azp": client_id,
        "exp": now
        + int(
            timedelta(
                minutes=5,
            ).total_seconds()
        ),
        "iat": now,
        "sub": str(
            enrollment.user.id,
        ),
        "nonce": nonce,
        "name": full_name,
        "given_name": firstname,
        "family_name": lastname,
        "email": email,
        (
            "https://purl.imsglobal.org" "/spec/lti/claim/message_type"
        ): "LtiResourceLinkRequest",
        ("https://purl.imsglobal.org" "/spec/lti/claim/version"): "1.3.0",
        (
            "https://purl.imsglobal.org" "/spec/lti/claim/deployment_id"
        ): settings.LTI_DEPLOYMENT_ID,
        (
            "https://purl.imsglobal.org" "/spec/lti/claim/target_link_uri"
        ): settings.ZOOM_TARGET_LINK_URI,
        ("https://purl.imsglobal.org" "/spec/lti/claim/resource_link"): {
            "id": ("zoom_course_" f"{enrollment.course_id}"),
            "title": ("Sala de videoconferencia Zoom"),
        },
        ("https://purl.imsglobal.org" "/spec/lti/claim/roles"): _get_lti_roles(
            enrollment.role_id,
        ),
        ("https://purl.imsglobal.org" "/spec/lti/claim/context"): {
            "id": str(
                enrollment.course_id,
            ),
            "label": (f"COURSE-{enrollment.course_id}"),
            "title": (f"Curso ID {enrollment.course_id}"),
            "type": [
                COURSE_SECTION_TYPE,
            ],
        },
        ("https://purl.imsglobal.org" "/spec/lti/claim/tool_platform"): {
            "guid": "gaia-academic-platform",
            "name": "Gaia Academic LMS",
            "url": settings.LMS_ISSUER,
        },
        ("https://purl.imsglobal.org" "/spec/lti/claim/launch_presentation"): {
            "locale": "es-EC",
            "document_target": "window",
        },
        "jti": str(
            uuid4(),
        ),
    }

    id_token = sign_lti_jwt(
        payload,
    )

    safe_redirect_uri = escape(
        redirect_uri,
        quote=True,
    )

    safe_id_token = escape(
        id_token,
        quote=True,
    )

    safe_state = escape(
        state,
        quote=True,
    )

    html_form = f"""
    <!doctype html>
    <html lang="es">
        <head>
            <meta charset="utf-8" />
            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            />
            <title>Conectando con Zoom</title>
        </head>
        <body
            onload="document.forms['ltiLaunchForm'].submit();"
            style="
                min-height: 100vh;
                display: grid;
                place-items: center;
                margin: 0;
                padding: 24px;
                box-sizing: border-box;
                font-family: Arial, sans-serif;
                background: #f8fafc;
                color: #172861;
            "
        >
            <main style="text-align: center;">
                <h2 style="margin: 0 0 8px;">
                    Conectando con Zoom...
                </h2>

                <p style="margin: 0;">
                    Validando el acceso seguro al curso.
                </p>

                <form
                    name="ltiLaunchForm"
                    method="POST"
                    action="{safe_redirect_uri}"
                >
                    <input
                        type="hidden"
                        name="id_token"
                        value="{safe_id_token}"
                    />

                    <input
                        type="hidden"
                        name="state"
                        value="{safe_state}"
                    />
                </form>
            </main>
        </body>
    </html>
    """

    return HTMLResponse(
        content=html_form,
        headers={
            "Cache-Control": "no-store",
            "Pragma": "no-cache",
        },
    )


def generate_access_token(
    grant_type: str,
    client_assertion_type: str,
    client_assertion: str,
    scope: str,
) -> dict:
    """
    OAuth 2.0 Client Credentials para servicios LTI
    Advantage. No se utiliza durante el lanzamiento
    básico, pero debe quedar protegido correctamente.
    """

    if grant_type != "client_credentials":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="grant_type no válido.",
        )

    if client_assertion_type != CLIENT_ASSERTION_TYPE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("client_assertion_type no válido."),
        )

    validate_zoom_client_assertion(
        client_assertion,
    )

    normalized_scope = validate_requested_scopes(
        scope,
    )

    return issue_service_access_token(
        normalized_scope,
    )
