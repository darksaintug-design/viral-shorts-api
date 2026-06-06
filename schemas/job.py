from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class JobCreate(BaseModel):
    youtube_url: str

class ClipData(BaseModel):
    id: str
    video_url: str
    title: str
    headline: str
    description: str
    hashtags: str
    virality_score: int
    start_time: str
    end_time: str
    duration: int
    captions_text: Optional[str] = None
    uploaded_to_youtube: bool = False
    youtube_short_url: Optional[str] = None
    class Config:
        from_attributes = True

class JobResponse(BaseModel):
    id: str
    youtube_url: str
    status: str
    progress: int
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    clips: List[ClipData] = []
    class Config:
        from_attributes = True

class JobStatusResponse(BaseModel):
    id: str
    status: str
    progress: int
    error_message: Optional[str] = None
    class Config:
        from_attributes = True
