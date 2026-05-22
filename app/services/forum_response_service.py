from sqlalchemy.orm import Session

from app.repositories import forum_response_repo
from app.schemas.forum_response import ForumResponseCreate, ForumResponseUpdate


def create_forum_response(db: Session, data: ForumResponseCreate):
    return forum_response_repo.create(db, data)


def get_forum_response(db: Session, forum_response_id: int):
    forum_response = forum_response_repo.get_by_id(db, forum_response_id)

    if not forum_response:
        raise Exception("Forum response not found")

    return forum_response


def get_all_forum_responses(db: Session):
    return forum_response_repo.get_all(db)


def get_all_by_enrollment(db: Session, enrollment_id: int):
    return forum_response_repo.get_all_by_enrollment(db, enrollment_id)


def get_all_by_lesson_block(db: Session, lesson_block_id: int):
    return forum_response_repo.get_all_by_lesson_block(db, lesson_block_id)


def get_all_replies(db: Session, forum_response_id: int):
    return forum_response_repo.get_all_replies(db, forum_response_id)


def update_forum_response(
    db: Session, forum_response_id: int, data: ForumResponseUpdate
):
    forum_response = get_forum_response(db, forum_response_id)

    return forum_response_repo.update(db, forum_response, data)


def delete_forum_response(db: Session, forum_response_id: int):
    forum_response = get_forum_response(db, forum_response_id)

    return forum_response_repo.delete(db, forum_response)
