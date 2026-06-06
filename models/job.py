from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base
from datetime import datetime
import uuid
from enum import Enum as PyEnum

class JobStatusEnum(str, PyEnum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    TRANSCRIBING = "transcribing"
    ANALYZING = "analyzing"
    CLIPPING = "clipping"
    REFORMATTING = "reformatting"
    CAPTIONING = "captioning"
    GENERATING_METADATA = "generating_metadata"
    STORING = "storing"
    COMPLETE = "complete"
    FAILED = "failed"

class Job(Base):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    youtube_url = Column(String, nullable=False)
    status = Column(Enum(JobStatusEnum), default=JobStatusEnum.QUEUED, index=True)
    progress = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    raw_video_path = Column(String, nullable=True)
    transcript_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    clips = relationship("Clip", back_populates="job", cascade="all, delete-orphan")
