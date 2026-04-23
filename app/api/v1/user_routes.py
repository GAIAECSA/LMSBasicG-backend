from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserLogin
from app.services import user_service
from app.utils.jwt import create_access_token, get_current_user_id


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    db_user = user_service.authenticate_user(db, data)
    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({
        "sub": str(db_user.id),
        "username": db_user.username,
        "role_id": db_user.role_id
    })

    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_current_user(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = user_service.get_current_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user