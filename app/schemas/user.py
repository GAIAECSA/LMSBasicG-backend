from pydantic import BaseModel, field_validator, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str
    phone_number: str | None
    departament: str | None

    @field_validator("email")
    def validate_email(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El correo electrónico no puede estar vacío")
        return v
    
    @field_validator("password")
    def validate_password(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("La contraseña no puede estar vacía")
        return v
    
    @field_validator("firstname")
    def validate_firstname(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        return v
    
    @field_validator("lastname")
    def validate_lastname(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El apellido no puede estar vacío")
        return v

class UserLogin(BaseModel):
    email: str
    password: str