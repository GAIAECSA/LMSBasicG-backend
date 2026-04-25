from sqlalchemy.orm import Session, joinedload
from app.models.progress import Progress

def create(db: Session, progress: Progress):
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress

def update(db: Session, progress: Progress):
    db.merge(progress)
    db.commit()
    db.refresh(progress)
    return progress

def delete(db: Session, progress: Progress):
    progress.deleted = True
    db.merge(progress)
    db.commit()
    return progress

def get_by_id(db: Session, progress_id: int):
    return db.query(Progress)\
        .options(
            joinedload(Progress.lesson_block),
            joinedload(Progress.enrollment)
        )\
        .filter(
            Progress.id == progress_id,
            Progress.deleted == False
        )\
        .first()

def get_by_enrollment(db: Session, enrollment_id: int):
    return db.query(Progress)\
        .options(
            joinedload(Progress.lesson_block)
        )\
        .filter(
            Progress.enrollment_id == enrollment_id,
            Progress.deleted == False
        )\
        .order_by(Progress.lesson_block_id)\
        .all()



