from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.utils.jwt import get_current_user

from . import zoom_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/jwks")
def jwks():
    try:
        return zoom_service.get_lti_jwks()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/zoom/launch/{course_id}")
def launch_tool(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return zoom_service.initiate_launch(db, course_id, user)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/zoom/login")
def lti_login_init(
    iss: str,
    login_hint: str,
    target_link_uri: str,
    lti_message_hint: str = None,
    client_id: str = None,
):
    # Requisito de redirección OIDC por especificación LTI 1.3
    return {"status": "ready"}


@router.get("/zoom/authorize", response_class=HTMLResponse)
def lti_authorize(
    client_id: str,
    redirect_uri: str,
    response_type: str,
    state: str,
    nonce: str,
    login_hint: str,
    lti_message_hint: str,
    db: Session = Depends(get_db),
    prompt: str = "none",
):
    try:
        return zoom_service.process_authorization(
            db=db,
            client_id=client_id,
            redirect_uri=redirect_uri,
            state=state,
            nonce=nonce,
            login_hint=login_hint,
            lti_message_hint=lti_message_hint,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/token")
def lti_token(
    grant_type: str = Form(...),
    client_assertion_type: str = Form(...),
    client_assertion: str = Form(...),
    scope: str = Form(None),
):
    try:
        return zoom_service.generate_access_token(grant_type, scope)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
