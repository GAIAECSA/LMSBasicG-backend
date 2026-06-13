from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class ForumResponse(Base):
    __tablename__ = "forum_responses"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False)

    # Claves foráneas (con index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False, index=True)
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"), nullable=False, index=True)
    forum_response_id = Column(Integer, ForeignKey("forum_responses.id"), nullable=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    enrollment = relationship("Enrollment", back_populates="forum_responses")
    lesson_block = relationship("LessonBlock", back_populates="forum_responses")
    business = relationship("Business", back_populates="forum_responses")
    parent_response = relationship("ForumResponse", remote_side=[id])
