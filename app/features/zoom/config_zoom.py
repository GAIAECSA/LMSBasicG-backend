from urllib.parse import urlparse

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ZoomLTISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # ======================================
    # ATHENA COMO PLATAFORMA LTI
    # ======================================

    LMS_ISSUER: str = "https://demo-sva.gaiaecsa.com"

    LMS_CLIENT_ID: str = "gaia-academic-lms-zoom-lti"

    LTI_DEPLOYMENT_ID: str = "deployment-gaia-1"

    LTI_KEY_ID: str = "gaia-lti-key-1"

    LTI_PUBLIC_ROOT_URL: str = "https://demo-sva.gaiaecsa.com" "/api/v1/zoom/api/v1/lti"

    LTI_PRIVATE_KEY_PATH: str = "/opt/lmsbasicg/secrets/" "gaia-lti-private.pem"

    LTI_INTERNAL_SIGNING_SECRET: str

    # ======================================
    # ZOOM COMO HERRAMIENTA EXTERNA
    # ======================================

    ZOOM_LTI_KEY: str
    ZOOM_LTI_SECRET: str

    ZOOM_TARGET_LINK_URI: str = "https://applications.zoom.us" "/lti/advantage"

    ZOOM_TOOL_REDIRECT_URI: str = (
        "https://applications.zoom.us" "/lti/advantage/oauth/complete"
    )

    ZOOM_LOGIN_INIT_URI: str

    ZOOM_TOOL_JWKS_URL: str = "https://applications.zoom.us" "/lti/advantage/jwks"

    ZOOM_RICH_OAUTH_REDIRECT_URI: str = (
        "https://applications.zoom.us" "/lti/rich/oauth/complete"
    )

    # ======================================
    # DURACIONES Y SCOPES
    # ======================================

    LTI_ALLOWED_SCOPES: str = ""

    LTI_LAUNCH_TICKET_TTL_SECONDS: int = 60
    LTI_LOGIN_HINT_TTL_SECONDS: int = 300
    LTI_SERVICE_ACCESS_TOKEN_TTL_SECONDS: int = 3600

    @field_validator(
        "LMS_ISSUER",
        "LTI_PUBLIC_ROOT_URL",
        "ZOOM_TARGET_LINK_URI",
        "ZOOM_TOOL_REDIRECT_URI",
        "ZOOM_LOGIN_INIT_URI",
        "ZOOM_TOOL_JWKS_URL",
        "ZOOM_RICH_OAUTH_REDIRECT_URI",
    )
    @classmethod
    def validate_url(
        cls,
        value: str,
    ) -> str:
        normalized_value = value.strip().rstrip("/")

        parsed_url = urlparse(
            normalized_value,
        )

        if (
            parsed_url.scheme
            not in {
                "http",
                "https",
            }
            or not parsed_url.netloc
        ):
            raise ValueError(f"La URL no es válida: {value}")

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
                "LTI_INTERNAL_SIGNING_SECRET "
                "debe contener al menos "
                "32 caracteres."
            )

        return normalized_value

    @property
    def lti_jwks_url(
        self,
    ) -> str:
        return f"{self.LTI_PUBLIC_ROOT_URL}" "/jwks"

    @property
    def lti_authorize_url(
        self,
    ) -> str:
        return f"{self.LTI_PUBLIC_ROOT_URL}" "/zoom/authorize"

    @property
    def lti_token_url(
        self,
    ) -> str:
        return f"{self.LTI_PUBLIC_ROOT_URL}" "/token"

    @property
    def allowed_scopes(
        self,
    ) -> set[str]:
        return {
            scope.strip()
            for scope in (self.LTI_ALLOWED_SCOPES.split())
            if scope.strip()
        }


settings = ZoomLTISettings()
