from sqlalchemy.orm import Session

from app.models.forum_response import ForumResponse
from app.schemas.forum_response import (
    ForumResponseCreate,
    ForumResponseUpdate
)


def create(
    db: Session,
    data: ForumResponseCreate
):
    forum_response = ForumResponse(
        **data.model_dump()
    )

    db.add(forum_response)

    db.commit()
    db.refresh(forum_response)

    return forum_response


def get_by_id(
    db: Session,
    forum_response_id: int
):
    return db.query(ForumResponse).filter(
        ForumResponse.id == forum_response_id,
        ForumResponse.deleted == False
    ).first()


def get_all(db: Session):
    return db.query(ForumResponse).filter(
        ForumResponse.deleted == False
    ).all()


def get_all_by_enrollment(
    db: Session,
    enrollment_id: int
):
    return db.query(ForumResponse).filter(
        ForumResponse.enrollment_id == enrollment_id,
        ForumResponse.deleted == False
    ).all()


def get_all_by_lesson_block(
    db: Session,
    lesson_block_id: int
):
    return db.query(ForumResponse).filter(
        ForumResponse.lesson_block_id == lesson_block_id,
        ForumResponse.deleted == False
    ).all()


def get_all_replies(
    db: Session,
    forum_response_id: int
):
    return db.query(ForumResponse).filter(
        ForumResponse.forum_response_id == forum_response_id,
        ForumResponse.deleted == False
    ).all()


def update(
    db: Session,
    forum_response: ForumResponse,
    data: ForumResponseUpdate
):
    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(forum_response, key, value)

    db.commit()
    db.refresh(forum_response)

    return forum_response


def delete(
    db: Session,
    forum_response: ForumResponse
):
    forum_response.deleted = True

    db.commit()
    db.refresh(forum_response)

    return forum_response