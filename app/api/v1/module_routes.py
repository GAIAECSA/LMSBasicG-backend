from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.module import ModuleCreate, ModuleUpdate, ModuleResponse
from app.services import module_service
from app.utils.jwt import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/modules", response_model=ModuleResponse)
def create_module(data: ModuleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return module_service.create_module(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/modules/{module_id}", response_model=ModuleResponse)
def update_module(module_id: int, data: ModuleUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return module_service.update_module(db, module_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/modules/{module_id}")
def delete_module(module_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        module_service.delete_module(db, module_id)
        return {"detail": "Módulo eliminado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/modules/{module_id}", response_model=ModuleResponse)
def get_module(module_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return module_service.get_module(db, module_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/courses/{course_id}/modules", response_model=list[ModuleResponse])
def get_modules_by_course(course_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return module_service.get_modules_by_course(db, course_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))