from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class HomeworkResponse(Base):
    __tablename__ = "homework_responses"

    id = Column(Integer, primary_key=True, index=True)

    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    lesson_block_id = Column(Integer, ForeignKey("lesson_blocks.id"))

    submitted_file_url = Column(String)
    submitted_filename = Column(String)

    comment = Column(Text)

    score = Column(Numeric(4, 2))

    status = Column(String)

    deleted = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    enrollment = relationship("Enrollment", back_populates="homework_responses")

    lesson_block = relationship("LessonBlock", back_populates="homework_responses")
