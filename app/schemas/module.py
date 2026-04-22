from pydantic import BaseModel, field_validator
from typing import Optional

class ModuleCreate(BaseModel):
    name: str
    order: int
    course_id: int

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre del módulo no puede estar vacío")
        return v

    @field_validator("order")
    def validate_order(cls, v):
        if v < 0:
            raise ValueError("El orden del módulo no puede ser negativo")
        return v
    
    @field_validator("course_id")
    def validate_course_id(cls, v):
        if v <= 0:
            raise ValueError("El ID del curso debe ser un número positivo")
        return v
    
class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("El nombre del módulo no puede estar vacío")
        return v

    @field_validator("order")
    def validate_order(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El orden del módulo no puede ser cero o negativo")
        return v

class ModuleResponse(BaseModel):
    id: int
    name: str
    order: int
    course_id: int

    class Config:
        from_attributes = True