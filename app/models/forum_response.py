from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class ForumResponse(Base):
    __tablename__ = "forum_responses"

    id = Column(Integer, primary_key=True)

    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)

    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"), nullable=False)

    comment = Column(String, nullable=False)

    forum_response_id = Column(Integer, ForeignKey("forum_responses.id"), nullable=True)

    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    enrollment = relationship("Enrollment", back_populates="forum_responses")

    lesson_block = relationship("LessonBlock", back_populates="forum_responses")

    parent_response = relationship("ForumResponse", remote_side=[id])
