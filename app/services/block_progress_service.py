from sqlalchemy.orm import Session
from datetime import datetime

from app.models.block_progress import BlockProgress
from app.repositories import block_progress_repo
from app.schemas.block_progress import BlockProgressCreate, BlockProgressUpdate


def create_block_progress(db: Session, data: BlockProgressCreate):
    existing = block_progress_repo.get_by_enrollment_block(
        db, data.enrollment_id, data.lesson_block_id
    )

    if existing:
        raise Exception("El progreso ya existe")

    progress = BlockProgress(**data.model_dump())

    if not progress.started_at:
        progress.started_at = datetime.utcnow()

    return block_progress_repo.create(db, progress)


def get_block_progress(db: Session, progress_id: int):
    progress = block_progress_repo.get_by_id(db, progress_id)

    if not progress:
        raise Exception("Progreso no encontrado")

    return progress


def get_progress_by_enrollment(db: Session, enrollment_id: int):
    return block_progress_repo.get_by_enrollment(db, enrollment_id)


def update_block_progress(db: Session, progress_id: int, data: BlockProgressUpdate):
    progress = block_progress_repo.get_by_id(db, progress_id)

    if not progress:
        raise Exception("Progreso no encontrado")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(progress, key, value)

    if update_data.get("is_completed") is True and not progress.completed_at:
        progress.completed_at = datetime.utcnow()

    return block_progress_repo.update(db, progress)


def complete_block(db: Session, enrollment_id: int, lesson_block_id: int):
    progress = block_progress_repo.get_by_enrollment_block(
        db, enrollment_id, lesson_block_id
    )

    if not progress:
        progress = BlockProgress(
            enrollment_id=enrollment_id,
            lesson_block_id=lesson_block_id,
            is_completed=True,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
        )
        return block_progress_repo.create(db, progress)

    progress.is_completed = True
    progress.completed_at = datetime.utcnow()

    return block_progress_repo.update(db, progress)

def delete_block_progress(db: Session, progress_id: int):
    progress = block_progress_repo.get_by_id(db, progress_id)

    if not progress:
        raise Exception("Progreso no encontrado")

    return block_progress_repo.delete(db, progress)