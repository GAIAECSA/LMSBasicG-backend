from pydantic import BaseModel, field_validator
from typing import Optional

class CategoryCreate(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre de la categoría no puede estar vacío")
        return v

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("El nombre de la categoría no puede estar vacío")
        return v

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True