from __future__ import annotations

import base64
import secrets
import threading
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import HTTPException, status
from jwt import PyJWKClient
from jwt.exceptions import PyJWKClientError, PyJWTError

from .config_zoom import settings

CLIENT_ASSERTION_TYPE = "urn:ietf:params:oauth:" "client-assertion-type:jwt-bearer"

LOGIN_HINT_AUDIENCE = "zoom-lti-login-hint"


@dataclass(frozen=True)
class LoginHintData:
    user_id: int
    course_id: int


@dataclass(frozen=True)
class LaunchTicketData:
    user_id: int
    course_id: int
    expires_at: float


@dataclass(frozen=True)
class ServiceAccessTokenData:
    scope: str
    expires_at: float


_launch_tickets: dict[
    str,
    LaunchTicketData,
] = {}

_service_access_tokens: dict[
    str,
    ServiceAccessTokenData,
] = {}

_ticket_lock = threading.Lock()
_access_token_lock = threading.Lock()


def _int_to_base64(
    value: int,
) -> str:
    raw_value = value.to_bytes(
        (value.bit_length() + 7) // 8,
        byteorder="big",
    )

    return (
        base64.urlsafe_b64encode(
            raw_value,
        )
        .decode("utf-8")
        .rstrip("=")
    )


@lru_cache(maxsize=1)
def _get_private_key() -> rsa.RSAPrivateKey:
    private_key_path = Path(
        settings.LTI_PRIVATE_KEY_PATH,
    )

    if not private_key_path.exists():
        raise RuntimeError(
            "No se encontró la clave privada LTI en: " f"{private_key_path}"
        )

    raw_private_key = private_key_path.read_bytes()

    private_key = serialization.load_pem_private_key(
        raw_private_key,
        password=None,
    )

    if not isinstance(
        private_key,
        rsa.RSAPrivateKey,
    ):
        raise RuntimeError("La clave privada LTI debe ser RSA.")

    return private_key


def get_jwks() -> dict[str, list[dict[str, str]]]:
    """
    Expone la clave pública de ATHENA para que
    Zoom valide las firmas de los id_token.
    """

    public_key = _get_private_key().public_key()

    numbers = public_key.public_numbers()

    jwk = {
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "kid": settings.LTI_KEY_ID,
        "n": _int_to_base64(numbers.n),
        "e": _int_to_base64(numbers.e),
    }

    return {
        "keys": [
            jwk,
        ],
    }


def sign_lti_jwt(
    payload: dict[str, Any],
) -> str:
    """
    Firma el id_token enviado desde ATHENA hacia Zoom.
    """

    headers = {
        "kid": settings.LTI_KEY_ID,
        "typ": "JWT",
    }

    return jwt.encode(
        payload=payload,
        key=_get_private_key(),
        algorithm="RS256",
        headers=headers,
    )


def create_login_hint(
    user_id: int,
    course_id: int,
) -> str:
    """
    Crea un login_hint firmado y de corta duración.

    Evita exponer user_id como valor manipulable.
    """

    now = int(time.time())

    payload = {
        "iss": settings.LMS_ISSUER,
        "aud": LOGIN_HINT_AUDIENCE,
        "sub": str(user_id),
        "course_id": course_id,
        "purpose": "zoom-lti-login-hint",
        "iat": now,
        "exp": (now + settings.LTI_LOGIN_HINT_TTL_SECONDS),
        "jti": secrets.token_urlsafe(16),
    }

    return jwt.encode(
        payload=payload,
        key=settings.LTI_INTERNAL_SIGNING_SECRET,
        algorithm="HS256",
    )


def decode_login_hint(
    login_hint: str,
) -> LoginHintData:
    try:
        payload = jwt.decode(
            jwt=login_hint,
            key=settings.LTI_INTERNAL_SIGNING_SECRET,
            algorithms=[
                "HS256",
            ],
            audience=LOGIN_HINT_AUDIENCE,
            issuer=settings.LMS_ISSUER,
            options={
                "require": [
                    "iss",
                    "aud",
                    "sub",
                    "course_id",
                    "purpose",
                    "iat",
                    "exp",
                    "jti",
                ],
            },
        )
    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("El login_hint recibido no es válido " "o ya expiró."),
        ) from exc

    if payload.get("purpose") != "zoom-lti-login-hint":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El propósito del login_hint no es válido.",
        )

    try:
        user_id = int(payload["sub"])
        course_id = int(payload["course_id"])
    except (
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El contenido del login_hint no es válido.",
        ) from exc

    if user_id <= 0 or course_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El login_hint contiene valores no válidos.",
        )

    return LoginHintData(
        user_id=user_id,
        course_id=course_id,
    )


