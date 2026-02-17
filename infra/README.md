# Eylo Recipe Import Backend

Backend infrastructure for importing recipes from Instagram, TikTok, and YouTube via Share Sheet integration.

## Architecture

**Fire and Forget Pattern**: Mobile clients send URLs and immediately return. Heavy processing (scraping, AI extraction) happens asynchronously with push notifications upon completion.

### Components

- **API Gateway** (`app/main.py`): FastAPI server handling import requests
- **Worker** (`app/worker.py`): Background processor for recipe extraction
- **Queue** (`app/queue.py`): Redis-based job queue (file-based fallback for local dev)
- **Services**:
  - **Apify Client**: Instagram/TikTok scraping via Apify actors
  - **YouTube Client**: YouTube video download via yt-dlp
  - **OpenAI Extractor**: GPT-4o-mini powered recipe extraction from video/images
  - **FCM Client**: Push notifications to mobile devices

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- API keys for: **Apify**, **OpenAI**, **Firebase**
- Database: **Supabase** (PostgreSQL) or SQLite for local testing
- Optional: Redis (recommended for production)

### 2. Setup (Local Development)

```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.local.example .env
# Edit .env with your API keys
```

### 3. Run Services

You need **two terminals** for local development:

**Terminal 1: API Server**
```bash
cd infra
python -m app.main
```

**Terminal 2: Background Worker**
```bash
cd infra
python -m app.worker
```

---

## 🧪 Testing

### Manual Testing

1. **Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Import Recipe** (Instagram):
   ```bash
   curl -X POST http://localhost:8000/import/recipe \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.instagram.com/reel/ABC123/"}'
   ```

3. **Import Recipe** (TikTok):
   ```bash
   curl -X POST http://localhost:8000/import/recipe \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.tiktok.com/@user/video/1234567890"}'
   ```

4. **List Recipes**:
   ```bash
   curl http://localhost:8000/recipes
   ```

5. **Verify Processing**:
   - Check Worker terminal for "Processing job..." and "Completed: [Recipe Title]"
   - Use Supabase dashboard to view `recipes` table

---

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Description | Required |
|----------|-------------|----------|
| `APIFY_API_TOKEN` | Apify API key for Instagram/TikTok scraping | Yes |
| `OPENAI_API_KEY` | OpenAI API key (GPT-4o-mini) for recipe extraction | Yes |
| `FCM_SERVER_KEY` | Firebase Cloud Messaging key for push notifications | Optional |
| `DATABASE_URL` | PostgreSQL connection string (Supabase recommended) | Yes |
| `REDIS_URL` | Redis connection string or `memory://` for local | Yes |

### Supported Platforms

- ✅ **Instagram** (Reels, Posts, Carousels)
- ✅ **TikTok** (Videos)
- ✅ **YouTube** (Shorts, Videos)

---

## 📦 Production Deployment

### Checklist

- [ ] Use **PostgreSQL** (Supabase, AWS RDS, etc.)
- [ ] Use **Redis** (Redis Cloud, ElastiCache, etc.)
- [ ] Set strong `JWT_SECRET` in `.env`
- [ ] Configure CORS origins in `main.py`
- [ ] Set up process manager (Supervisor, systemd, Docker, K8s)
- [ ] Monitor worker logs for failures

### Docker Deployment

```bash
# Build and run
docker-compose up -d --build

# View logs
docker-compose logs -f worker
docker-compose logs -f api

# Stop services
docker-compose down
```

---

## 🛠️ Troubleshooting

### Worker not picking up jobs?
- Ensure Worker is running **simultaneously** with API server
- If using file-based queue (`memory://`), allow 2-5s polling delay
- If using Redis, verify Redis is running: `redis-cli ping`

### Scraping failed?
- **Apify quota**: Check your Apify dashboard for remaining credits
- **TikTok 404**: Ensure video URL is public and valid
- **Instagram private**: Only public posts can be scraped

### "moov atom not found" error?
- This was fixed by enabling `shouldDownloadVideos: True` in TikTok scraper
- If issue persists, check worker logs for video download errors

### "Validation error for Ingredient"?
- This was fixed by allowing numeric types for `quantity` field
- If you see this, ensure you've restarted the worker after updating `schemas.py`

### Database issues?
- **SQLite** (local): Delete `eylo_test.db` to reset
- **Supabase**: Check connection string and ensure tables exist
- **Duplicate imports**: API blocks re-importing the same URL (by design)

### No data in database?
- Check worker logs for "Completed: [Recipe Title]"
- Verify you're checking the correct table (`recipes`)
- Ensure filtering by `user_id = "dummy_user"` (current default)
- Try refreshing Supabase dashboard (cache issue)

---

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/import/recipe` | Submit URL for recipe extraction |
| GET | `/recipes` | List all recipes (sorted by newest) |

---

## 🔧 Development Notes

### Project Structure
```
infra/
├── app/
│   ├── main.py           # FastAPI application
│   ├── worker.py         # Background job processor
│   ├── queue.py          # Job queue (Redis/file-based)
│   ├── database.py       # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── config.py         # Settings management
│   └── services/
│       ├── apify_client.py      # Instagram/TikTok scraping
│       ├── youtube_client.py    # YouTube download
│       ├── openai_extractor.py  # AI recipe extraction
│       └── fcm_client.py        # Push notifications
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── README.md           # This file
```

### Database Schema

**recipes** table:
- `id` (UUID): Primary key
- `user_id` (String): User identifier (currently "dummy_user")
- `title` (String): Recipe title
- `source_url` (String): Original URL
- `source_type` (String): Platform (instagram_reel, tiktok_video, youtube_short)
- `data` (JSON): Full recipe data (ingredients, steps, tags, etc.)
- `created_at` (Timestamp): Creation time
- `imported_at` (Timestamp): Import time

**import_jobs** table:
- `id` (UUID): Job ID
- `user_id` (String): User identifier
- `source_url` (String): URL being processed
- `status` (String): queued, processing, completed, failed
- `error_message` (String): Error details if failed
- `recipe_id` (UUID): Foreign key to recipes table
- `created_at` (Timestamp): Job creation time
- `completed_at` (Timestamp): Job completion time

---

## 📄 License

MIT
