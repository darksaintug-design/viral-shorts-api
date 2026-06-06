import openai
import json
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class CaptionGenerator:
    """Generate dynamic captions for viral shorts"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    def generate_captions(self, transcript_segment: str) -> str:
        """
        Generate dynamic captions for a clip
        Returns: formatted caption text
        """
        
        system_prompt = """You are a viral short-form content editor.

Rewrite the transcript into dynamic captions for vertical short videos.

Rules:
- Break into short punchy lines (1–6 words per line)
- Emphasize key words in ALL CAPS
- Add emojis sparingly for emotion
- Remove filler words
- Keep conversational tone
- Preserve original meaning

Style: Alex Hormozi bold kinetic captions

Output format:
Line 1
Line 2
Line 3

No extra commentary."""
        
        try:
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate captions for:\n\n{transcript_segment}"}
                ],
                temperature=0.8,
            )
            
            captions = response['choices'][0]['message']['content']
            logger.info("Captions generated successfully")
            return captions
        
        except Exception as e:
            logger.error(f"Caption generation failed: {str(e)}")
            raise
