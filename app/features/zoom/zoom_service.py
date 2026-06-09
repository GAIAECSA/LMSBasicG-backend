import urllib.parse
import uuid
from datetime import datetime, timedelta, timezone

from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload

from app.models.enrollment import Enrollment

from .config_zoom import settings
from .security_zoom import get_jwks, sign_jwt


def get_lti_jwks() -> dict:
    return get_jwks()


def initiate_launch(db: Session, course_id: int, user: dict) -> RedirectResponse:
    # Usamos db.begin() para manejar la transacción de lectura de forma consistente
    with db.begin():
        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.user_id
                == user["user_id"],  # Ajustado para leer el diccionario de tu JWT
                Enrollment.course_id == course_id,
                Enrollment.deleted == False,
            )
            .first()
        )

        if not enrollment:
            raise Exception("No tienes una matrícula activa en este curso.")

    params = {
        "iss": settings.LMS_ISSUER,
        "target_link_uri": settings.ZOOM_TARGET_LINK_URI,
        "login_hint": str(user["user_id"]),
        "lti_message_hint": str(course_id),
        "client_id": settings.ZOOM_CLIENT_ID,
    }
    query_string = urllib.parse.urlencode(params)
    return RedirectResponse(url=f"{settings.ZOOM_LOGIN_INIT_URI}?{query_string}")


def process_authorization(
    db: Session,
    client_id: str,
    redirect_uri: str,
    state: str,
    nonce: str,
    login_hint: str,
    lti_message_hint: str,
) -> HTMLResponse:
    if client_id != settings.ZOOM_CLIENT_ID:
        raise Exception("Client ID mismatch")

    # Mantenemos el joinedload(Enrollment.user) aquí dentro de db.begin() porque el endpoint
    # /authorize es llamado por Zoom asíncronamente y necesitamos reconstruir el perfil completo (nombre, email)
    with db.begin():
        enrollment = (
            db.query(Enrollment)
            .options(joinedload(Enrollment.user))
            .filter(
                Enrollment.user_id == int(login_hint),
                Enrollment.course_id == int(lti_message_hint),
                Enrollment.deleted == False,
            )
            .first()
        )

        if not enrollment:
            raise Exception("Matrícula no encontrada para el flujo de autenticación.")

        if enrollment.role_id == 3:
            lti_roles = ["http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor"]
        elif enrollment.role_id == 4:
            lti_roles = ["http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"]
        else:
            lti_roles = ["http://purl.imsglobal.org/vocab/lis/v2/membership#Member"]

        user_id = enrollment.user.id
        full_name = f"{enrollment.user.firstname} {enrollment.user.lastname}"
        firstname = enrollment.user.firstname
        lastname = enrollment.user.lastname
        email = enrollment.user.email

    now = datetime.now(timezone.utc)
    payload = {
        "iss": settings.LMS_ISSUER,
        "aud": client_id,
        "exp": (now + timedelta(minutes=5)).timestamp(),
        "iat": now.timestamp(),
        "sub": str(user_id),
        "nonce": nonce,
        "name": full_name,
        "given_name": firstname,
        "family_name": lastname,
        "email": email,
        "https://purl.imsglobal.org/spec/lti/claim/message_type": "LtiResourceLinkRequest",
        "https://purl.imsglobal.org/spec/lti/claim/version": "1.3.0",
        "https://purl.imsglobal.org/spec/lti/claim/deployment_id": "deployment-gaia-1",
        "https://purl.imsglobal.org/spec/lti/claim/target_link_uri": settings.ZOOM_TARGET_LINK_URI,
        "https://purl.imsglobal.org/spec/lti/claim/resource_link": {
            "id": f"resource_course_{lti_message_hint}",
            "title": "Sala de Videoconferencia Zoom",
        },
        "https://purl.imsglobal.org/spec/lti/claim/roles": lti_roles,
        "https://purl.imsglobal.org/spec/lti/claim/context": {
            "id": str(lti_message_hint),
            "type": ["CourseSection"],
            "title": f"Curso ID {lti_message_hint}",
        },
        "https://purl.imsglobal.org/spec/lti/claim/tool_platform": {
            "guid": "gaia_academic_platform",
            "name": "Gaia Academic LMS",
        },
    }

    id_token = sign_jwt(payload)

    html_form = f"""
    <html>
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


def generate_access_token(grant_type: str, scope: str = None) -> dict:
    if grant_type != "client_credentials":
        raise Exception("Invalid grant_type")

    return {
        "access_token": str(uuid.uuid4()),
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": scope,
    }
