from pydantic import BaseModel, field_validator
from typing import Optional

class LessonCreate(BaseModel):
    name: str
    order: int
    module_id: int

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre de la lección no puede estar vacío")
        return v

    @field_validator("order")
    def validate_order(cls, v):
        if v < 0:
            raise ValueError("El orden de la lección no puede ser negativo")
        return v
    
    @field_validator("module_id")
    def validate_module_id(cls, v):
        if v <= 0:
            raise ValueError("El ID del módulo debe ser un número positivo")
        return v
    
class LessonUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    module_id: Optional[int] = None

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("El nombre de la lección no puede estar vacío")
        return v

    @field_validator("order")
    def validate_order(cls, v):
        if v is not None and v < 0:
            raise ValueError("El orden de la lección no puede ser negativo")
        return v
    
    @field_validator("module_id")
    def validate_module_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El ID del módulo debe ser un número positivo")
        return v
    
class LessonResponse(BaseModel):
    id: int
    name: str
    order: int
    module_id: int
    
    class Config:
        orm_mode = True