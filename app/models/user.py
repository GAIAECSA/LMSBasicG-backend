import os

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from app.db.base import Base

SECRET_KEY = os.getenv("ENCRYPTION_KEY")


class User(Base):
    __tablename__ = "users"

    # =========================
    # Campos principales
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)

    email = Column(String, index=True, nullable=True)

    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)

    # =========================
    # Datos sensibles cifrados
    # =========================

    idnumber = Column(
        EncryptedType(
            String,
            SECRET_KEY,
            AesEngine,
            "pkcs5",
        ),
        nullable=True,
    )

    phone_number = Column(
        EncryptedType(
            String,
            SECRET_KEY,
            AesEngine,
            "pkcs5",
        ),
        nullable=True,
    )

    # Hashes para búsquedas
    idnumber_hash = Column(String, index=True, nullable=True)
    phone_number_hash = Column(String, index=True, nullable=True)

    # Nota: se mantiene el nombre para compatibilidad
    departament = Column(String, nullable=True)

    # =========================
    # Auditoría
    # =========================

    deleted = Column(
        Boolean,
        index=True,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # =========================
    # Claves foráneas
    # =========================

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
        index=True,
    )

    # =========================
    # Relaciones
    # =========================

    business = relationship(
        "Business",
        back_populates="users",
    )

    role = relationship(
        "Role",
        back_populates="users",
    )

    certificates = relationship(
        "Certificate",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    privacy_policies = relationship(
        "UserPrivacyPolicy",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # =========================
    # Restricciones
    # =========================

    __table_args__ = (
        Index(
            "uq_user_business_username_active",
            "business_id",
            "username",
            unique=True,
            postgresql_where=text("deleted = false"),
        ),
        Index(
            "uq_user_business_email_active",
            "business_id",
            "email",
            unique=True,
            postgresql_where=text("deleted = false"),
        ),
        CheckConstraint(
            "email IS NULL OR trim(email) <> ''",
            name="email_not_blank",
        ),
        CheckConstraint(
            "trim(username) <> ''",
            name="username_not_blank",
        ),
        CheckConstraint(
            "trim(password) <> ''",
            name="password_not_blank",
        ),
        CheckConstraint(
            "trim(firstname) <> ''",
            name="firstname_not_blank",
        ),
        CheckConstraint(
            "trim(lastname) <> ''",
            name="lastname_not_blank",
        ),
    )
