from urllib.parse import urlparse

from pydantic import field_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class ZoomLTISettings(BaseSettings):
    """
    Configuración de ATHENA como plataforma LTI 1.3.

    Zoom LTI Pro actúa como herramienta externa.
    ATHENA actúa como LMS o plataforma.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # Identificador estable del LMS registrado en Zoom.
    # No debe cambiar entre reinicios.
    LMS_ISSUER: str = "https://demo-sva.gaiaecsa.com"

    # URL pública externa hasta el prefijo de este router.
    # Debe coincidir con la URL accesible desde Internet.
    LTI_PUBLIC_ROOT_URL: str = (
        "https://demo-sva.gaiaecsa.com"
        "/api/v1/zoom/api/v1/lti"
    )

    LTI_DEPLOYMENT_ID: str = "deployment-gaia-1"
    LTI_KEY_ID: str = "gaia-lti-key-1"

    # Clave privada RSA persistente.
    LTI_PRIVATE_KEY_PATH: str = (
        "/opt/lmsbasicg/secrets/gaia-lti-private.pem"
    )

    # Secreto interno: no se comparte con Zoom.
    # Utilizado para proteger el login_hint.
    LTI_INTERNAL_SIGNING_SECRET: str

    # Datos copiados desde las credenciales LTI Pro de Zoom.
    ZOOM_LTI_CLIENT_ID: str

    ZOOM_TARGET_LINK_URI: str = (
        "https://applications.zoom.us/lti/advantage"
    )

    ZOOM_OAUTH_REDIRECT_URI: str = (
        "https://applications.zoom.us"
        "/lti/advantage/oauth/complete"
    )

    ZOOM_LOGIN_INIT_URI: str

    # Copiar exactamente el Public JWK URL entregado
    # por Zoom LTI Pro.
    ZOOM_TOOL_JWKS_URL: str

    # Mantener vacío para el lanzamiento básico.
    # Agregar scopes solamente cuando implementes
    # NRPS, AGS u otros servicios LTI Advantage.
    LTI_ALLOWED_SCOPES: str = ""

    LTI_LAUNCH_TICKET_TTL_SECONDS: int = 60
    LTI_LOGIN_HINT_TTL_SECONDS: int = 300
    LTI_SERVICE_ACCESS_TOKEN_TTL_SECONDS: int = 3600

    @field_validator(
        "LMS_ISSUER",
        "LTI_PUBLIC_ROOT_URL",
        "ZOOM_TARGET_LINK_URI",
        "ZOOM_OAUTH_REDIRECT_URI",
        "ZOOM_LOGIN_INIT_URI",
        "ZOOM_TOOL_JWKS_URL",
    )
    @classmethod
    def validate_url(
        cls,
        value: str,
    ) -> str:
        normalized_value = value.strip().rstrip("/")

        parsed_url = urlparse(normalized_value)

        if (
            parsed_url.scheme not in {"http", "https"}
            or not parsed_url.netloc
        ):
            raise ValueError(
                f"La URL no es válida: {value}"
            )

        return normalized_value

    @field_validator(
        "LTI_INTERNAL_SIGNING_SECRET",
    )
    @classmethod
    def validate_internal_secret(
        cls,
        value: str,
    ) -> str:
        normalized_value = value.strip()

        if len(normalized_value) < 32:
            raise ValueError(
                "LTI_INTERNAL_SIGNING_SECRET debe tener "
                "al menos 32 caracteres."
            )

        return normalized_value

    @property
    def lti_jwks_url(
        self,
    ) -> str:
        return f"{self.LTI_PUBLIC_ROOT_URL}/jwks"

    @property
    def lti_authorize_url(
        self,
    ) -> str:
        return (
            f"{self.LTI_PUBLIC_ROOT_URL}"
            "/zoom/authorize"
        )

    @property
    def lti_token_url(
        self,
    ) -> str:
        return f"{self.LTI_PUBLIC_ROOT_URL}/token"

    @property
    def allowed_scopes(
        self,
    ) -> set[str]:
        return {
            scope.strip()
            for scope in self.LTI_ALLOWED_SCOPES.split()
            if scope.strip()
        }


settings = ZoomLTISettings()