from pydantic import BaseModel
from typing import Optional, Any, Dict
from enum import Enum
from datetime import datetime
from fastapi import Form
from app.schemas.lesson_block_type import LessonBlockTypeBasicResponse


class LessonBlockCompletitionType(str, Enum):
    VER = "VER"
    RESPONDER = "RESPONDER"
    SUBIR = "SUBIR"


class LessonBlockCreate(BaseModel):
    content: Optional[Dict[str, Any]] = None

    counts_toward_grade: bool = True
    completion_type: LessonBlockCompletitionType
    completion_value: Optional[int] = None

    order: int = 0
    default: bool = False

    lesson_id: int
    block_type_id: int

    date_available: Optional[datetime] = None

    is_active: bool = True

    @classmethod
    def as_form(
        cls,
        lesson_id: int = Form(...),
        block_type_id: int = Form(...),
        completion_type: LessonBlockCompletitionType = Form(...),
        completion_value: Optional[int] = Form(None),
        order: int = Form(0),
        default: bool = Form(False),
        counts_toward_grade: bool = Form(True),
        date_available: Optional[datetime] = Form(None),
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
            default=default,
            counts_toward_grade=counts_toward_grade,
            date_available=date_available,
            is_active=is_active,
            content=parsed_content,
        )


class LessonBlockUpdate(BaseModel):
    content: Optional[Dict[str, Any]] = None

    counts_toward_grade: Optional[bool] = None
    completion_type: Optional[LessonBlockCompletitionType] = None
    completion_value: Optional[int] = None

    order: Optional[int] = None
    default: Optional[bool] = None

    lesson_id: Optional[int] = None
    block_type_id: Optional[int] = None

    date_available: Optional[datetime] = None

    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        lesson_id: Optional[int] = Form(None),
        block_type_id: Optional[int] = Form(None),
        completion_type: Optional[LessonBlockCompletitionType] = Form(None),
        completion_value: Optional[int] = Form(None),
        order: Optional[int] = Form(None),
        default: Optional[bool] = Form(None),
        counts_toward_grade: Optional[bool] = Form(None),
        date_available: Optional[datetime] = Form(None),
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
            default=default,
            counts_toward_grade=counts_toward_grade,
            date_available=date_available,
            is_active=is_active,
            content=parsed_content,
        )


class LessonBlockResponse(BaseModel):
    id: int

    content: Dict[str, Any]

    counts_toward_grade: bool

    completion_type: Optional[LessonBlockCompletitionType]
    completion_value: Optional[int]

    order: int
    default: bool = False

    lesson_id: int
    block_type_id: int

    date_available: Optional[datetime]

    is_active: bool
    deleted: bool

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    lesson_block_type: LessonBlockTypeBasicResponse

    model_config = {"from_attributes": True}