def _cleanup_expired_launch_tickets(
    now: float,
) -> None:
    expired_tickets = [
        ticket for ticket, data in _launch_tickets.items() if data.expires_at <= now
    ]

    for ticket in expired_tickets:
        _launch_tickets.pop(
            ticket,
            None,
        )


def create_launch_ticket(
    user_id: int,
    course_id: int,
) -> str:
    """
    Crea un ticket opaco temporal y de un solo uso.

    El JWT principal del LMS nunca aparece en la URL.
    """

    now = time.time()
    ticket = secrets.token_urlsafe(48)

    ticket_data = LaunchTicketData(
        user_id=user_id,
        course_id=course_id,
        expires_at=(now + settings.LTI_LAUNCH_TICKET_TTL_SECONDS),
    )

    with _ticket_lock:
        _cleanup_expired_launch_tickets(
            now,
        )

        _launch_tickets[ticket] = ticket_data

    return ticket


def consume_launch_ticket(
    ticket: str,
) -> LaunchTicketData:
    """
    Consume el ticket. Después de utilizarse una vez,
    deja de existir.
    """

    if not ticket.strip():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El ticket temporal no existe.",
        )

    now = time.time()

    with _ticket_lock:
        _cleanup_expired_launch_tickets(
            now,
        )

        ticket_data = _launch_tickets.pop(
            ticket,
            None,
        )

    if not ticket_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("El enlace temporal no existe, expiró " "o ya fue utilizado."),
        )

    if ticket_data.expires_at <= now:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=("El enlace temporal para abrir Zoom expiró."),
        )

    return ticket_data


@lru_cache(maxsize=1)
def _get_zoom_tool_jwk_client() -> PyJWKClient:
    return PyJWKClient(
        settings.ZOOM_TOOL_JWKS_URL,
    )


def validate_zoom_client_assertion(
    client_assertion: str,
) -> dict[str, Any]:
    """
    Valida el JWT firmado por Zoom cuando solicita
    un bearer token para consumir servicios LTI.

    Este flujo se utiliza solamente si posteriormente
    habilitas NRPS, AGS u otros servicios Advantage.
    """

    try:
        signing_key = (
            _get_zoom_tool_jwk_client()
            .get_signing_key_from_jwt(
                client_assertion,
            )
            .key
        )

        payload = jwt.decode(
            jwt=client_assertion,
            key=signing_key,
            algorithms=[
                "RS256",
            ],
            audience=settings.lti_token_url,
            options={
                "require": [
                    "iss",
                    "sub",
                    "aud",
                    "exp",
                    "iat",
                    "jti",
                ],
            },
        )
    except (
        PyJWTError,
        PyJWKClientError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El client_assertion no es válido.",
        ) from exc

    if (
        payload.get("iss") != settings.ZOOM_LTI_CLIENT_ID
        or payload.get("sub") != settings.ZOOM_LTI_CLIENT_ID
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=("El emisor del client_assertion " "no corresponde a Zoom LTI Pro."),
        )

    return payload


def validate_requested_scopes(
    scope: str,
) -> str:
    requested_scopes = {
        current_scope.strip()
        for current_scope in scope.split()
        if current_scope.strip()
    }

    if not requested_scopes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe solicitar al menos un scope.",
        )

    invalid_scopes = requested_scopes - settings.allowed_scopes

    if invalid_scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Se solicitaron scopes no habilitados: "
                + ", ".join(
                    sorted(invalid_scopes),
                )
            ),
        )

    return " ".join(
        sorted(requested_scopes),
    )


def _cleanup_expired_service_tokens(
    now: float,
) -> None:
    expired_tokens = [
        token
        for token, data in (_service_access_tokens.items())
        if data.expires_at <= now
    ]

    for token in expired_tokens:
        _service_access_tokens.pop(
            token,
            None,
        )


def issue_service_access_token(
    scope: str,
) -> dict[str, Any]:
    now = time.time()

    access_token = secrets.token_urlsafe(
        48,
    )

    with _access_token_lock:
        _cleanup_expired_service_tokens(
            now,
        )

        _service_access_tokens[access_token] = ServiceAccessTokenData(
            scope=scope,
            expires_at=(now + settings.LTI_SERVICE_ACCESS_TOKEN_TTL_SECONDS),
        )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": (settings.LTI_SERVICE_ACCESS_TOKEN_TTL_SECONDS),
        "scope": scope,
    }
