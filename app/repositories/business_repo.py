from sqlalchemy.orm import Session

from app.models.business import Business

# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================


def get_by_domain(db: Session, domain: str):
    return (
        db.query(Business)
        .filter(Business.domain == domain, Business.deleted == False)
        .first()
    )
