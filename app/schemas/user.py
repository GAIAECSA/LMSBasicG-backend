from pydantic import BaseModel, field_validator, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    email: EmailStr | None
    phone_number: str | None
    departament: str | None

    @field_validator("email")
    def validate_email(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El correo electrónico no puede estar vacío")
        return v
    
    @field_validator("username")
    def validate_username(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre de usuario no puede estar vacío")
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
    username: str
    password: str