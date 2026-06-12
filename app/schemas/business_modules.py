from typing import Any

from pydantic import BaseModel


class BusinessModuleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    config: dict[str, Any]

    class Config:
        from_attributes = True
