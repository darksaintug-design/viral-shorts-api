from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base
from datetime import datetime
import uuid
from enum import Enum as PyEnum

class PlanEnum(str, PyEnum):
    FREE = "free"
    PRO = "pro"
    AGENCY = "agency"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    plan = Column(Enum(PlanEnum), default=PlanEnum.FREE)
    videos_used_this_month = Column(Integer, default=0)
    monthly_reset_date = Column(DateTime, nullable=True)
    youtube_connected = Column(Boolean, default=False)
    youtube_refresh_token = Column(String, nullable=True)
    youtube_channel_id = Column(String, nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def get_monthly_limit(self):
        limits = {PlanEnum.FREE: 3, PlanEnum.PRO: 999999, PlanEnum.AGENCY: 999999}
        return limits.get(self.plan, 3)
    
    def can_process_video(self):
        limit = self.get_monthly_limit()
        return self.videos_used_this_month < limit
