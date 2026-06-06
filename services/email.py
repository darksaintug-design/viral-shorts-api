from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Send emails using Resend"""
    
    @staticmethod
    def send_welcome_email(user_email: str, user_name: str = None):
        """
        Send welcome email to new user
        """
        try:
            from resend import Resend
            resend = Resend(api_key=settings.RESEND_API_KEY)
            
            resend.emails.send(
                {
                    "from": settings.ADMIN_EMAIL,
                    "to": user_email,
                    "subject": "Welcome to Viral Shorts!",
                    "html": f"<h1>Welcome!</h1><p>Start converting YouTube to viral shorts.</p><a href='{settings.FRONTEND_URL}/dashboard'>Dashboard</a>"
                }
            )
            logger.info(f"Welcome email sent to {user_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
    
    @staticmethod
    def send_shorts_ready_email(user_email: str, job_id: str, clip_count: int):
        """
        Send email when shorts are ready
        """
        try:
            from resend import Resend
            resend = Resend(api_key=settings.RESEND_API_KEY)
            
            resend.emails.send(
                {
                    "from": settings.ADMIN_EMAIL,
                    "to": user_email,
                    "subject": f"Your {clip_count} Viral Shorts are Ready!",
                    "html": f"<h1>Shorts Ready!</h1><p>Generated {clip_count} viral shorts.</p><a href='{settings.FRONTEND_URL}/clips/{job_id}'>View</a>"
                }
            )
            logger.info(f"Shorts ready email sent to {user_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
