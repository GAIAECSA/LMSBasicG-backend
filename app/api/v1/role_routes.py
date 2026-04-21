from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.role import RoleCreate, RoleResponse
from app.services import role_service

router = APIRouter()

@router.post("/roles", response_model=RoleResponse)
def create_role(data: RoleCreate, db: Session = Depends(get_db)):
    try:
        return role_service.create_role(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/roles/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = role_service.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role