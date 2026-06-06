from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Viral Shorts API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api"
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ADMIN_PASSWORD: str = "admin-password-change-in-production"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/viral_shorts_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = "sk-"
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    WHISPER_MODEL: str = "whisper-1"
    YOUTUBE_CLIENT_ID: str = ""
    YOUTUBE_CLIENT_SECRET: str = ""
    YOUTUBE_REDIRECT_URI: str = "http://localhost:8000/api/auth/youtube/callback"
    STRIPE_SECRET_KEY: str = "sk_test_"
    STRIPE_WEBHOOK_SECRET: str = "whsec_"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_BUCKET_NAME: str = "viral-shorts-videos"
    AWS_REGION: str = "us-east-1"
    FRONTEND_URL: str = "http://localhost:3000"
    MAX_VIDEO_DURATION_MINUTES: int = 120
    MAX_FILE_SIZE_GB: int = 5
    TEMP_VIDEO_DIR: str = "/tmp/viral_shorts"
    FFMPEG_PATH: str = "/usr/bin/ffmpeg"
    FFPROBE_PATH: str = "/usr/bin/ffprobe"
    RESEND_API_KEY: str = "re_"
    ADMIN_EMAIL: str = "admin@example.com"
    LOG_LEVEL: str = "INFO"
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
