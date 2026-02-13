# Eylo Recipe Import Backend

Backend infrastructure for importing recipes from Instagram via Share Sheet integration.

## Architecture

**Fire and Forget Pattern**: Mobile clients send URLs and immediately return. Heavy processing (scraping, AI) happens asynchronously with push notifications upon completion.

### Components

- **API Gateway** (`app/main.py`): FastAPI server handling import requests
- **Worker** (`app/worker.py`): Background processor for recipe extraction
- **Queue** (`app/queue.py`): Redis-based job queue (supports file-based fallback for local dev)
- **Services**:
  - **Apify Client**: Instagram/TikTok scraping with proxy rotation
  - **OpenAI Extractor**: AI-powered recipe extraction from video/images
  - **S3 Client**: Media storage
  - **FCM Client**: Push notifications

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- API keys for: Apify, OpenAI, AWS S3, Firebase
- Optional: Docker & Docker Compose (for production/Redis)

### 2. Setup (Local Development)

```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.local.example .env
# Edit .env with your API keys
```

### 3. Run Services

You need two terminals for local development:

**Terminal 1: API Server**
```bash
python -m app.main
```

**Terminal 2: Background Worker**
```bash
python -m app.worker
```

---

## 🧪 Testing

### Manual Testing

1. **Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Import Recipe**:
   ```bash
   curl -X POST http://localhost:8000/import/recipe \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.instagram.com/reel/ABC123/"}'
   ```

3. **Verify Processing**:
   - Check Worker logs for "Processing job..."
   - Use `check_db.py` (if available) or inspect database directly

---

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Description |
|----------|-------------|
| `APIFY_API_TOKEN` | Apify API key for scraping |
| `OPENAI_API_KEY` | OpenAI API key for extraction |
| `FCM_SERVER_KEY` | Firebase Cloud Messaging key |
| `AWS_S3_BUCKET` | AWS S3 Bucket Name |
| `AWS_ACCESS_KEY_ID` | AWS Credentials |
| `DATABASE_URL` | PostgreSQL connection string (or SQLite path) |
| `REDIS_URL` | Redis connection string (or `memory://`) |

### Redis Setup (Recommended for Prod)

The in-memory queue works for simple testing but doesn't share data between processes reliably. For robust development:

**Option 1: Docker (Recommended)**
```bash
docker run -d -p 6379:6379 --name eylo-redis redis
# Update .env: REDIS_URL=redis://localhost:6379
```

**Option 2: Windows**
- Use [Memurai](https://www.memurai.com/) or WSL.

---

## 📦 Deployment

### Production Checklist

- [ ] Use **PostgreSQL** (e.g., Supabase, AWS RDS)
- [ ] Use **Redis** (e.g., Redis Cloud, ElastiCache)
- [ ] Set `TEST_MODE=False` in `.env`
- [ ] Configure `CORS` origins in `main.py`
- [ ] Set up process manager (Supervisor, Docker Swarm, K8s)

### Docker Deployment

```bash
# Build and run
docker-compose up -d --build

# View logs
docker-compose logs -f
```

---

## 🛠️ Troubleshooting

**Worker not picking up jobs?**
- Ensure Worker is running *simultaneously* with API.
- If using file-based queue (default local), allow 2-5s lag.
- If using Redis, ensure Redis is running.

**Scraping failed?**
- Check Apify token quota.
- Verify Instagram content availability (public?).

**Database issues?**
- By default uses `eylo_test.db` (SQLite). Deleting this file resets the DB.

---

## License

MIT

