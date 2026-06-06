from celery import shared_task
from database.connection import SessionLocal
from models.user import User
from models.job import Job, JobStatusEnum
from models.clip import Clip
from services.downloader import VideoDownloader
from services.transcriber import TranscriptionService
from services.analyzer import ClipAnalyzer
from services.renderer import VideoRenderer
from services.captioner import CaptionGenerator
from services.metadata_generator import MetadataGenerator
from services.storage import S3Storage
from utils.validators import time_to_seconds, seconds_to_time
from config.settings import settings
import logging
import os
from datetime import datetime
import subprocess

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_video(self, job_id: str):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            logger.error(f"Job {job_id} not found")
            return
        
        user = db.query(User).filter(User.id == job.user_id).first()
        
        update_job_status(db, job, JobStatusEnum.DOWNLOADING, 10)
        downloader = VideoDownloader()
        video_path = downloader.download(job.youtube_url)
        job.raw_video_path = video_path
        
        update_job_status(db, job, JobStatusEnum.TRANSCRIBING, 25)
        audio_path = extract_audio(video_path)
        transcriber = TranscriptionService()
        transcript_data = transcriber.transcribe(audio_path)
        job.transcript_text = transcript_data.get('text', '')
        db.commit()
        
        update_job_status(db, job, JobStatusEnum.ANALYZING, 40)
        analyzer = ClipAnalyzer()
        clips_data = analyzer.analyze_and_detect_clips(job.transcript_text)
        
        if not clips_data:
            raise Exception("No viral clips detected")
        
        storage = S3Storage()
        renderer = VideoRenderer()
        caption_gen = CaptionGenerator()
        metadata_gen = MetadataGenerator()
        
        for idx, clip_data in enumerate(clips_data):
            progress = 50 + (idx / len(clips_data)) * 40
            
            update_job_status(db, job, JobStatusEnum.CLIPPING, int(progress))
            clip_output_path = os.path.join(settings.TEMP_VIDEO_DIR, f"clip_{idx}.mp4")
            renderer.extract_clip(
                video_path,
                clip_data['start_time'],
                clip_data['end_time'],
                clip_output_path
            )
            
            update_job_status(db, job, JobStatusEnum.REFORMATTING, int(progress + 5))
            vertical_path = os.path.join(settings.TEMP_VIDEO_DIR, f"vertical_{idx}.mp4")
            renderer.convert_to_vertical(clip_output_path, vertical_path)
            
            update_job_status(db, job, JobStatusEnum.CAPTIONING, int(progress + 10))
            transcript_segment = get_transcript_segment(
                job.transcript_text,
                clip_data['start_time'],
                clip_data['end_time']
            )
            captions = caption_gen.generate_captions(transcript_segment)
            
            captioned_path = os.path.join(settings.TEMP_VIDEO_DIR, f"captioned_{idx}.mp4")
            burn_captions_to_video(vertical_path, captioned_path, captions)
            
            update_job_status(db, job, JobStatusEnum.GENERATING_METADATA, int(progress + 15))
            metadata = metadata_gen.generate_metadata(transcript_segment)
            
            update_job_status(db, job, JobStatusEnum.STORING, int(progress + 20))
            s3_key = f"clips/{job.id}/clip_{idx}.mp4"
            video_url = storage.upload_file(captioned_path, s3_key)
            
            signed_url = storage.get_signed_url(s3_key)
            
            virality_score = calculate_virality_score(metadata, captions)
            
            clip = Clip(
                job_id=job.id,
                video_url=signed_url,
                title=metadata.get('title', 'Untitled'),
                headline=metadata.get('headline', ''),
                description=metadata.get('description', ''),
                hashtags=metadata.get('hashtags', ''),
                virality_score=virality_score,
                start_time=clip_data['start_time'],
                end_time=clip_data['end_time'],
                duration=time_to_seconds(clip_data['end_time']) - time_to_seconds(clip_data['start_time']),
                transcript_segment=transcript_segment,
                captions_text=captions,
            )
            db.add(clip)
        
        user.videos_used_this_month += 1
        
        update_job_status(db, job, JobStatusEnum.COMPLETE, 100)
        job.completed_at = datetime.utcnow()
        db.commit()
        
        cleanup_temp_files(video_path, audio_path)
        
        logger.info(f"Job {job_id} completed successfully")
    
    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        job.status = JobStatusEnum.FAILED
        job.error_message = str(e)
        db.commit()
    
    finally:
        db.close()

def update_job_status(db, job: Job, status: JobStatusEnum, progress: int):
    job.status = status
    job.progress = min(progress, 100)
    if job.started_at is None:
        job.started_at = datetime.utcnow()
    db.commit()
    logger.info(f"Job {job.id} - {status}: {progress}%")

def extract_audio(video_path: str) -> str:
    audio_path = video_path.replace('.mp4', '.mp3')
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-q:a', '9',
        '-n',
        audio_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return audio_path

def get_transcript_segment(full_transcript: str, start_time: str, end_time: str) -> str:
    return full_transcript[:500]

def burn_captions_to_video(input_path: str, output_path: str, captions: str):
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y',
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def calculate_virality_score(metadata: dict, captions: str) -> int:
    score = 50
    power_words = ['AMAZING', 'SHOCKING', 'INCREDIBLE', 'VIRAL', 'MUST', 'EPIC']
    for word in power_words:
        if word in metadata.get('title', '').upper():
            score += 5
    
    title_len = len(metadata.get('title', ''))
    if 40 <= title_len <= 60:
        score += 10
    
    hashtag_count = len(metadata.get('hashtags', '').split('#'))
    if hashtag_count >= 10:
        score += 5
    
    return min(score, 100)

def cleanup_temp_files(*file_paths):
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted temp file: {file_path}")
        except Exception as e:
            logger.warning(f"Could not delete temp file {file_path}: {str(e)}")
