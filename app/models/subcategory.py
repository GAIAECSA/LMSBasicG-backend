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


class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String,
        index=True,
        nullable=False,
    )

    is_mdt = Column(
        Boolean,
        nullable=False,
        default=False,
    )

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

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
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

    category = relationship(
        "Category",
        back_populates="subcategories",
    )

    business = relationship(
        "Business",
        back_populates="subcategories",
    )

    courses = relationship(
        "Course",
        back_populates="subcategory",
        cascade="all, delete-orphan",
    )

    # =========================
    # Restricciones
    # =========================

    __table_args__ = (
        Index(
            "uq_subcategory_business_category_name_active",
            "business_id",
            "category_id",
            "name",
            unique=True,
            postgresql_where=text("deleted = false"),
        ),
        CheckConstraint(
            "trim(name) <> ''",
            name="subcategory_name_not_blank",
        ),
    )
