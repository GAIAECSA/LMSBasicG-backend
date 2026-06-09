from urllib.parse import urlparse

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ZoomSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # ======================================
    # ZOOM SERVER-TO-SERVER OAUTH
    # ======================================

    ZOOM_ACCOUNT_ID: str
    ZOOM_CLIENT_ID: str
    ZOOM_CLIENT_SECRET: str

    # Email or Zoom user id of the real Zoom account that hosts meetings.
    ZOOM_HOST_EMAIL: str

    ZOOM_API_BASE_URL: str = "https://api.zoom.us/v2"
    ZOOM_OAUTH_TOKEN_URL: str = "https://zoom.us/oauth/token"

    # Refresh cached token a little before real expiration.
    ZOOM_TOKEN_CACHE_SKEW_SECONDS: int = 60

    # ======================================
    # DEFAULT MEETING VALUES
    # ======================================

    ZOOM_DEFAULT_TIMEZONE: str = "America/Guayaquil"
    ZOOM_DEFAULT_DURATION_MINUTES: int = 60

    # Your current LMS roles seem to use:
    # 3 = teacher, 4 = student.
    TEACHER_ROLE_ID: int = 3
    STUDENT_ROLE_ID: int = 4

    @field_validator(
        "ZOOM_ACCOUNT_ID",
        "ZOOM_CLIENT_ID",
        "ZOOM_CLIENT_SECRET",
        "ZOOM_HOST_EMAIL",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("Este valor no puede estar vacío.")

        return normalized_value

    @field_validator("ZOOM_HOST_EMAIL")
    @classmethod
    def validate_host_email(cls, value: str) -> str:
        normalized_value = value.strip()

        if "@" not in normalized_value or "." not in normalized_value:
            raise ValueError("ZOOM_HOST_EMAIL debe ser un correo válido.")

        return normalized_value

    @field_validator("ZOOM_API_BASE_URL", "ZOOM_OAUTH_TOKEN_URL")
    @classmethod
    def validate_url(cls, value: str) -> str:
        normalized_value = value.strip().rstrip("/")

        parsed_url = urlparse(normalized_value)

        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError(f"La URL no es válida: {value}")

        return normalized_value

    @field_validator(
        "ZOOM_TOKEN_CACHE_SKEW_SECONDS",
        "ZOOM_DEFAULT_DURATION_MINUTES",
        "TEACHER_ROLE_ID",
        "STUDENT_ROLE_ID",
    )
    @classmethod
    def validate_positive_integer(cls, value: int) -> int:
        if int(value) <= 0:
            raise ValueError("El valor debe ser mayor a cero.")

        return int(value)


settings = ZoomSettings()
