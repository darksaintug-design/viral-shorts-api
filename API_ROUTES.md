# Backend API Routes Documentation

## Authentication Endpoints

### POST /api/auth/signup
Register a new user
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

### POST /api/auth/login
Login and get JWT token
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

### GET /api/auth/me
Get current user info (requires Bearer token)

### POST /api/auth/logout
Logout user (token invalidation on frontend)

## Video Processing Endpoints

### POST /api/process
Start processing a YouTube video
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```
Returns: `job_id` for tracking

### GET /api/status/{job_id}
Get current processing status and progress percentage

### GET /api/clips/{job_id}
Get all generated clips with metadata (title, description, hashtags, virality score)

### POST /api/upload/{clip_id}
Upload a clip to YouTube Shorts

## Admin Endpoints

### GET /api/admin/settings
Get admin configuration (requires admin_password header)

### POST /api/admin/settings
Update admin configuration
```json
{
  "youtube_channel_url": "https://youtube.com/@channel",
  "instagram_url": "https://instagram.com/account",
  "watermark_position": "bottom-right",
  "watermark_opacity": 0.8,
  "caption_bg_color": "#000000",
  "caption_text_color": "#FFFFFF",
  "caption_highlight_color": "#FFFF00",
  "caption_font": "Arial Black",
  "auto_upload_enabled": false
}
```

## Job Status Values
- queued
- downloading
- transcribing
- analyzing
- clipping
- reformatting
- captioning
- adding_headlines
- generating_metadata
- storing
- complete
- failed
