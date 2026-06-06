from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database.connection import Base
from datetime import datetime

class AdminSettings(Base):
    __tablename__ = "admin_settings"
    id = Column(Integer, primary_key=True, default=1)
    youtube_channel_url = Column(String, nullable=True)
    instagram_url = Column(String, nullable=True)
    watermark_url = Column(String, nullable=True)
    watermark_position = Column(String, default="bottom-right")
    watermark_opacity = Column(Float, default=0.8)
    caption_bg_color = Column(String, default="#000000")
    caption_text_color = Column(String, default="#FFFFFF")
    caption_highlight_color = Column(String, default="#FFFF00")
    caption_font = Column(String, default="Arial Black")
    auto_upload_enabled = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
