from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, ValidationInfo, field_validator


class UserCreate(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    idnumber: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    departament: Optional[str] = None

    @field_validator(
        "username", "password", "firstname", "lastname", "email", check_fields=False
    )
    @classmethod
    def validate_not_empty(cls, v: Optional[str], info: ValidationInfo):
        if v is None:
            return v

        v = v.strip()
        if not v:
            mensajes = {
                "username": "El nombre de usuario",
                "password": "La contraseña",
                "firstname": "El nombre",
                "lastname": "El apellido",
                "email": "El correo electrónico",
            }
            campo = mensajes.get(info.field_name, "El campo")
            raise ValueError(f"{campo} no puede estar vacío")

        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: Optional[str]):
        if v is None:
            return v

        v = v.strip()
        if not v:
            raise ValueError("El número de teléfono no puede estar vacío")

        check_val = v.replace("+", "", 1) if v.startswith("+") else v
        if not check_val.isdigit():
            raise ValueError(
                "El número de teléfono solo debe contener números y opcionalmente un '+' al inicio"
            )

        return v


class UserRegister(UserCreate):
    domain: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    idnumber: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    departament: Optional[str] = None

    @field_validator(
        "username", "password", "firstname", "lastname", "email", check_fields=False
    )
    @classmethod
    def validate_not_empty(cls, v: Optional[str], info: ValidationInfo):
        if v is None:
            return v

        v = v.strip()
        if not v:
            mensajes = {
                "username": "El nombre de usuario",
                "password": "La contraseña",
                "firstname": "El nombre",
                "lastname": "El apellido",
                "email": "El correo electrónico",
            }
            campo = mensajes.get(info.field_name, "El campo")
            raise ValueError(f"{campo} no puede estar vacío")

        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: Optional[str]):
        if v is None:
            return v

        v = v.strip()
        if not v:
            raise ValueError("El número de teléfono no puede estar vacío")

        check_val = v.replace("+", "", 1) if v.startswith("+") else v
        if not check_val.isdigit():
            raise ValueError(
                "El número de teléfono solo debe contener números y opcionalmente un '+' al inicio"
            )

        return v


class UserLogin(BaseModel):
    username: str
    password: str
    domain: str


class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    role_id: int
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    departament: Optional[str] = None
    idnumber: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserBasicResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    role_id: int
    idnumber: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
