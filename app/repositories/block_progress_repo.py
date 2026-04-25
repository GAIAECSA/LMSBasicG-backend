from sqlalchemy.orm import Session, joinedload
from app.models.block_progress import BlockProgress

def create(db: Session, progress: BlockProgress):
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress

def update(db: Session, progress: BlockProgress):
    db.merge(progress)
    db.commit()
    db.refresh(progress)
    return progress

def delete(db: Session, progress: BlockProgress):
    progress.deleted = True
    db.merge(progress)
    db.commit()
    return progress

def get_by_id(db: Session, progress_id: int):
    return db.query(BlockProgress)\
        .filter(
            BlockProgress.id == progress_id,
            BlockProgress.deleted == False
        )\
        .first()

def get_by_enrollment(db: Session, enrollment_id: int):
    return db.query(BlockProgress)\
        .filter(
            BlockProgress.enrollment_id == enrollment_id,
            BlockProgress.deleted == False
        )\
        .order_by(BlockProgress.lesson_block_id)\
        .all()



