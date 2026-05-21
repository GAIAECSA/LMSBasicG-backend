from datetime import datetime
from pydantic import BaseModel


class ForumResponseBase(BaseModel):
    enrollment_id: int
    lesson_block_id: int
    comment: str
    forum_response_id: int | None = None


class ForumResponseCreate(ForumResponseBase):
    pass


class ForumResponseUpdate(BaseModel):
    comment: str | None = None
    deleted: bool | None = None


class ForumResponseResponse(ForumResponseBase):
    id: int
    deleted: bool
    created_at: datetime

    class Config:
        from_attributes = True