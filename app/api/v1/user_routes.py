from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.others.auth import UserSession
from app.schemas.user import UserLogin, UserRegister, UserResponse, UserUpdate
from app.services import business_service, user_service
from app.utils.jwt import create_access_token, get_current_user, require_admin

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================================================
# CÓDIGO REFACTORIZADO Y OPTIMIZADO
# =====================================================================


@router.post("/register")
def register(
    data: UserRegister,
    db: Session = Depends(get_db),
):
    business = business_service.get_by_domain(db, data.domain)
    if not business:
        raise HTTPException(status_code=404, detail="Dominio no encontrado")
    try:
        return user_service.create_user(db, data, business_id=business.id)

    except user_service.UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    business = business_service.get_by_domain(db, data.domain)
    if not business:
        raise HTTPException(status_code=404, detail="Dominio no encontrado")

    user = user_service.authenticate_user(db, data, business.id)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token(
        {
            "sub": str(user.id),
            "username": user.username,
            "role": str(user.role_id),
            "domain": data.domain,
            "business_id": str(business.id),
        }
    )

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_current_user(
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    user = user_service.get_current_user(
        db, current_user.user_id, current_user.business_id
    )

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user


@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db), current_user: UserSession = Depends(require_admin)
):
    try:
        return user_service.get_all_users(db, current_user.business_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserSession = Depends(get_current_user),
):
    try:
        return user_service.update_user(db, user_id, data, current_user.business_id)

    except user_service.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except user_service.UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: UserSession = Depends(require_admin),
):
    try:
        user_service.delete_user(
            db=db, user_id=user_id, business_id=current_admin.business_id
        )

        return {"detail": "Usuario eliminado correctamente"}

    except user_service.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Viejos
# @router.post("/register")
# def register(data: UserCreate, db: Session = Depends(get_db)):
#   return user_service.create_user(db, data)


# @router.post("/login")
# def login(data: UserLogin, db: Session = Depends(get_db)):
#   db_user = user_service.authenticate_user(db, data)
#  db_user2 = business_service.get_by_domain(data.domain)
# if not db_user:
#    raise HTTPException(status_code=401, detail="Credenciales inválidas")

# token = create_access_token(
#   {
#      "sub": str(db_user.id),
#     "username": db_user.username,
#    "role": str(db_user.role_id),
#   "domain": data.domain,
#  "business_id": str(db_user2.id),
# }
# )

# return {"access_token": token, "token_type": "bearer"}


# @router.get("/me", response_model=UserResponse)
# def read_current_user(
#   db: Session = Depends(get_db),
#  current_user=Depends(get_current_user),
# ):
#   user = user_service.get_current_user(db, current_user["user_id"])

#  if not user:
#     raise HTTPException(status_code=404, detail="Usuario no encontrado")

# return user


# @router.get("/users", response_model=list[UserResponse])
# def get_all_users(db: Session = Depends(get_db), user=Depends(require_admin)):
#   try:
#      return user_service.get_all_users(db)
# except Exception as e:
#    raise HTTPException(status_code=400, detail=str(e))


# @router.put("/users/{user_id}", response_model=UserResponse)
# def update_user(
#   user_id: int,
#  data: UserUpdate,
# db: Session = Depends(get_db),
# user=Depends(get_current_user),
# ):
#   try:
#      return user_service.update_user(db, user_id, data)
# except Exception as e:
#    raise HTTPException(status_code=400, detail=str(e))


# @router.delete("/users/{user_id}")
# def delete_user(
#   user_id: int,
#  db: Session = Depends(get_db),
# user=Depends(require_admin),
# user2=Depends(get_current_user),
# ):
#   try:
#      user_service.delete_user(db, user_id)
#     return {"detail": "Usuario eliminado correctamente"}
# except Exception as e:
#   raise HTTPException(status_code=400, detail=str(e))
