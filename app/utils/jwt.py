from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.schemas.others.auth import UserSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSession:
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    try:
        return UserSession(
            user_id=int(payload.get("sub")),
            role_id=int(payload.get("role")),
            domain=payload.get("domain"),
            business_id=int(payload.get("business_id")),
        )
    except (TypeError, ValueError, AttributeError):
        raise HTTPException(status_code=401, detail="Token con formato inválido")


def require_admin(user: UserSession = Depends(get_current_user)):
    if user.role_id != 1:
        raise HTTPException(status_code=403, detail="No autorizado")
    return user
