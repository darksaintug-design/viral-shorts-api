from pydantic import BaseModel
from typing import Optional

class AdminSettingsUpdate(BaseModel):
    youtube_channel_url: Optional[str] = None
    instagram_url: Optional[str] = None
    watermark_position: Optional[str] = None
    watermark_opacity: Optional[float] = None
    caption_bg_color: Optional[str] = None
    caption_text_color: Optional[str] = None
    caption_highlight_color: Optional[str] = None
    caption_font: Optional[str] = None
    auto_upload_enabled: Optional[bool] = None

class AdminSettingsResponse(BaseModel):
    youtube_channel_url: Optional[str]
    instagram_url: Optional[str]
    watermark_position: str
    watermark_opacity: float
    caption_bg_color: str
    caption_text_color: str
    caption_highlight_color: str
    caption_font: str
    auto_upload_enabled: bool
    class Config:
        from_attributes = True
