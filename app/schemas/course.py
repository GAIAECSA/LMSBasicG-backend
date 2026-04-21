from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal
from enum import Enum


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

    image_url: Optional[str] = None
    discount_price: Optional[Decimal] = Field(None, ge=0)
    currency: str = Field(default="USD", max_length=10)
    rating: Optional[Decimal] = Field(None, ge=0, le=5)
    total_students: int = Field(default=0, ge=0)

    subcategory_id: int

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
        if v is not None and v < 0:
            raise ValueError("El precio del curso no puede ser negativo")
        return v

class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[Decimal] = Field(None, ge=0)
    is_free: Optional[bool] = None
    level: Optional[CourseLevel] = None
    is_published: Optional[bool] = None
    open_enrollment: Optional[bool] = None
    duration_hours: Optional[int] = Field(None, ge=0)
    total_lessons: Optional[int] = Field(None, ge=0)

    image_url: Optional[str] = None
    discount_price: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=10)
    rating: Optional[Decimal] = Field(None, ge=0, le=5)
    total_students: Optional[int] = Field(None, ge=0)

    subcategory_id: Optional[int] = None

class CourseResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    is_free: bool
    level: CourseLevel
    is_published: bool
    duration_hours: int
    total_lessons: int

    image_url: Optional[str] = None
    discount_price: Optional[Decimal] = None
    currency: str
    published_at: Optional[str] = None
    rating: Optional[Decimal] = None
    total_students: int

    subcategory_id: int

    class Config:
        from_attributes = True