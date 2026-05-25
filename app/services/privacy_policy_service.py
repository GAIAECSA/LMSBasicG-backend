# app/services/privacy_policy_service.py
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.models.privacy_policy import PrivacyPolicy
from app.repositories import privacy_policy_repo
from app.schemas.privacy_policy import PrivacyPolicyCreate, PrivacyPolicyUpdate
from app.utils.file_upload import save_policy_privacy_file

import os
import logging

logger = logging.getLogger(__name__)


def create_privacy_policy(
    db: Session,
    data: PrivacyPolicyCreate,
    file: UploadFile | None,
):

    with db.begin():

        existing = privacy_policy_repo.get_by_version(
            db,
            data.version,
        )

        if existing:
            raise Exception("La versión ya existe")

        file_url = None

        if file:
            file_data = save_policy_privacy_file(file)
            file_url = file_data["file_url"]

        privacy_policy = PrivacyPolicy(
            **data.model_dump(exclude={"file_url"}),
            file_url=file_url,
        )

        if privacy_policy.is_active:

            active_policies = privacy_policy_repo.find_active(db)

            for pp in active_policies:
                pp.is_active = False
                privacy_policy_repo.update(db, pp)

        return privacy_policy_repo.create(
            db,
            privacy_policy,
        )


def update_privacy_policy(
    db: Session,
    privacy_policy_id: int,
    data: PrivacyPolicyUpdate,
    file: UploadFile | None,
):

    old_file_path = None

    with db.begin():

        privacy_policy = privacy_policy_repo.get_by_id(
            db,
            privacy_policy_id,
        )

        if not privacy_policy:
            raise Exception("Política no encontrada")

        update_data = data.model_dump(exclude_unset=True)

        if file:

            if privacy_policy.file_url:
                old_file_path = privacy_policy.file_url.lstrip("/")

            file_data = save_policy_privacy_file(file)

            update_data["file_url"] = file_data["file_url"]

        for key, value in update_data.items():
            setattr(privacy_policy, key, value)

        if privacy_policy.is_active:

            active_policies = privacy_policy_repo.find_active(db)

            for pp in active_policies:

                if pp.id != privacy_policy.id:
                    pp.is_active = False
                    privacy_policy_repo.update(db, pp)

        updated = privacy_policy_repo.update(
            db,
            privacy_policy,
        )

    if file and old_file_path and os.path.exists(old_file_path):

        try:
            os.remove(old_file_path)

        except Exception as e:
            logger.warning(f"No se pudo eliminar archivo viejo: {e}")

    return updated


def delete_privacy_policy(db: Session, privacy_policy_id: int):

    privacy_policy = privacy_policy_repo.get_by_id(db, privacy_policy_id)

    if not privacy_policy:
        raise Exception("Política no encontrada")

    privacy_policy.deleted = True

    return privacy_policy_repo.update(db, privacy_policy)


def get_privacy_policy(db: Session, privacy_policy_id: int):

    privacy_policy = privacy_policy_repo.get_by_id(db, privacy_policy_id)

    if not privacy_policy or privacy_policy.deleted:
        raise Exception("Política no encontrada")

    return privacy_policy


def get_all_privacy_policies(db: Session):
    return privacy_policy_repo.get_all(db)


def get_active_privacy_policy(db: Session):

    privacy_policy = privacy_policy_repo.get_active(db)

    if not privacy_policy:
        raise Exception("No existe una política activa")

    return privacy_policy
