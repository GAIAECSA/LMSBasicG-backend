from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text, text)
from sqlalchemy.orm import relationship

from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ZoomMeeting(Base):
    __tablename__ = "zoom_meetings"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    teacher_id = Column(Integer, nullable=False, index=True)

    zoom_meeting_id = Column(String(64), nullable=False, unique=True, index=True)
    zoom_host_user_id = Column(String(128), nullable=True)

    topic = Column(String(255), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer, nullable=False)
    timezone = Column(String(64), nullable=False)

    password = Column(String(32), nullable=True)
    join_url = Column(Text, nullable=False)

    deleted = Column(Boolean, nullable=False, default=False, server_default=text("false"), index=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)

    business = relationship("Business", back_populates="zoom_meetings")