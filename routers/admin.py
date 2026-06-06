from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from models.admin_settings import AdminSettings
from schemas.admin import AdminSettingsUpdate, AdminSettingsResponse
from utils.auth import verify_admin_password
from fastapi import Header
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])

def verify_admin(admin_password: str = Header(...)):
    if not verify_admin_password(admin_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin password")
    return True

@router.get("/settings", response_model=AdminSettingsResponse)
def get_settings(admin_verified: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    settings = db.query(AdminSettings).first()
    if not settings:
        settings = AdminSettings()
        db.add(settings)
        db.commit()
    
    return AdminSettingsResponse.from_orm(settings)

@router.post("/settings", response_model=AdminSettingsResponse)
def update_settings(
    settings_data: AdminSettingsUpdate,
    admin_verified: bool = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    settings = db.query(AdminSettings).first()
    if not settings:
        settings = AdminSettings()
        db.add(settings)
    
    update_data = settings_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)
    
    db.commit()
    db.refresh(settings)
    
    logger.info("Admin settings updated")
    
    return AdminSettingsResponse.from_orm(settings)
