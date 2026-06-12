import logging

from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import SessionLocal
from app.models.business import Business
from app.models.business_lms_config import BusinessLmsConfig

logger = logging.getLogger(__name__)


class BusinessMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        host = request.headers.get("host", "")

        if ":" in host:
            host = host.split(":")[0]

        logger.info(
            "[BUSINESS_MIDDLEWARE] Host recibido: %s",
            host,
        )

        db = SessionLocal()

        try:

            business = (
                db.query(Business)
                .filter(
                    Business.domain == host,
                    Business.is_active == True,
                    Business.deleted == False,
                )
                .first()
            )

            if business:
                logger.info(
                    "[BUSINESS_MIDDLEWARE] Empresa encontrada -> id=%s nombre=%s dominio=%s",
                    business.id,
                    business.name,
                    business.domain,
                )
            else:
                logger.warning(
                    "[BUSINESS_MIDDLEWARE] No existe empresa para el host: %s",
                    host,
                )

            request.state.business = business

            if business:

                configs = (
                    db.query(BusinessLmsConfig)
                    .filter(
                        BusinessLmsConfig.business_id == business.id,
                        BusinessLmsConfig.is_active == True,
                        BusinessLmsConfig.deleted == False,
                    )
                    .all()
                )

                logger.info(
                    "[BUSINESS_MIDDLEWARE] Módulos habilitados encontrados: %s",
                    len(configs),
                )

                request.state.enabled_modules = [
                    {
                        "id": cfg.lms_config.id,
                        "name": cfg.lms_config.name,
                        "description": cfg.lms_config.description,
                        "config": cfg.config,
                    }
                    for cfg in configs
                ]

            else:

                request.state.enabled_modules = []

        finally:
            db.close()

        return await call_next(request)
