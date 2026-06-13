from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class CertificateTemplate(Base):
    __tablename__ = "certificate_templates"

    id = Column(Integer, primary_key=True, index=True)
    background_image_url = Column(String)
    fields = Column(JSONB)
    qr_config = Column(JSONB)

    # Claves foráneas
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    course = relationship("Course", back_populates="certificate_templates")
    business = relationship("Business", back_populates="certificate_templates")