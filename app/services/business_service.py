from typing import Optional

from sqlalchemy.orm import Session

from app.models.business import Business
from app.repositories import business_repo

# =====================================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================================


class BusinessNotFoundError(Exception):
    pass


# =====================================================================
# SERVICIOS
# =====================================================================


def get_by_domain(
    db: Session,
    domain: str,
) -> Optional[Business]:
    return business_repo.get_by_domain(db, domain)
