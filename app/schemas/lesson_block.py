from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict
from enum import Enum
from app.schemas.lesson_block_type import LessonBlockBasicResponse

class LessonBlockCompletitionType(str, Enum):
    VER = "VER"
    RESPONDER = "RESPONDER"
    SUBIR = "SUBIR"

class LessonBlockCreate(BaseModel):
    
    content: Dict[str, Any]

    is_required: Optional[bool] = True
    completion_type: LessonBlockCompletitionType
    completion_value: Optional[int] = None
    order: Optional[int] = 0

    lesson_id: int
    block_type_id: int

    is_active: Optional[bool] = True

class LessonBlockUpdate(BaseModel):
    
    content: Optional[Dict[str, Any]] = None

    is_required: Optional[bool] = None
    completion_type: LessonBlockCompletitionType
    completion_value: Optional[int] = None
    order: Optional[int] = None

    lesson_id: Optional[int] = None
    block_type_id: Optional[int] = None

    is_active: Optional[bool] = None

class LessonBlockResponse(BaseModel):
    id: int
    content: Dict[str, Any]
    
    is_required: bool
    completion_type: LessonBlockCompletitionType
    completion_value: Optional[int]
    order: int

    lesson_id: int

    is_active: bool

    lesson_block_type: LessonBlockBasicResponse

    class Config:
        from_attributes = True
