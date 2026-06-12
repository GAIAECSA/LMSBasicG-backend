from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.business_lms_config import BusinessLmsConfig


def get_enabled_configs(
    db: Session,
    domain: str,
):
    return (
        db.query(BusinessLmsConfig)
        .join(
            Business,
            Business.id == BusinessLmsConfig.business_id,
        )
        .filter(
            Business.domain == domain,
            Business.is_active == True,
            Business.deleted == False,
            BusinessLmsConfig.is_active == True,
            BusinessLmsConfig.deleted == False,
        )
        .all()
    )
