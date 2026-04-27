from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class CertificateTemplateCreate(BaseModel):
    course_id: int
    fields: List[Dict[str, Any]]
    qr_config: Optional[Dict[str, Any]] = None


class CertificateTemplateUpdate(BaseModel):
    course_id: Optional[int] = None
    fields: Optional[List[Dict[str, Any]]] = None
    qr_config: Optional[Dict[str, Any]] = None

class CertificateTemplateResponse(BaseModel):
    id: int
    course_id: int
    background_image_url: Optional[str]
    fields: Optional[List[Dict[str, Any]]]
    qr_config: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True