from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserLogin
from app.services import user_service
from app.utils.jwt import create_access_token

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
        "sub": db_user.id,
        "role_id": db_user.role_id
    })

    return {"access_token": token, "token_type": "bearer", "role_id": db_user.role_id}