from pydantic import BaseModel, field_validator
from typing import Optional

class LessonBlockTypeCreate(BaseModel):
    name: str


    @field_validator("name")
    def name_must_not_be_blank(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Name cannot be blank")
        return v.strip()
    
class LessonBlockTypeUpdate(BaseModel):
    name: Optional[str] = None

    @field_validator("name")
    def name_must_not_be_blank(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("Name cannot be blank")
        return v.strip() if v is not None else None
    
class LessonBlockTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True