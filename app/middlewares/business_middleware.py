import logging

from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import SessionLocal
from app.models.business import Business

logger = logging.getLogger(__name__)


class BusinessMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        host = request.headers.get("host", "")

        if ":" in host:
            host = host.split(":")[0]

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

            request.state.business = business

        except Exception as e:

            logger.exception(
                "[BUSINESS_MIDDLEWARE] Error obteniendo empresa para host %s",
                host,
            )

            request.state.business = None

        finally:
            db.close()

        return await call_next(request)
