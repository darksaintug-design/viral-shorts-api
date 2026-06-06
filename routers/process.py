from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from models.user import User
from models.job import Job, JobStatusEnum
from models.clip import Clip
from schemas.job import JobCreate, JobResponse, JobStatusResponse, ClipData
from routers.auth import get_current_user
from utils.validators import validate_youtube_url
from queue.tasks import process_video
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["processing"])

@router.post("/process", response_model=JobStatusResponse)
def process_youtube_url(job_data: JobCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not validate_youtube_url(job_data.youtube_url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid YouTube URL")
    
    if not current_user.can_process_video():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Monthly limit reached. Plan: {current_user.plan.value}"
        )
    
    job = Job(
        user_id=current_user.id,
        youtube_url=job_data.youtube_url,
        status=JobStatusEnum.QUEUED,
        progress=0
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    process_video.delay(str(job.id))
    
    logger.info(f"Job created: {job.id} for user {current_user.email}")
    
    return JobStatusResponse(
        id=str(job.id),
        status=job.status,
        progress=job.progress,
        error_message=job.error_message
    )

@router.get("/status/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    return JobStatusResponse(
        id=str(job.id),
        status=job.status,
        progress=job.progress,
        error_message=job.error_message
    )

@router.get("/clips/{job_id}", response_model=JobResponse)
def get_clips(job_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    clips = db.query(Clip).filter(Clip.job_id == job.id).all()
    
    return JobResponse(
        id=str(job.id),
        youtube_url=job.youtube_url,
        status=job.status,
        progress=job.progress,
        error_message=job.error_message,
        created_at=job.created_at,
        completed_at=job.completed_at,
        clips=[ClipData.from_orm(clip) for clip in clips]
    )

@router.post("/upload/{clip_id}")
def upload_clip_to_youtube(clip_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    clip = db.query(Clip).join(Job).filter(
        Clip.id == clip_id,
        Job.user_id == current_user.id
    ).first()
    
    if not clip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clip not found")
    
    if clip.uploaded_to_youtube:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Clip already uploaded")
    
    return {"message": "Upload queued", "clip_id": clip_id}
