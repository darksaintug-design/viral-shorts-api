from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base
from datetime import datetime
import uuid

class Clip(Base):
    __tablename__ = "clips"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False, index=True)
    video_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    headline = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    hashtags = Column(Text, nullable=False)
    virality_score = Column(Integer, default=0)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    transcript_segment = Column(Text, nullable=True)
    captions_text = Column(Text, nullable=True)
    uploaded_to_youtube = Column(Boolean, default=False)
    youtube_short_url = Column(String, nullable=True)
    youtube_video_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    job = relationship("Job", back_populates="clips")
