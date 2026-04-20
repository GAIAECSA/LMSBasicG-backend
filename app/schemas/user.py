from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    phone_number: str | None
    departament: str | None

class UserLogin(BaseModel):
    email: str
    password: str