from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func, DateTime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    
    phone_number = Column(String, nullable=True)
    departament = Column(String, nullable=True) # Provincia

    role_id = Column(Integer, ForeignKey("roles.id"))

    deleted = Column(Boolean, index=True, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())