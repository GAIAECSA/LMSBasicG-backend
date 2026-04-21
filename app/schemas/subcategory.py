from pydantic import BaseModel, field_validator
from typing import Optional

class SubcategoryCreate(BaseModel):
    
    name: str

    category_id: int

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre de la subcategoría no puede estar vacío")
        return v
    
    @field_validator("category_id")
    def validate_category_id(cls, v):
        if v <= 0:
            raise ValueError("El ID de la categoría debe ser un número positivo")
        return v

class SubcategoryUpdate(BaseModel):

    name: Optional[str] = None

    category_id: Optional[int] = None

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("El nombre de la subcategoría no puede estar vacío")
        return v
    
    @field_validator("category_id")
    def validate_category_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El ID de la categoría debe ser un número positivo")
        return v

class SubcategoryResponse(BaseModel):
    id: int
    name: str
    category_id: int

    class Config:
        from_attributes = True