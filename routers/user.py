from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from models.user import User
from schemas.user import UserResponse
from routers.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["user"])

@router.get("/user/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    """
    return UserResponse.from_orm(current_user)

@router.get("/user/quota")
def get_user_quota(current_user: User = Depends(get_current_user)):
    """
    Get user's monthly video processing quota
    """
    limit = current_user.get_monthly_limit()
    used = current_user.videos_used_this_month
    
    return {
        "plan": current_user.plan.value,
        "limit": limit,
        "used": used,
        "remaining": max(0, limit - used),
        "percentage": min(100, int((used / limit * 100))) if limit > 0 else 100,
        "unlimited": limit > 100,
    }

@router.get("/user/youtube/status")
def get_youtube_status(current_user: User = Depends(get_current_user)):
    """
    Get YouTube connection status
    """
    return {
        "connected": current_user.youtube_connected,
        "channel_id": current_user.youtube_channel_id,
    }
