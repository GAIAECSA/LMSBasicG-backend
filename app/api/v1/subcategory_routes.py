from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.subcategory import SubcategoryCreate, SubcategoryUpdate, SubcategoryResponse
from app.services import subcategory_service
from app.utils.jwt import require_admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/subcategories", response_model=SubcategoryResponse)
def create_subcategory(data: SubcategoryCreate, db: Session = Depends(get_db), user = Depends(require_admin)):
    try:
        return subcategory_service.create_subcategory(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/subcategories/{subcategory_id}", response_model=SubcategoryResponse)
def update_subcategory(subcategory_id: int, data: SubcategoryUpdate, db: Session = Depends(get_db), user = Depends(require_admin)):
    try:
        return subcategory_service.update_subcategory(db, subcategory_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/subcategories/{subcategory_id}")
def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db), user = Depends(require_admin)):
    try:
        subcategory_service.delete_subcategory(db, subcategory_id)
        return {"detail": "Subcategoría eliminada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/subcategories/{subcategory_id}", response_model=SubcategoryResponse)
def get_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    try:
        return subcategory_service.get_subcategory(db, subcategory_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/categories/{category_id}/subcategories", response_model=list[SubcategoryResponse])
def get_subcategories_by_category(category_id: int, db: Session = Depends(get_db)):
    try:
        return subcategory_service.get_subcategories_by_category(db, category_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/subcategories", response_model=list[SubcategoryResponse])
def get_all_subcategories(db: Session = Depends(get_db)):
    try:
        return subcategory_service.get_all_subcategories(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))