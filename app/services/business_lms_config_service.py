from sqlalchemy.orm import Session

from app.repositories import business_lms_config_repo


def get_enabled_configs(
    db: Session,
    business_id: int,
):
    configs = business_lms_config_repo.get_enabled_configs(
        db,
        business_id,
    )

    return [
        {
            "id": cfg.lms_config.id,
            "name": cfg.lms_config.name,
            "description": cfg.lms_config.description,
            "category": getattr(cfg.lms_config, "category", None),
            "config": cfg.config,
        }
        for cfg in configs
    ]
