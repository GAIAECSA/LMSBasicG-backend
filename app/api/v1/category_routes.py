from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services import category_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/categories", response_model=CategoryResponse)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return category_service.create_category(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    try:
        return category_service.update_category(db, category_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category_service.delete_category(db, category_id)
        return {"detail": "Categoría eliminada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    try:
        return category_service.get_category(db, category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/categories", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    try:
        return category_service.get_all_categories(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))