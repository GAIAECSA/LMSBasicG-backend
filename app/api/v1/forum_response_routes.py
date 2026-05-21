from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.forum_response import (
    ForumResponseCreate,
    ForumResponseUpdate,
    ForumResponseResponse
)
from app.services import forum_response_service

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/",
    response_model=ForumResponseResponse
)
def create_forum_response(
    data: ForumResponseCreate,
    db: Session = Depends(get_db)
):
    try:
        return forum_response_service.create_forum_response(
            db,
            data
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[ForumResponseResponse]
)
def get_all_forum_responses(
    db: Session = Depends(get_db)
):
    try:
        return forum_response_service.get_all_forum_responses(
            db
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/{forum_response_id}",
    response_model=ForumResponseResponse
)
def get_forum_response(
    forum_response_id: int,
    db: Session = Depends(get_db)
):
    try:
        return forum_response_service.get_forum_response(
            db,
            forum_response_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get(
    "/lesson-block/{lesson_block_id}",
    response_model=list[ForumResponseResponse]
)
def get_all_by_lesson_block(
    lesson_block_id: int,
    db: Session = Depends(get_db)
):
    try:
        return forum_response_service.get_all_by_lesson_block(
            db,
            lesson_block_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/replies/{forum_response_id}",
    response_model=list[ForumResponseResponse]
)
def get_all_replies(
    forum_response_id: int,
    db: Session = Depends(get_db)
):
    try:
        return forum_response_service.get_all_replies(
            db,
            forum_response_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put(
    "/{forum_response_id}",
    response_model=ForumResponseResponse
)
def update_forum_response(
    forum_response_id: int,
    data: ForumResponseUpdate,
    db: Session = Depends(get_db)
):
    try:
        return forum_response_service.update_forum_response(
            db,
            forum_response_id,
            data
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete(
    "/{forum_response_id}",
    response_model=ForumResponseResponse
)
def delete_forum_response(
    forum_response_id: int,
    db: Session = Depends(get_db)
):
    try:
        return forum_response_service.delete_forum_response(
            db,
            forum_response_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )