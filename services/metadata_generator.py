import openai
import json
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class MetadataGenerator:
    """Generate viral titles, descriptions, and hashtags"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    def generate_metadata(self, transcript_segment: str) -> dict:
        """
        Generate title, description, hashtags, and headline for a clip
        Returns: dict with metadata
        """
        
        system_prompt = """You are a YouTube Shorts growth expert.

Generate for each clip:
1. Scroll-stopping title (under 60 characters)
2. SEO-optimized description (2–4 sentences)
3. 12 relevant hashtags
4. Short on-screen headline (max 6 words)

Title rules:
- Create curiosity
- Use power words
- Avoid clickbait lies
- Feel urgent or intriguing

Return in this exact format:

TITLE: ...
HEADLINE: ...
DESCRIPTION: ...
HASHTAGS: #tag1 #tag2 #tag3"""
        
        try:
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate metadata for:\n\n{transcript_segment}"}
                ],
                temperature=0.8,
            )
            
            response_text = response['choices'][0]['message']['content']
            
            # Parse response
            metadata = self._parse_metadata(response_text)
            logger.info("Metadata generated successfully")
            return metadata
        
        except Exception as e:
            logger.error(f"Metadata generation failed: {str(e)}")
            raise
    
    def _parse_metadata(self, response_text: str) -> dict:
        """
        Parse GPT response into structured metadata
        """
        metadata = {
            'title': '',
            'headline': '',
            'description': '',
            'hashtags': ''
        }
        
        lines = response_text.split('\n')
        
        for line in lines:
            if line.startswith('TITLE:'):
                metadata['title'] = line.replace('TITLE:', '').strip()
            elif line.startswith('HEADLINE:'):
                metadata['headline'] = line.replace('HEADLINE:', '').strip()
            elif line.startswith('DESCRIPTION:'):
                metadata['description'] = line.replace('DESCRIPTION:', '').strip()
            elif line.startswith('HASHTAGS:'):
                metadata['hashtags'] = line.replace('HASHTAGS:', '').strip()
        
        return metadata
