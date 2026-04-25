from pydantic import BaseModel
from typing import Optional, Any, Dict
from enum import Enum
from fastapi import Form
from app.schemas.lesson_block_type import LessonBlockTypeBasicResponse


class LessonBlockCompletitionType(str, Enum):
    VER = "VER"
    RESPONDER = "RESPONDER"
    SUBIR = "SUBIR"


class LessonBlockCreate(BaseModel):
    content: Optional[Dict[str, Any]] = None

    is_required: bool = True
    completion_type: LessonBlockCompletitionType
    completion_value: Optional[int] = None
    order: int = 0

    lesson_id: int
    block_type_id: int

    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        lesson_id: int = Form(...),
        block_type_id: int = Form(...),
        completion_type: LessonBlockCompletitionType = Form(...),
        completion_value: Optional[int] = Form(None),
        order: int = Form(0),
        is_required: bool = Form(True),
        is_active: bool = Form(True),
        content: Optional[str] = Form(None),
    ):
        import json

        parsed_content = json.loads(content) if content else None

        return cls(
            lesson_id=lesson_id,
            block_type_id=block_type_id,
            completion_type=completion_type,
            completion_value=completion_value,
            order=order,
            is_required=is_required,
            is_active=is_active,
            content=parsed_content,
        )

class LessonBlockUpdate(BaseModel):
    content: Optional[Dict[str, Any]] = None

    is_required: Optional[bool] = None
    completion_type: Optional[LessonBlockCompletitionType] = None
    completion_value: Optional[int] = None
    order: Optional[int] = None

    lesson_id: Optional[int] = None
    block_type_id: Optional[int] = None

    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        lesson_id: Optional[int] = Form(None),
        block_type_id: Optional[int] = Form(None),
        completion_type: Optional[LessonBlockCompletitionType] = Form(None),
        completion_value: Optional[int] = Form(None),
        order: Optional[int] = Form(None),
        is_required: Optional[bool] = Form(None),
        is_active: Optional[bool] = Form(None),
        content: Optional[str] = Form(None),
    ):
        import json

        parsed_content = json.loads(content) if content else None

        return cls(
            lesson_id=lesson_id,
            block_type_id=block_type_id,
            completion_type=completion_type,
            completion_value=completion_value,
            order=order,
            is_required=is_required,
            is_active=is_active,
            content=parsed_content,
        )

class LessonBlockResponse(BaseModel):
    id: int
    content: Dict[str, Any]
    
    is_required: bool
    completion_type: LessonBlockCompletitionType
    completion_value: Optional[int]
    order: int

    lesson_id: int

    is_active: bool

    lesson_block_type: LessonBlockTypeBasicResponse

    class Config:
        from_attributes = True
