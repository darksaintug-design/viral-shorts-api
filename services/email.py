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
                    "subject": "Welcome to Viral Shorts! 🎬",
                    "html": f"""
                    <h1>Welcome to Viral Shorts!</h1>
                    <p>Hi {user_name or user_email},</p>
                    <p>Your account is ready. Start converting YouTube videos to viral shorts in 60 seconds.</p>
                    <p><a href="{settings.FRONTEND_URL}/dashboard">Go to Dashboard</a></p>
                    """
                }
            )
            logger.info(f"Welcome email sent to {user_email}")
        except Exception as e:
            logger.error(f"Failed to send welcome email: {str(e)}")
    
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
                    "subject": f"Your {clip_count} Viral Shorts are Ready! 🚀",
                    "html": f"""
                    <h1>Your Shorts are Ready!</h1>
                    <p>We've generated {clip_count} viral-ready shorts from your video.</p>
                    <p>Each short has:</p>
                    <ul>
                        <li>✅ Optimized captions</li>
                        <li>✅ Viral title & description</li>
                        <li>✅ SEO hashtags</li>
                        <li>✅ Virality score</li>
                    </ul>
                    <p><a href="{settings.FRONTEND_URL}/clips/{job_id}">View Your Shorts</a></p>
                    """
                }
            )
            logger.info(f"Shorts ready email sent to {user_email}")
        except Exception as e:
            logger.error(f"Failed to send shorts ready email: {str(e)}")
    
    @staticmethod
    def send_processing_failed_email(user_email: str, error_message: str):
        """
        Send email when processing fails
        """
        try:
            from resend import Resend
            resend = Resend(api_key=settings.RESEND_API_KEY)
            
            resend.emails.send(
                {
                    "from": settings.ADMIN_EMAIL,
                    "to": user_email,
                    "subject": "Video Processing Failed",
                    "html": f"""
                    <h1>Processing Failed</h1>
                    <p>We encountered an error processing your video:</p>
                    <p><code>{error_message}</code></p>
                    <p><a href="{settings.FRONTEND_URL}/dashboard">Try Again</a></p>
                    """
                }
            )
            logger.info(f"Error email sent to {user_email}")
        except Exception as e:
            logger.error(f"Failed to send error email: {str(e)}")
