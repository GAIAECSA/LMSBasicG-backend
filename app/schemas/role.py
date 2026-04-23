from pydantic import BaseModel, field_validator

class RoleCreate(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre del rol no puede estar vacío")
        return v

class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class RoleBasicResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True