from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: int
    role_id: int
    domain: str
    business_id: int


class UserSession(TokenPayload):
    pass
