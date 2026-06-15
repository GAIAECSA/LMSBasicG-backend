from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)
    is_mdt = Column(Boolean, nullable=False, default=False)

    deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    # =========================
    # Claves foráneas
    # =========================

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
        back_populates="categories",
    )

    subcategories = relationship(
        "Subcategory",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    # =========================
    # Restricciones
    # =========================

    __table_args__ = (
        Index(
            "uq_category_business_name_active",
            "business_id",
            "name",
            unique=True,
            postgresql_where=text("deleted = false"),
        ),
        CheckConstraint(
            "trim(name) <> ''",
            name="category_name_not_blank",
        ),
    )
