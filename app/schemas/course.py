# app/schemas/course.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal
from enum import Enum
from fastapi import Form

class CourseLevel(str, Enum):
    PRINCIPIANTE = "PRINCIPIANTE"
    INTERMEDIO = "INTERMEDIO"
    AVANZADO = "AVANZADO"

class CourseCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    price: Decimal = Field(..., ge=0)
    is_free: bool
    level: CourseLevel
    is_published: bool
    open_enrollment: bool
    duration_hours: int = Field(..., ge=0)
    total_lessons: int = Field(..., ge=0)
    subcategory_id: int
    discount_price: Optional[Decimal] = Field(None, ge=0)

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
        price: Decimal = Form(...),
        is_free: bool = Form(...),
        level: CourseLevel = Form(...),
        is_published: bool = Form(...),
        open_enrollment: bool = Form(...),
        duration_hours: int = Form(...),
        total_lessons: int = Form(...),
        subcategory_id: int = Form(...),
        discount_price: Optional[Decimal] = Form(None),
    ):
        return cls(
            name=name,
            description=description,
            price=price,
            is_free=is_free,
            level=level,
            is_published=is_published,
            open_enrollment=open_enrollment,
            duration_hours=duration_hours,
            total_lessons=total_lessons,
            subcategory_id=subcategory_id,
            discount_price=discount_price,
        )

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre del curso no puede estar vacío")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("La descripción del curso no puede estar vacía")
        return v

    @field_validator("price")
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    is_free: Optional[bool] = None
    level: Optional[CourseLevel] = None
    is_published: Optional[bool] = None
    open_enrollment: Optional[bool] = None
    duration_hours: Optional[int] = None
    total_lessons: Optional[int] = None
    subcategory_id: Optional[int] = None
    discount_price: Optional[Decimal] = None

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        price: Optional[Decimal] = Form(None),
        is_free: Optional[bool] = Form(None),
        level: Optional[CourseLevel] = Form(None),
        is_published: Optional[bool] = Form(None),
        open_enrollment: Optional[bool] = Form(None),
        duration_hours: Optional[int] = Form(None),
        total_lessons: Optional[int] = Form(None),
        subcategory_id: Optional[int] = Form(None),
        discount_price: Optional[Decimal] = Form(None),
    ):
        return cls(
            name=name,
            description=description,
            price=price,
            is_free=is_free,
            level=level,
            is_published=is_published,
            open_enrollment=open_enrollment,
            duration_hours=duration_hours,
            total_lessons=total_lessons,
            subcategory_id=subcategory_id,
            discount_price=discount_price,
        )

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("El nombre no puede estar vacío")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("La descripción no puede estar vacía")
        return v

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v

class CourseResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    is_free: bool
    level: CourseLevel
    is_published: bool
    open_enrollment: bool
    duration_hours: int
    total_lessons: int
    subcategory_id: int

    image_url: Optional[str] = None
    discount_price: Optional[Decimal] = None
    currency: Optional[str] = "USD"
    rating: Optional[Decimal] = None
    total_students: Optional[int] = 0

    class Config:
        from_attributes = True