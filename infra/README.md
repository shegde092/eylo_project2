# Eylo Recipe Import Backend

Backend infrastructure for importing recipes from Instagram via Share Sheet integration.

## Architecture

**Fire and Forget Pattern**: Mobile clients send URLs and immediately return. Heavy processing (scraping, AI) happens asynchronously with push notifications upon completion.

### Components

- **API Gateway** (`app/main.py`): FastAPI server handling import requests
- **Worker** (`app/worker.py`): Background processor for recipe extraction
- **Queue** (`app/queue.py`): Redis-based job queue
- **Services**:
  - **Apify Client**: Instagram scraping with proxy rotation
  - **Gemini Extractor**: AI-powered recipe extraction from video/images
  - **S3 Client**: Media storage
  - **FCM Client**: Push notifications

## Quick Start

### 1. Prerequisites

- Docker & Docker Compose
- Python 3.11+
- API keys for: Apify, Gemini AI, AWS S3, Firebase

### 2. Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# nano .env

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f api
docker-compose logs -f worker
```

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Import a recipe
curl -X POST http://localhost:8000/import/recipe \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.instagram.com/reel/ABC123/",
    "fcm_token": "your_device_token"
  }'

# Response:
# {
#   "job_id": "uuid-here",
#   "status": "processing",
#   "message": "Recipe import started..."
# }
```

## Data Flow

```
Mobile App → POST /import/recipe → Redis Queue → Worker Process
                ↓                                      ↓
            202 Accepted                    1. Scrape (Apify)
                                           2. Extract (Gemini)
                                           3. Upload (S3)
                                           4. Save (PostgreSQL)
                                           5. Notify (FCM)
                                                ↓
                                        Push Notification
```

## Database Schema

### Recipes Table

```sql
id              UUID PRIMARY KEY
user_id         UUID NOT NULL
title           VARCHAR(255)
source_url      TEXT
source_type     VARCHAR(50)  -- 'reel', 'post', 'tv'
data            JSONB         -- Structured recipe data
thumbnail_url   TEXT
video_url       TEXT
created_at      TIMESTAMP
```

### Recipe Data (JSONB)

```json
{
  "prep_time_minutes": 15,
  "cook_time_minutes": 20,
  "ingredients": [
    {"item": "Pasta", "quantity": "500", "unit": "g"}
  ],
  "steps": ["Boil water...", "Cook pasta..."],
  "tags": ["italian", "quick"]
}
```

## Development

### Run Locally (Without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL and Redis manually
# or use:
docker-compose up postgres redis -d

# Run API
python -m app.main

# Run Worker (in another terminal)
python -m app.worker
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Environment Variables

See `.env.example` for required variables:

- `APIFY_API_TOKEN`: Apify API key
- `GEMINI_API_KEY`: Google AI Studio key
- `FCM_SERVER_KEY`: Firebase Cloud Messaging key
- `AWS_S3_BUCKET`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: AWS credentials
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string

## API Endpoints

### POST `/import/recipe`

Import a recipe from Instagram URL.

**Request:**
```json
{
  "url": "https://www.instagram.com/reel/ABC123/",
  "fcm_token": "optional_fcm_token"
}
```

**Response:**
```json
{
  "job_id": "uuid",
  "status": "processing",
  "message": "Recipe import started. You'll receive a notification when it's ready."
}
```

### GET `/recipes/{recipe_id}`

Get recipe by ID (used after push notification).

### GET `/recipes`

List all recipes (paginated).

## Deployment

### Production Checklist

- [ ] Update CORS origins in `main.py`
- [ ] Add authentication middleware
- [ ] Configure Firebase service account
- [ ] Set up monitoring (Sentry, DataDog)
- [ ] Configure auto-scaling for worker
- [ ] Set up backup for PostgreSQL
- [ ] Use managed Redis (AWS ElastiCache, etc.)

### Deploy to AWS

```bash
# Build and push Docker images
docker build -t eylo-api .
docker tag eylo-api:latest <ecr-repo>/eylo-api:latest
docker push <ecr-repo>/eylo-api:latest

# Update ECS service
aws ecs update-service --cluster eylo --service api --force-new-deployment
```

## Monitoring

### Key Metrics

- Recipe import success rate
- Average processing time per job
- Apify scraping failures
- Gemini AI extraction errors
- S3 upload failures

### Logs

```bash
# View API logs
docker-compose logs -f api

# View worker logs
docker-compose logs -f worker

# Filter for errors
docker-compose logs api | grep ERROR
```

## Troubleshooting

### Worker not processing jobs

```bash
# Check Redis queue
docker exec -it eylo_redis redis-cli
> LLEN eylo:recipe_import
> LRANGE eylo:recipe_import 0 -1
```

### Apify scraping fails

- Check API token is valid
- Instagram may have changed layout (update Apify actor)
- Check rate limits

### Gemini AI errors

- Verify API key
- Check video file size < 2GB
- Ensure video format is supported

## Cost Optimization

- Use S3 Intelligent-Tiering for old videos
- Implement caching for duplicate URLs
- Batch Gemini requests if possible
- Monitor Apify usage (most expensive component)

## License

MIT
