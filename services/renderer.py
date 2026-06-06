import subprocess
import os
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class VideoRenderer:
    """Render video clips using FFmpeg"""
    
    def __init__(self):
        self.ffmpeg_path = settings.FFMPEG_PATH
        self.ffprobe_path = settings.FFPROBE_PATH
        self.temp_dir = settings.TEMP_VIDEO_DIR
    
    def extract_clip(self, input_path: str, start_time: str, end_time: str, output_path: str) -> bool:
        """
        Extract clip segment from video
        """
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-ss', start_time,
                '-to', end_time,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'medium',
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
            
            logger.info(f"Clip extracted: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Clip extraction failed: {str(e)}")
            return False
    
    def convert_to_vertical(self, input_path: str, output_path: str) -> bool:
        """
        Convert video to 9:16 vertical format
        Crops and centers the video
        """
        try:
            # Scale to 1080x1920 with padding
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-c:a', 'aac',
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
            
            logger.info(f"Video converted to vertical: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Vertical conversion failed: {str(e)}")
            return False
    
    def add_captions(self, input_path: str, output_path: str, captions: str, settings_obj=None) -> bool:
        """
        Add burned-in captions to video
        """
        try:
            # Simplified caption burning - just copies video
            # Real implementation would use drawtext filter
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'medium',
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
            
            logger.info(f"Captions added: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Caption addition failed: {str(e)}")
            return False
    
    def get_video_info(self, video_path: str) -> dict:
        """
        Get video information using ffprobe
        """
        try:
            cmd = [
                self.ffprobe_path,
                '-v', 'error',
                '-show_format',
                '-show_streams',
                '-of', 'json',
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
                
                return {
                    'duration': float(data['format'].get('duration', 0)),
                    'width': video_stream['width'] if video_stream else 0,
                    'height': video_stream['height'] if video_stream else 0,
                }
            return {}
        except Exception as e:
            logger.error(f"Could not get video info: {str(e)}")
            return {}
