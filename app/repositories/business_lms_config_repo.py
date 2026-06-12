from sqlalchemy.orm import Session

from app.models.business_lms_config import BusinessLmsConfig


def get_enabled_configs(
    db: Session,
    business_id: int,
):
    return (
        db.query(BusinessLmsConfig)
        .filter(
            BusinessLmsConfig.business_id == business_id,
            BusinessLmsConfig.is_active == True,
            BusinessLmsConfig.deleted == False,
        )
        .all()
    )
