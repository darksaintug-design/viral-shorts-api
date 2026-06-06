import openai
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class TranscriptionService:
    """Transcribe video audio using OpenAI Whisper"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    def transcribe(self, audio_path: str) -> dict:
        """
        Transcribe audio file to text
        Returns: {"text": full_transcript, "segments": [{"start": time, "end": time, "text": text}]}
        """
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model=settings.WHISPER_MODEL,
                    file=audio_file,
                )
            
            logger.info(f"Transcription completed: {len(transcript['text'])} characters")
            return transcript
        
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise
