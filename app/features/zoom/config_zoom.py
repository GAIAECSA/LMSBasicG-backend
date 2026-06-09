from pydantic_settings import BaseSettings


class ZoomLTISettings(BaseSettings):
    # Identificador de tu LMS (Cámbialo por tu dominio o ngrok en desarrollo)
    LMS_ISSUER: str = "https://tudominio.com"
    LMS_CLIENT_ID: str = "gaia-academic-lms"

    # Credenciales de Zoom (Extraídas de tu configuración de LTI Advantage)
    ZOOM_CLIENT_ID: str = "zZ7G4s-tR5ekhIrEyKRR5w"
    ZOOM_LTI_SECRET: str = "HGDPWtWhgr0VwtvmWKo45Z9JBZEe31uAOTTh"

    ZOOM_TARGET_LINK_URI: str = "https://applications.zoom.us/lti/advantage"
    ZOOM_OAUTH_REDIRECT_URI: str = (
        "https://applications.zoom.us/lti/advantage/oauth/complete"
    )
    ZOOM_LOGIN_INIT_URI: str = (
        "https://applications.zoom.us/lti/advantage/login/zZ7G4s-tR5ekhIrEyKRR5w"
    )


settings = ZoomLTISettings()
