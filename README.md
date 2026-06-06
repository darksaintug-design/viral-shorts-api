# Viral Shorts API - Backend Setup

## Quick Start with Docker

### Prerequisites
- Docker & Docker Compose installed
- Environment variables set in `.env` file

### Start Development Environment

```bash
# Clone repository
git clone https://github.com/darksaintug-design/viral-shorts-api.git
cd viral-shorts-api

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
vim .env

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f api

# Run database migrations (if needed)
docker-compose exec api alembic upgrade head
```

### Services Running
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/api/docs
- **Database**: PostgreSQL on localhost:5432
- **Cache**: Redis on localhost:6379
- **Worker**: Celery background tasks

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

## Environment Variables

Create `.env` file with:

```env
# OpenAI
OPENAI_API_KEY=sk-...

# YouTube
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# AWS S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_BUCKET_NAME=viral-shorts-videos

# Database (docker-compose sets this)
DATABASE_URL=postgresql://viralshorts:viralshorts_password@postgres:5432/viral_shorts_db

# Redis (docker-compose sets this)
REDIS_URL=redis://redis:6379/0

# JWT
JWT_SECRET=your-secret-key-here
ADMIN_PASSWORD=admin-password-here
```

## Project Structure

```
viral-shorts-api/
├── config/              # Configuration
├── database/            # Database setup
├── models/              # SQLAlchemy models
├── routers/             # API endpoints
├── schemas/             # Pydantic schemas
├── services/            # Business logic
├── queue/               # Celery tasks
├── utils/               # Helper functions
├── main.py              # FastAPI app
├── requirements.txt     # Dependencies
├── Dockerfile           # Docker image
├── docker-compose.yml   # Local dev setup
└── .env.example         # Environment template
```

## Key Features

✅ JWT Authentication
✅ Video Download & Transcription
✅ AI Clip Detection
✅ Video Processing Pipeline
✅ Async Job Queue (Celery + Redis)
✅ PostgreSQL Database
✅ AWS S3 Integration
✅ Rate Limiting
✅ Admin Settings
✅ Error Handling & Logging

## Deployment

### Deploy to Railway or Render

1. Push repository to GitHub
2. Connect GitHub repo to Railway/Render
3. Set environment variables in dashboard
4. Add PostgreSQL and Redis add-ons
5. Deploy from main branch

### Environment Variables for Production

```
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=<production-postgres-url>
REDIS_URL=<production-redis-url>
FRONTEND_URL=https://yourdomain.com
```

## API Documentation

See `API_ROUTES.md` for complete endpoint documentation.

Access interactive docs at: http://localhost:8000/api/docs

## Troubleshooting

### Database Connection Issues
```bash
docker-compose logs postgres
```

### Celery Worker Issues
```bash
docker-compose logs worker
```

### Clear Redis Cache
```bash
docker-compose exec redis redis-cli FLUSHALL
```

### Rebuild Docker Images
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Support

For issues, check logs:
```bash
docker-compose logs -f
```
