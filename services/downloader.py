import yt_dlp
import os
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class VideoDownloader:
    """Download videos using yt-dlp"""
    
    def __init__(self):
        self.temp_dir = settings.TEMP_VIDEO_DIR
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def download(self, youtube_url: str) -> str:
        """
        Download video from YouTube
        Returns: path to downloaded video file
        """
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(self.temp_dir, '%(id)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                video_path = os.path.join(self.temp_dir, f"{info['id']}.mp4")
                logger.info(f"Video downloaded: {video_path}")
                return video_path
        
        except Exception as e:
            logger.error(f"Video download failed: {str(e)}")
            raise
    
    def get_video_duration(self, video_path: str) -> int:
        """
        Get video duration in seconds using yt-dlp
        """
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_path, download=False)
                return int(info.get('duration', 0))
        except Exception as e:
            logger.error(f"Could not get video duration: {str(e)}")
            return 0
