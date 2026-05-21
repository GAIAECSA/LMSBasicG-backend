from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserPrivacyPolicyCreate(BaseModel):
    user_id: int
    privacy_policy_id: int


class UserPrivacyPolicyResponse(BaseModel):
    id: int

    user_id: int
    privacy_policy_id: int

    accepted: bool
    accepted_at: datetime

    created_at: Optional[datetime]

    class Config:
        from_attributes = True
