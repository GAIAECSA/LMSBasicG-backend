import urllib.parse
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

# TODO: Ajusta estas importaciones a la estructura real de tu aplicación
from app.db.session import get_db
from app.models.enrollment import Enrollment
from app.models.user import User
from app.utils.jwt import (
    get_current_user,
)  # Dependencia que recupera el usuario logueado

# Importaciones de seguridad y configuración local
from .config_zoom import settings
from .security_zoom import get_jwks, sign_jwt

router = APIRouter(prefix="/api/v1/lti", tags=["Zoom LTI Integration"])


@router.get("/jwks")
def jwks():
    """Expone la clave pública para que Zoom valide nuestras firmas"""
    return get_jwks()


@router.get("/zoom/launch/{course_id}")
def launch_tool(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Punto de partida en el LMS. Valida que el usuario tenga matrícula activa
    y lo redirige al inicio de sesión de Zoom.
    """
    # Verificamos si existe la matrícula para el usuario actual en el curso especificado
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id,
            Enrollment.deleted == False,
        )
        .first()
    )

    if not enrollment:
        raise HTTPException(
            status_code=403, detail="No tienes una matrícula activa en este curso."
        )

    # Pasamos el ID del usuario como login_hint y el ID del curso como lti_message_hint
    params = {
        "iss": settings.LMS_ISSUER,
        "target_link_uri": settings.ZOOM_TARGET_LINK_URI,
        "login_hint": str(current_user.id),
        "lti_message_hint": str(course_id),
        "client_id": settings.ZOOM_CLIENT_ID,
    }

    query_string = urllib.parse.urlencode(params)
    zoom_login_url = f"{settings.ZOOM_LOGIN_INIT_URI}?{query_string}"

    return RedirectResponse(url=zoom_login_url)


@router.get("/zoom/login")
def lti_login_init(
    iss: str,
    login_hint: str,
    target_link_uri: str,
    lti_message_hint: str = None,
    client_id: str = None,
):
    """Requisito del estándar OIDC para flujos iniciados desde la herramienta externa."""
    pass


@router.get("/zoom/authorize", response_class=HTMLResponse)
def lti_authorize(
    client_id: str,
    redirect_uri: str,
    response_type: str,
    state: str,
    nonce: str,
    login_hint: str,
    lti_message_hint: str,
    db: Session = Depends(get_db),
    prompt: str = "none",
):
    """
    Zoom nos devuelve el control aquí. Buscamos la matrícula real
    para armar los claims de identidad y rol (Docente vs Estudiante).
    """
    if client_id != settings.ZOOM_CLIENT_ID:
        raise HTTPException(status_code=400, detail="Client ID mismatch")

    # Recuperamos la matrícula uniendo al usuario para extraer sus datos personales
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == int(login_hint),
            Enrollment.course_id == int(lti_message_hint),
            Enrollment.deleted == False,
        )
        .first()
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Matrícula no encontrada para el flujo de autenticación.",
        )

    # Mapeo de roles de acuerdo al diseño de tu base de datos (3 Docente, 4 Estudiante)
    if enrollment.role_id == 3:
        lti_roles = ["http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor"]
    elif enrollment.role_id == 4:
        lti_roles = ["http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"]
    else:
        lti_roles = ["http://purl.imsglobal.org/vocab/lis/v2/membership#Member"]

    now = datetime.now(timezone.utc)

    # Construcción del Payload LTI 1.3 estructurado con la información del modelo User
    payload = {
        "iss": settings.LMS_ISSUER,
        "aud": client_id,
        "exp": (now + timedelta(minutes=5)).timestamp(),
        "iat": now.timestamp(),
        "sub": str(enrollment.user.id),
        "nonce": nonce,
        # Información de perfil del usuario extraída de tu tabla 'users'
        "name": f"{enrollment.user.firstname} {enrollment.user.lastname}",
        "given_name": enrollment.user.firstname,
        "family_name": enrollment.user.lastname,
        "email": enrollment.user.email,
        # Claims requeridos por LTI Advantage 1.3
        "https://purl.imsglobal.org/spec/lti/claim/message_type": "LtiResourceLinkRequest",
        "https://purl.imsglobal.org/spec/lti/claim/version": "1.3.0",
        "https://purl.imsglobal.org/spec/lti/claim/deployment_id": "deployment-gaia-1",
        "https://purl.imsglobal.org/spec/lti/claim/target_link_uri": settings.ZOOM_TARGET_LINK_URI,
        "https://purl.imsglobal.org/spec/lti/claim/resource_link": {
            "id": f"resource_course_{enrollment.course_id}",
            "title": "Sala de Videoconferencia Zoom",
        },
        "https://purl.imsglobal.org/spec/lti/claim/roles": lti_roles,
        "https://purl.imsglobal.org/spec/lti/claim/context": {
            "id": str(enrollment.course_id),
            "type": ["CourseSection"],
            "title": f"Curso ID {enrollment.course_id}",
        },
        "https://purl.imsglobal.org/spec/lti/claim/tool_platform": {
            "guid": "gaia_academic_platform",
            "name": "Gaia Academic LMS",
        },
    }

    id_token = sign_jwt(payload)

    # LTI exige que el envío del token hacia la herramienta destino se realice mediante un POST en el cliente
    html_form = f"""
    <html>
        <head><title>Cargando Aula Virtual...</title></head>
        <body onload="document.ltiLaunchForm.submit();" style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h2>Conectando con Zoom de forma segura...</h2>
            <form name="ltiLaunchForm" method="POST" action="{redirect_uri}">
                <input type="hidden" name="id_token" value="{id_token}" />
                <input type="hidden" name="state" value="{state}" />
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_form)


@router.post("/token")
def lti_token(
    grant_type: str = Form(...),
    client_assertion_type: str = Form(...),
    client_assertion: str = Form(...),
    scope: str = Form(None),
):
    """Entrega tokens bearer temporales si Zoom decide consultar servicios de backend del LMS."""
    if grant_type != "client_credentials":
        raise HTTPException(status_code=400, detail="Invalid grant_type")

    access_token = str(uuid.uuid4())

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": scope,
    }
