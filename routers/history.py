from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from models.user import User
from models.job import Job
from routers.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["history"])

@router.get("/history")
def get_user_job_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get processing history for current user
    """
    jobs = db.query(Job).filter(Job.user_id == current_user.id).order_by(Job.created_at.desc()).all()
    
    return {
        "total_jobs": len(jobs),
        "jobs": [
            {
                "id": str(job.id),
                "youtube_url": job.youtube_url,
                "status": job.status.value,
                "progress": job.progress,
                "created_at": job.created_at,
                "completed_at": job.completed_at,
                "clip_count": len(job.clips),
            }
            for job in jobs
        ]
    }

@router.delete("/jobs/{job_id}")
def delete_job(job_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Delete a job and associated clips
    """
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    db.delete(job)
    db.commit()
    
    logger.info(f"Job {job_id} deleted by user {current_user.email}")
    
    return {"message": "Job deleted successfully"}
