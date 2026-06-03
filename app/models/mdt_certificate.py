import os
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from app.db.base import Base

SECRET_KEY = os.getenv("ENCRYPTION_KEY")


class MdtCertificate(Base):
    __tablename__ = "mdt_certificates"

    __table_args__ = (
        CheckConstraint(
            "certificate_type IN ('MDT', 'INSTITUTIONAL')",
            name="ck_mdt_certificate_type",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )

    file_url = Column(String, nullable=False)
    file_name = Column(String, nullable=False)

    id_number = Column(
        EncryptedType(String, SECRET_KEY, AesEngine, "pkcs5"),
        nullable=False,
    )

    id_number_hash = Column(
        String,
        nullable=False,
        index=True,
    )

    certificate_type = Column(String(20), nullable=False)

    deleted = Column(Boolean, default=False, nullable=False)

    visited_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=None,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    course = relationship(
        "Course",
        back_populates="mdt_certificates",
    )

    def mark_as_visited(self) -> None:
        """
        Asigna la fecha y hora actual en zona horaria UTC al campo visited_at.
        Llamar a este método antes de hacer el db.commit() en tu servicio.
        """
        self.visited_at = datetime.now(timezone.utc)
