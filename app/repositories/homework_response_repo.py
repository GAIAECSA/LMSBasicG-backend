from sqlalchemy.orm import Session

from app.models.homework_response import HomeworkResponse


def create(db: Session, homework_response: HomeworkResponse):
    db.add(homework_response)
    db.commit()
    db.refresh(homework_response)
    return homework_response


def update(db: Session, homework_response: HomeworkResponse):
    db.merge(homework_response)
    db.commit()
    db.refresh(homework_response)
    return homework_response


def delete(db: Session, homework_response: HomeworkResponse):
    homework_response.deleted = True
    db.merge(homework_response)
    db.commit()
    return homework_response


def get_by_id(db: Session, homework_response_id: int):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.id == homework_response_id,
            HomeworkResponse.deleted == False
        )
        .first()
    )


def get_all_by_enrollment(db: Session, enrollment_id: int):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.deleted == False,
            HomeworkResponse.enrollment_id == enrollment_id
        )
        .all()
    )


def get_all_by_lesson_block(db: Session, lesson_block_id: int):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.deleted == False,
            HomeworkResponse.lesson_block_id == lesson_block_id
        )
        .all()
    )


def get_by_enrollment_and_lesson_block(
    db: Session,
    enrollment_id: int,
    lesson_block_id: int
):
    return (
        db.query(HomeworkResponse)
        .filter(
            HomeworkResponse.deleted == False,
            HomeworkResponse.enrollment_id == enrollment_id,
            HomeworkResponse.lesson_block_id == lesson_block_id
        )
        .first()
    )