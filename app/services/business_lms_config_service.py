from sqlalchemy.orm import Session

from app.repositories import business_lms_config_repo


def get_enabled_configs(
    db: Session,
    domain: str,
):
    configs = business_lms_config_repo.get_enabled_configs(
        db,
        domain,
    )

    return [
        {
            "id": cfg.lms_config.id,
            "name": cfg.lms_config.name,
            "description": cfg.lms_config.description,
            "config": cfg.config,
        }
        for cfg in configs
    ]
