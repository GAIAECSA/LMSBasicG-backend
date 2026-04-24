from pydantic import BaseModel, field_validator
from typing import Optional, Dict, Any


class LessonBlockTypeCreate(BaseModel):
    key: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    content_type: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

    @field_validator("key")
    def validate_key(cls, v):
        v = v.strip().lower()
        if not v:
            raise ValueError("La clave no puede estar vacía")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        return v


class LessonBlockTypeUpdate(BaseModel):
    key: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    content_type: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    @field_validator("key")
    def validate_key(cls, v):
        if v is None:
            return v
        v = v.strip().lower()
        if not v:
            raise ValueError("La clave no puede estar vacía")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        return v


class LessonBlockTypeResponse(BaseModel):
    id: int
    key: str
    name: str
    description: Optional[str]
    icon: Optional[str]
    content_type: Optional[str]
    config: Optional[Dict[str, Any]]
    is_active: bool

    class Config:
        from_attributes = True

class LessonBlockBasicResponse(BaseModel):
    id: int
    key: str

    class Config:
        from_attributes = True