import openai
import json
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class ClipAnalyzer:
    """Analyze transcript and detect viral clip moments using GPT-4"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    def analyze_and_detect_clips(self, transcript: str) -> list:
        """
        Analyze transcript and detect viral-ready clip segments
        Returns: list of clip segments with timestamps and metadata
        """
        
        system_prompt = """You are a viral content strategist specializing in YouTube Shorts, TikTok, and Instagram Reels.

Analyze the full video transcript and extract the most engaging 15–60 second segments most likely to go viral.

Focus on:
- Emotional intensity
- Controversial opinions
- Strong hooks
- Clear value (advice, tips, lessons)
- Storytelling moments
- Shocking or surprising statements
- Bold claims
- Conflict or tension

Avoid:
- Slow intros
- Sponsor messages
- Rambling
- Context-heavy segments that need full video

Return 3–5 clip segments.

Each clip must:
- Work independently without full context
- Start with a strong hook in first 3 seconds
- Have a satisfying ending

Return valid JSON only:
{
  "clips": [
    {
      "start_time": "HH:MM:SS",
      "end_time": "HH:MM:SS",
      "hook": "First 5 words of clip",
      "why_viral": "Short explanation"
    }
  ]
}"""
        
        try:
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this transcript:\n\n{transcript}"}
                ],
                temperature=0.7,
            )
            
            response_text = response['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                clips_data = json.loads(response_text)
                logger.info(f"Detected {len(clips_data['clips'])} viral clip moments")
                return clips_data['clips']
            except json.JSONDecodeError:
                logger.error("Failed to parse GPT response as JSON")
                return []
        
        except Exception as e:
            logger.error(f"Clip analysis failed: {str(e)}")
            raise
