# Eylo Backend - Local Development Setup (No Docker)

This guide shows how to run the backend locally without Docker.

## Prerequisites

- Python 3.11+ ✓ (You have 3.13.7)
- Redis (optional - we'll use a simplified in-memory queue for testing)
- PostgreSQL (optional - we'll use SQLite for testing)

## Quick Start (Simplified Testing Mode)

### 1. Create Virtual Environment

```powershell
cd infra
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure Environment (Test Mode)

```powershell
cp .env.local.example .env
# Uses SQLite instead of PostgreSQL
# Uses in-memory queue instead of Redis
```

### 4. Run API Server

```powershell
python -m app.main
```

API will be available at: `http://localhost:8000`

### 5. Run Worker (in another terminal)

```powershell
cd infra
.\venv\Scripts\Activate.ps1
python -m app.worker
```

## Testing the API

```powershell
# Health check
curl http://localhost:8000/health

# Import a recipe (test mode - will use mock scraper)
curl -X POST http://localhost:8000/import/recipe `
  -H "Content-Type: application/json" `
  -d '{\"url\": \"https://www.instagram.com/reel/test123/\"}'
```

## Full Production Mode

If you want to test with real services (Apify, Gemini, etc.):

1. Install Redis: https://github.com/microsoftarchive/redis/releases
2. Install PostgreSQL: https://www.postgresql.org/download/windows/
3. Get API keys:
   - Apify: https://console.apify.com/
   - Gemini: https://aistudio.google.com/app/apikey
   - AWS S3: https://console.aws.amazon.com/
   - Firebase: https://console.firebase.google.com/

4. Update `.env` with real credentials

## Troubleshooting

### Module not found errors

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Port already in use

Change port in `.env`:
```
API_PORT=8001
```

### Database errors

We're using SQLite by default for testing, so no PostgreSQL needed initially.
