from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.forum_response import (
    ForumResponseCreate,
    ForumResponseResponse,
    ForumResponseUpdate,
)
from app.schemas.others.auth import UserSession
from app.services import forum_response_service
from app.utils.jwt import get_current_user, require_admin

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ForumResponseResponse)
def create_forum_response(
    data: ForumResponseCreate,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return forum_response_service.create_forum_response(
            db, data, current_user.business_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=list[ForumResponseResponse])
def get_all_forum_responses(
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return forum_response_service.get_all_forum_responses(
            db, current_user.business_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{forum_response_id}", response_model=ForumResponseResponse)
def get_forum_response(
    forum_response_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return forum_response_service.get_forum_response(
            db, forum_response_id, current_user.business_id
        )
    except forum_response_service.ForumResponseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get(
    "/lesson-block/{lesson_block_id}", response_model=list[ForumResponseResponse]
)
def get_all_by_lesson_block(
    lesson_block_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return forum_response_service.get_all_by_lesson_block(
            db, lesson_block_id, current_user.business_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/enrollment/{enrollment_id}", response_model=list[ForumResponseResponse])
def get_all_by_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return forum_response_service.get_all_by_enrollment(
            db, enrollment_id, current_user.business_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/replies/{forum_response_id}", response_model=list[ForumResponseResponse])
def get_all_replies(
    forum_response_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return forum_response_service.get_all_replies(
            db, forum_response_id, current_user.business_id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/{forum_response_id}", response_model=ForumResponseResponse)
def update_forum_response(
    forum_response_id: int,
    data: ForumResponseUpdate,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return forum_response_service.update_forum_response(
            db, forum_response_id, data, current_user.business_id
        )
    except forum_response_service.ForumResponseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{forum_response_id}")
def delete_forum_response(
    forum_response_id: int,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(
        get_current_user
    ),  # Cambiar a require_admin si solo administradores pueden borrar
):
    try:
        forum_response_service.delete_forum_response(
            db, forum_response_id, current_user.business_id
        )
        return {"detail": "Respuesta de foro eliminada"}
    except forum_response_service.ForumResponseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


"""


@router.post("/", response_model=ForumResponseResponse)
def create_forum_response(data: ForumResponseCreate, db: Session = Depends(get_db)):
    try:
        return forum_response_service.create_forum_response(db, data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ForumResponseResponse])
def get_all_forum_responses(db: Session = Depends(get_db)):
    try:
        return forum_response_service.get_all_forum_responses(db)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{forum_response_id}", response_model=ForumResponseResponse)
def get_forum_response(forum_response_id: int, db: Session = Depends(get_db)):
    try:
        return forum_response_service.get_forum_response(db, forum_response_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/lesson-block/{lesson_block_id}", response_model=list[ForumResponseResponse]
)
def get_all_by_lesson_block(lesson_block_id: int, db: Session = Depends(get_db)):
    try:
        return forum_response_service.get_all_by_lesson_block(db, lesson_block_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/replies/{forum_response_id}", response_model=list[ForumResponseResponse])
def get_all_replies(forum_response_id: int, db: Session = Depends(get_db)):
    try:
        return forum_response_service.get_all_replies(db, forum_response_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{forum_response_id}", response_model=ForumResponseResponse)
def update_forum_response(
    forum_response_id: int, data: ForumResponseUpdate, db: Session = Depends(get_db)
):
    try:
        return forum_response_service.update_forum_response(db, forum_response_id, data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
"""
