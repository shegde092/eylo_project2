# Eylo Project - Complete File-by-File Technical Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Complete File Reference](#complete-file-reference)
   - [Root Files](#root-directory-files)
   - [Backend Files](#backend-directory-infra)
   - [Mobile Files](#mobile-directory-mobile)
4. [Technology Stack](#technology-stack)
5. [Data Flow](#data-flow)
6. [Deployment](#deployment)

---

## 🎯 Project Overview

**Eylo** is a recipe import application that allows users to save Instagram, YouTube, and TikTok recipes directly into their recipe collection using AI-powered extraction.

### Key Features
- **Seamless UX**: Share from social media → Recipe ready in ~30 seconds
- **AI-Powered**: OpenAI GPT-4o-mini extracts structured recipe data from videos and images
- **Cross-Platform**: Works on both iOS and Android via Share Sheet integration
- **Async Processing**: Fire-and-forget - users don't wait for processing
- **Push Notifications**: Alerts when recipe is ready

### User Flow
1. User views cooking video on Instagram/YouTube/TikTok
2. Taps Share → Selects "Eylo"
3. Extension extracts URL and sends to backend
4. Receives immediate confirmation (< 2 seconds)
5. Backend processes asynchronously (30-40 seconds)
6. Push notification: "Recipe Ready! 🍝"
7. User opens app and views recipe

---

## 🏗️ Architecture

```
Social Media App
      ↓
Share Extension (iOS/Android)
      ↓
FastAPI Server (main.py)
      ↓
Job Queue (queue.py)
      ↓
Worker Process (worker.py)
   ├→ Scraper (apify_client.py, youtube_client.py)
   ├→ AI Extraction (openai_extractor.py)
   ├→ Database (database.py)
   └→ Push Notification (fcm_client.py)
```

---

## 📁 Project Structure

```
eylo_project2/
│
├── 📄 README.md                      # Main project documentation
├── 📄 explain.md                     # This file - Complete documentation
│
├── 📁 infra/                         # Backend (FastAPI + Worker)
│   │
│   ├── 📄 .env                       # Environment variables (gitignored)
│   ├── 📄 .env.example               # Template for .env
│   ├── 📄 .env.local.example         # Local dev template
│   ├── 📄 .gitignore                 # Git ignore rules
│   │
│   ├── 📄 requirements.txt           # Python dependencies
│   ├── 📄 docker-compose.yml         # Multi-container Docker setup
│   ├── 📄 Dockerfile                 # Container image
│   │
│   ├── 📄 README.md                  # Backend documentation (Consolidated)
│   │
│   ├── 📁 app/                       # Main application code
│   │   ├── 📄 __init__.py            # Package marker
│   │   ├── 📄 main.py                # ⭐ FastAPI server (API endpoints)
│   │   ├── 📄 worker.py              # ⭐ Background job processor
│   │   ├── 📄 config.py              # Configuration management
│   │   ├── 📄 database.py            # SQLAlchemy ORM models
│   │   ├── 📄 schemas.py             # Pydantic validation models
│   │   ├── 📄 queue.py               # Job queue (Redis/file-based)
│   │   ├── 📄 utils.py               # Helper utilities
│   │   │
│   │   └── 📁 services/              # External service integrations
│   │       ├── 📄 __init__.py        # Package marker
│   │       ├── 📄 apify_client.py    # ⭐ Instagram/TikTok scraper
│   │       ├── 📄 youtube_client.py  # ⭐ YouTube scraper (yt-dlp)
│   │       ├── 📄 openai_extractor.py # ⭐ AI recipe extraction (PRIMARY)
│   │       └── 📄 fcm_client.py      # Push notifications
│   │
│   ├── 📁 migrations/                # Database migrations (unused)
│   │
│
└── 📁 mobile/                        # Mobile applications
    │
    ├── 📁 ios/                       # iOS Share Extension
    │   ├── 📁 EyloShare/             # Share Extension code
    │   │   ├── 📄 ShareViewController.swift  # Main controller
    │   │   └── 📄 Info.plist         # Extension metadata
    │   └── 📄 README.md              # iOS setup guide
    │
    ├── 📁 android/                   # Android Share Intent
    │   ├── 📁 app/src/main/
    │   │   ├── 📁 java/com/eylo/
    │   │   │   ├── 📄 ShareActivity.kt       # Handle share intent
    │   │   │   ├── 📄 RecipeImportWorker.kt  # Background worker
    │   │   │   ├── 📄 ApiService.kt          # Retrofit API client
    │   │   │   └── 📁 models/                # Data models
    │   │   ├── 📁 res/                       # Resources (layouts, strings)
    │   │   └── 📄 AndroidManifest.xml        # App manifest
    │   └── 📄 README.md              # Android setup guide
    │
    └── 📁 Eylo/                      # Main Eylo app (React Native)
        └── (Not documented in this guide)
```

### 📂 Directory Breakdown

#### Root Level (2 files)
- **Documentation**: Main README and this technical guide.

#### Backend (`infra/`) - 20+ files
- **Configuration**: Env files, Docker, requirements.
- **Application Code**: 14 Python files (Core logic + Services).
- **Documentation**: 1 Consolidated README.

#### Mobile (`mobile/`) - 8+ files
- **iOS**: 3 Swift/config files
- **Android**: 5+ Kotlin/config files

### 🔑 Key Files (Must Know)

| File | Purpose | Lines | Critical? |
|------|---------|-------|-----------|
| **`infra/app/main.py`** | API Server | 101 | ⭐⭐⭐ |
| **`infra/app/worker.py`** | Job Processor | 253 | ⭐⭐⭐ |
| **`infra/app/services/openai_extractor.py`** | AI Extraction | 188 | ⭐⭐⭐ |
| **`infra/app/services/apify_client.py`** | Scraping | 169 | ⭐⭐⭐ |
| **`infra/app/database.py`** | ORM Models | 49 | ⭐⭐ |
| **`infra/README.md`** | Backend Docs | 260 | ⭐⭐ |

### 📊 File Count Summary

- **Total Files**: ~35 (Reduced from 50+)
- **Python Files**: 14
- **Config Files**: 6
- **Documentation**: 4
- **Mobile Files**: 8+


---

## �📂 Complete File Reference

### 📍 Root Directory Files

#### `README.md`
**Location**: `/`  
**Purpose**: Main project documentation  
**Size**: 322 lines

**Contains**:
- Project overview and key features
- Architecture diagram
- Project structure overview
- Quick start guide for backend, iOS, Android
- How it works (user flow + tech stack)
- Testing instructions
- Current status and TODO
- Cost estimates ($81-91/month at 1,000 recipes/month)
- Troubleshooting guide

**Key Sections**:
```markdown
- 🎯 Project Overview
- 🏗️ Architecture  
- 📁 Project Structure
- 🚀 Quick Start
- 📱 How It Works
- 🧪 Testing
- 📊 Current Status
- 💰 Cost Estimates
- 🐛 Troubleshooting
```

---

#### `MANUAL_COMMANDS.md`
**Location**: `/`  
**Purpose**: Quick reference for manual commands  
**Size**: 136 lines

**Use Case**: Running project without Docker

**Commands**:
```powershell
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run API (Terminal 1)
python -m app.main

# Run Worker (Terminal 2)
python -m app.worker

# Test
curl http://localhost:8000/health
python check_db.py
```

**Also Includes**:
- Docker commands (`docker-compose up -d`)
- Testing commands
- Batch script shortcuts

---

###  📍 Backend Directory (`infra/`)

#### Configuration Files

##### `.env`
**Location**: `/infra/`  
**Purpose**: Environment variables (production)  
**Size**: 33 lines

**⚠️ CRITICAL**: Never commit! Listed in `.gitignore`

**Structure**:
```env
# API Settings
API_HOST=0.0.0.0
API_PORT=8000
JWT_SECRET=eylo_secret_key_change_in_production

# Database (Supabase PostgreSQL)
DATABASE_URL=postgresql://postgres:password@host:5432/postgres

# Queue (Redis or in-memory)
REDIS_URL=memory://  # Use redis://localhost:6379 for production

# AI Keys
OPENAI_API_KEY=sk-proj-...
APIFY_API_TOKEN=apify_api_...
GEMINI_API_KEY=test_key
FCM_SERVER_KEY=test_key

# AWS S3 Storage
AWS_S3_BUCKET=eylo-recipes
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

# Worker Settings
WORKER_CONCURRENCY=2
RETRY_ATTEMPTS=2
RETRY_DELAY_SECONDS=3

# Mode
TEST_MODE=false
```

---

##### `.env.example`
**Location**: `/infra/`  
**Purpose**: Template for environment variables

**Usage**: `cp .env.example .env` then fill in real values

---

##### `.env.local.example`
**Location**: `/infra/`  
**Purpose**: Local development template

**Differences from production**:
- Uses SQLite instead of PostgreSQL
- Uses `memory://` instead of Redis
- Has test/mock API keys

---

##### `.gitignore`
**Location**: `/infra/`  
**Purpose**: Exclude files from version control

**Ignores**:
```
__pycache__/
*.pyc
.env
venv/
*.db
queue_jobs.json
last_apify_run.json
```

---

##### `requirements.txt`
**Location**: `/infra/`  
**Purpose**: Python dependencies  
**Size**: 729 bytes

**Key Packages**:
```txt
fastapi==0.104.1           # API framework
uvicorn[standard]==0.24.0  # ASGI server
sqlalchemy==2.0.23         # ORM
psycopg2-binary==2.9.9     # PostgreSQL driver

redis==5.0.1               # Queue
openai==1.3.5              # OpenAI GPT-4o-mini
google-generativeai==0.3.1 # Gemini AI (legacy)

boto3==1.29.7              # AWS S3
firebase-admin==6.2.0      # Push notifications

httpx==0.25.1              # Async HTTP client
opencv-python==4.8.1.78    # Video frame extraction
yt-dlp==2023.11.16         # YouTube downloads

pydantic==2.5.0            # Data validation
pydantic-settings==2.1.0   # Settings management
```

**Install**: `pip install -r requirements.txt`

---

##### `requirements-local.txt`
**Location**: `/infra/`  
**Purpose**: Additional local dev dependencies

**Contains**: Testing and debugging tools

---

##### `docker-compose.yml`
**Location**: `/infra/`  
**Purpose**: Multi-container Docker orchestration  
**Size**: 1,525 bytes

**Services**:
```yaml
services:
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    
  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [redis]
    
  worker:
    build: .
    command: python -m app.worker
    env_file: .env
    depends_on: [redis]
```

**Commands**:
```bash
docker-compose up -d        # Start
docker-compose logs -f      # View logs
docker-compose down         # Stop
docker-compose restart api  # Restart API only
```

---

##### `Dockerfile`
**Location**: `/infra/`  
**Purpose**: Container image definition  
**Size**: 610 bytes

**Process**:
```dockerfile
FROM python:3.11-slim

# Install system deps (OpenCV needs libGL)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ /app/app/

# Expose port
EXPOSE 8000

# Default command (override in docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

---

##### `alembic.ini`
**Location**: `/infra/`  
**Purpose**: Database migration configuration (Alembic)  
**Status**: **Currently unused** - SQLAlchemy auto-creates tables

**Note**: Future migrations would use this

---

#### Documentation Files

##### `infra/README.md`
**Location**: `/infra/`  
**Purpose**: Backend-specific documentation  
**Size**: 5,794 bytes

**Sections**:
- Prerequisites (Python 3.11+, Docker)
- Installation steps
- Environment setup
- Running locally vs Docker
- API endpoints documentation
- Database schema
- Testing guide

---

##### `SETUP_GUIDE.md`
**Location**: `/infra/`  
**Purpose**: Quick setup for Supabase testing  
**Size**: 49 lines

**Steps**:
1. Install dependencies: `pip install google-generativeai openai psycopg2-binary`
2. Get Supabase password from dashboard
3. Update `DATABASE_URL` in `.env`
4. Restart API: `python -m app.main`
5. Test: `python test_api.py`

**Supabase Details**:
```
Host: db.ijsbaxhpkqvxzyuwsptp.supabase.co
Port: 5432
Database: postgres
User: postgres.ijsbaxhpkqvxzyuwsptp
```

---

##### `LOCAL_DEV.md`
**Location**: `/infra/`  
**Purpose**: Local development without Docker  
**Size**: 2,087 bytes

**Key Points**:
- Use SQLite (auto-created as `eylo_test.db`)
- File-based queue (`queue_jobs.json`)
- No Redis needed
- Faster iteration

---

##### `TESTING_GUIDE.md`
**Location**: `/infra/`  
**Purpose**: Testing procedures  
**Size**: 2,339 bytes

**Test Files**:
- `test_api.py` - API endpoints
- `test_real_reel.py` - Real Instagram test
- `check_db.py` - Database contents
- `test_openai_extraction.py` - AI extraction

---

##### `REDIS_SETUP.md`
**Location**: `/infra/`  
**Purpose**: Redis installation guide  
**Size**: 1,368 bytes

**Platforms**:
- Windows (via WSL or Memurai)
- Mac (`brew install redis`)
- Linux (`apt-get install redis`)

---

#### Application Code (`infra/app/`)

##### `__init__.py`
**Location**: `/infra/app/`  
**Purpose**: Package marker  
**Size**: 28 bytes

**Contents**: `# Eylo Backend Application`

---

##### `main.py`
**Location**: `/infra/app/`  
**Purpose**: **FastAPI application - API server**  
**Size**: 101 lines

**Role**: HTTP API Gateway

**Endpoints**:

**1. `GET /`**
```python
@app.get("/")
def read_root():
    return {"message": "Welcome to Eylo Recipe Import API"}
```

**2. `GET /health`**
```python
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

**3. `POST /import/recipe`**
**Purpose**: Queue a recipe import job

**Request**:
```json
{
  "url": "https://www.instagram.com/reel/ABC123/",
  "fcm_token": "optional_device_token"
}
```

**Process**:
```python
async def import_recipe(request: RecipeImportRequest, db: Session):
    user_id = str(uuid.uuid4())  # TODO: Get from JWT
    
    # Check for duplicates
    existing_recipe = db.query(Recipe).filter(
        Recipe.source_url == str(request.url)
    ).first()
    
    if existing_recipe:
        return RecipeImportResponse(
            job_id=existing_job.id,
            status="completed",
            message="Recipe already exists!"
        )
    
    # Check for pending jobs
    existing_job = db.query(ImportJob).filter(
        ImportJob.source_url == str(request.url),
        ImportJob.status.in_(["queued", "processing"])
    ).first()
    
    if existing_job:
        return RecipeImportResponse(
            job_id=existing_job.id,
            status=existing_job.status,
            message="Already being processed"
        )
    
    # Enqueue new job
    job_id = await enqueue_recipe_import(
        user_id=user_id,
        source_url=str(request.url),
        fcm_token=request.fcm_token
    )
    
    # Create job record
    import_job = ImportJob(
        id=job_id,
        user_id=user_id,
        source_url=str(request.url),
        status="queued"
    )
    db.add(import_job)
    db.commit()
    
    return RecipeImportResponse(
        job_id=job_id,
        status="queued",
        message="Recipe import started"
    )
```

**Response**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Recipe import started"
}
```

**4. `GET /recipes?skip=0&limit=100`**
```python
@app.get("/recipes", response_model=List[RecipeResponse])
def list_recipes(skip: int = 0, limit: int = 100, db: Session):
    recipes = db.query(Recipe).order_by(
        Recipe.created_at.desc()
    ).offset(skip).limit(limit).all()
    return recipes
```

**Auto-Generated Docs**: `/docs` (Swagger UI)

**Startup**:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run**: `python -m app.main`

---

##### `worker.py`
**Location**: `/infra/app/`  
**Purpose**: **Background job processor**  
**Size**: 253 lines

**Role**: Consumes jobs from queue and processes them

**Class: `RecipeProcessor`**

**Main Method: `process_job(job_data)`**

**Process Flow** (30-40 seconds):
```
1. UPDATE STATUS: Mark job as "processing" in database

2. SCRAPE (5-10s):
   platform = get_platform(url)  # instagram, youtube, tiktok
   
   if platform == 'youtube':
       content = youtube_client.scrape_url(url)
   else:
       content = apify_client.scrape_url(url, platform)
   
   → Returns: video_url, caption, thumbnail_url, author

3. EXTRACT AI (15-20s):
   if content.video_url:
       video_path = download_video(content.video_url)
       recipe = openai_extractor.extract_from_video(
           video_path,
           content.caption,
           content.author
       )
   elif content.image_urls:
       recipe = openai_extractor.extract_from_images(
           content.image_urls,
           content.caption,
           content.author
)
   
   → Returns: RecipeData (title, ingredients, steps, times)

4. UPLOAD S3 (5-10s):
   try:
       thumbnail_s3 = s3_client.upload_from_url(
           content.thumbnail_url,
           f"recipes/{user_id}/{job_id}/thumbnail.jpg"
       )
       video_s3 = s3_client.upload_from_url(
           content.video_url,
           f"recipes/{user_id}/{job_id}/video.mp4"
       )
   except:
       # Graceful fallback
       thumbnail_s3 = content.thumbnail_url  # Original URL
       video_s3 = content.video_url

5. SAVE DATABASE:
   recipe = Recipe(
       user_id=user_id,
       title=recipe.title,
       description=content.caption,
       source_url=url,
       source_type=post_type,
       data=recipe.model_dump(),  # Full JSON
       thumbnail_url=thumbnail_s3,
       video_url=video_s3
   )
   db.add(recipe)
   db.commit()
   
   import_job.status = "completed"
   import_job.recipe_id = recipe.id
   db.commit()

6. NOTIFY:
   if fcm_token:
       fcm_client.send_recipe_ready_notification(
           fcm_token,
           recipe.id,
           recipe.title
       )
```

**Error Handling**:
```python
try:
    # Process job
except Exception as e:
    logger.error(f"Job failed: {e}")
    import_job.status = "failed"
    import_job.error_message = str(e)
    db.commit()
```

**Retry Logic**: `_scrape_with_retry()`
```python
for attempt in range(retry_attempts):  # 2 attempts
    try:
        return await apify_client.scrape_url(url, platform)
    except:
        if attempt < retry_attempts - 1:
            delay = retry_delay_seconds * (attempt + 1)  # 3s, 6s
            await asyncio.sleep(delay)
```

**Main Loop**: `run()`
```python
async def run(self):
    logger.info("🚀 Recipe worker started")
    fcm_client.initialize()
    
    while True:
        job_data = dequeue_recipe_import(timeout=5)
        
        if job_data:
            await self.process_job(job_data)
        else:
            await asyncio.sleep(2)  # No jobs, wait
```

**Startup**:
```python
if __name__ == "__main__":
    processor = RecipeProcessor()
    asyncio.run(processor.run())
```

**Run**: `python -m app.worker`

---

##### `config.py`
**Location**: `/infra/app/`  
**Purpose**: **Configuration management**  
**Size**: 48 lines

**Uses**: Pydantic Settings for type-safe env var loading

**Class: `Settings(BaseSettings)`**
```python
class Settings(BaseSettings):
    # API Keys
    apify_api_token: str
    gemini_api_key: str
    openai_api_key: str
    fcm_server_key: str
    
    # Database
    database_url: str
    
    # Queue
    redis_url: str
    
    # Storage
    aws_s3_bucket: str
    aws_region: str = "us-east-1"
    aws_access_key_id: str
    aws_secret_access_key: str
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    jwt_secret: str
    
    # Worker
    worker_concurrency: int = 4
    retry_attempts: int = 3
    retry_delay_seconds: int = 5
    
    # Test Mode
    test_mode: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

**Singleton Pattern**:
```python
@lru_cache()
def get_settings() -> Settings:
    return Settings()  # Cached
```

**Usage**:
```python
from app.config import get_settings
settings = get_settings()
print(settings.openai_api_key)
```

**Features**:
- Auto-loads from `.env`
- Type validation
- Default values
- Case-insensitive keys

---

##### `database.py`
**Location**: `/infra/app/`  
**Purpose**: **SQLAlchemy ORM models**  
**Size**: 49 lines

**Database Engine**:
```python
engine = create_engine(
    settings.database_url,  # PostgreSQL or SQLite
    connect_args={"check_same_thread": False} if SQLite else {}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

**Model 1: `Recipe`**

**Table**: `recipes`

```python
class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, index=True)
    title = Column(String)
    description = Column(String, nullable=True)  # Original post caption
    source_url = Column(String)  # Instagram/YouTube URL
    source_type = Column(String)  # 'instagram_reel', 'youtube_video', etc.
    data = Column(JSON)  # Full recipe JSON from AI
    thumbnail_url = Column(String, nullable=True)  # S3 or original URL
    video_url = Column(String, nullable=True)  # S3 or original URL
    created_at = Column(DateTime, default=datetime.utcnow)
    imported_at = Column(DateTime, default=datetime.utcnow)
```

**Example `data` Column** (JSON/JSONB):
```json
{
  "title": "Pasta Carbonara",
  "prep_time_minutes": 10,
  "cook_time_minutes": 20,
  "ingredients": [
    {"item": "spaghetti", "quantity": "400", "unit": "g"},
    {"item": "eggs", "quantity": "4", "unit": "whole"},
    {"item": "parmesan", "quantity": "100", "unit": "g"}
  ],
  "steps": [
    "Boil pasta in salted water",
    "Mix eggs and parmesan",
    "Combine pasta with egg mixture"
  ],
  "tags": ["Italian", "Pasta", "Quick"]
}
```

**Model 2: `ImportJob`**

**Table**: `import_jobs`

```python
class ImportJob(Base):
    __tablename__ = "import_jobs"
    
    id = Column(String, primary_key=True)  # UUID from API
    user_id = Column(String, index=True)
    source_url = Column(String)
    status = Column(String, default="processing")
        # Values: "queued", "processing", "completed", "failed"
    error_message = Column(String, nullable=True)
    recipe_id = Column(String, ForeignKey("recipes.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
```

**Status Flow**:
```
queued → processing → completed
                   → failed
```

**Table Creation**:
```python
# In main.py:
Base.metadata.create_all(bind=engine)
```

**Why JSONB (PostgreSQL)?**
- Flexible schema for different recipe formats
- Queryable: `SELECT * FROM recipes WHERE data->>'tags' @> '["Italian"]'`
- No rigid structure needed

---

##### `schemas.py`
**Location**: `/infra/app/`  
**Purpose**: **Pydantic models for validation**  
**Size**: 63 lines

**Models**:

**1. `Ingredient`**
```python
class Ingredient(BaseModel):
    item: str          # "spaghetti"
    quantity: str      # "400" (string to allow "2-3")
    unit: str          # "g", "cup", "tsp"
```

**2. `RecipeData`** (AI extraction output)
```python
class RecipeData(BaseModel):
    title: str
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    ingredients: List[Ingredient]
    steps: List[str]
    tags: List[str] = []
```

**3. `RecipeImportRequest`** (API input)
```python
class RecipeImportRequest(BaseModel):
    url: HttpUrl  # Pydantic validates URL format
    fcm_token: Optional[str] = None
```

**4. `RecipeImportResponse`** (API output)
```python
class RecipeImportResponse(BaseModel):
    job_id: UUID
    status: str = "processing"
    message: str = "Recipe import started..."
```

**5. `RecipeResponse`** (GET /recipes)
```python
class RecipeResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    source_url: str
    source_type: str
    data: RecipeData  # Nested model
    thumbnail_url: Optional[str]
    video_url: Optional[str]
    created_at: datetime
    imported_at: datetime
    
    class Config:
        from_attributes = True  # Allow ORM models
```

**6. `ScrapedContent`** (Scraper output)
```python
class ScrapedContent(BaseModel):
    video_url: Optional[str] = None
    caption: str = ""
    thumbnail_url: Optional[str] = None
    author: str = ""
    post_type: str = "reel"
    image_urls: List[str] = []
```

**Benefits**:
- Type safety
- Auto-validation
- Auto-generated API docs
- Clear contracts between components

---

##### `queue.py`
**Location**: `/infra/app/`  
**Purpose**: **Job queue (Redis or file-based)**  
**Size**: 126 lines

**Dual Mode**:
- **Redis** (production): `redis://localhost:6379`
- **File-based** (local): `queue_jobs.json`

**Mode Detection**:
```python
USE_REDIS = not settings.redis_url.startswith("memory://")

if USE_REDIS:
    import redis
    redis_client = redis.from_url(settings.redis_url)
```

**Queue Name**: `"eylo:recipe_import"`

**Function 1: `enqueue_recipe_import(user_id, source_url, fcm_token)`**

**Returns**: `job_id` (UUID string)

**Redis Mode**:
```python
job_id = str(uuid.uuid4())
job_data = {
    "job_id": job_id,
    "user_id": user_id,
    "source_url": source_url,
    "fcm_token": fcm_token
}
redis_client.rpush(RECIPE_QUEUE, json.dumps(job_data))
```

**File Mode**:
```python
jobs = _load_queue()  # Read queue_jobs.json
jobs.append(job_data)
_save_queue(jobs)  # Write queue_jobs.json
```

**Function 2: `dequeue_recipe_import(timeout=5)`**

**Returns**: Job dict or `None`

**Redis Mode** (blocking):
```python
result = redis_client.blpop(RECIPE_QUEUE, timeout=timeout)
if result:
    _, job_json = result
    return json.loads(job_json)
```

**File Mode** (polling):
```python
start_time = time.time()
while time.time() - start_time < timeout:
    jobs = _load_queue()
    if jobs:
        job = jobs.pop(0)
        _save_queue(jobs)
        return job
    time.sleep(0.5)  # Poll every 500ms
return None
```

**File Helpers** (multi-process safe):

**`_load_queue(retries=5)`**:
- Handles `PermissionError` (file locking)
- Retries with random sleep (100-300ms)
- Returns `[]` if file doesn't exist

**`_save_queue(jobs, retries=5)`**:
- Atomic write to `queue_jobs.json`
- Retry logic for locking

**Why File-Based?**
- ✅ No Redis dependency for local dev
- ✅ Works across processes (API + Worker)
- ✅ Persistent across restarts
- ❌ Not suitable for production (slow, no concurrency)

---

##### `utils.py`
**Location**: `/infra/app/`  
**Purpose**: **Helper utilities**  
**Size**: 41 lines

**Function 1: `get_platform(url: str) -> str`**

**Returns**: `'instagram'`, `'youtube'`, `'tiktok'`, or `'unknown'`

```python
def get_platform(url: str) -> str:
    url = url.lower()
    if 'instagram.com' in url:
        return 'instagram'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'tiktok.com' in url:
        return 'tiktok'
    return 'unknown'
```

**Examples**:
- `https://www.instagram.com/reel/ABC/` → `'instagram'`
- `https://youtube.com/watch?v=123` → `'youtube'`
- `https://youtu.be/123` → `'youtube'`
- `https://tiktok.com/@user/video/123` → `'tiktok'`

**Function 2: `get_post_type(url: str) -> str`**

**Returns**: `'reel'`, `'post'`, `'youtube_video'`, `'youtube_short'`, `'tiktok_video'`, etc.

```python
def get_post_type(url: str) -> str:
    platform = get_platform(url)
    
    if platform == 'instagram':
        if '/reel/' in url:
            return 'reel'
        elif '/tv/' in url:
            return 'tv'
        elif '/p/' in url:
            return 'post'
    elif platform == 'youtube':
        if '/shorts/' in url:
            return 'youtube_short'
        return 'youtube_video'
    elif platform == 'tiktok':
        return 'tiktok_video'
    
    return 'unknown'
```

**Function 3: `is_supported_url(url: str) -> bool`**
```python
def is_supported_url(url: str) -> bool:
    return get_platform(url) != 'unknown'
```

**Usage in Worker**:
```python
platform = get_platform(job.source_url)  # For scraper selection
post_type = get_post_type(job.source_url)  # For database
```

---

#### Services (`infra/app/services/`)

##### `__init__.py`
**Location**: `/infra/app/services/`  
**Purpose**: Package marker  
**Size**: 20 bytes

---

##### `apify_client.py`
**Location**: `/infra/app/services/`  
**Purpose**: **Scrape Instagram/TikTok using Apify**  
**Size**: 169 lines

**Class: `ApifyClient`**

**Actor IDs**:
```python
self.actors = {
    "instagram": "shu8hvrXbJbY3Eb9W",
    "youtube": "jefer/youtube-video-downloader",
    "tiktok": "clockworks/tiktok-scraper"
}
```

**Main Method: `scrape_url(url, platform)`**

**Returns**: `ScrapedContent` object

**Process** (30-60 seconds):
```
1. Get actor ID for platform
2. Construct platform-specific input
3. POST to Apify API to start run
4. Poll run status every 5s (max 180s)
5. Get dataset ID when completed
6. Fetch scraped items
7. Parse first item → ScrapedContent
```

**Example Flow**:
```python
# 1. Start run
run_response = await client.post(
    f"https://api.apify.com/v2/acts/{actor_id}/runs",
    params={"token": self.api_token},
    json=run_input
)
run_id = run_response.json()["data"]["id"]

# 2. Wait for completion
while status == "RUNNING":
    await asyncio.sleep(5)
    run = await client.get(f"/actor-runs/{run_id}")
    status = run["data"]["status"]

# 3. Get results
dataset_id = run["data"]["defaultDatasetId"]
items = await client.get(f"/datasets/{dataset_id}/items")

# 4. Parse
return _parse_scraped_item(items[0], platform)
```

**Platform-Specific Inputs**:

**Instagram**:
```python
{
    "directUrls": ["https://instagram.com/reel/ABC/"],
    "resultsType": "details",
    "resultsLimit": 1,
    "addParentData": False
}
```

**YouTube** (Apify):
```python
{
    "videos": ["https://youtube.com/watch?v=123"],
    "preferredQuality": "1080p",
    "preferredFormat": "mp4"
}
```

**TikTok**:
```python
{
    "startUrls": [{"url": "https://tiktok.com/@user/video/123"}],
    "resultsPerPage": 1
}
```

**Response Parsing**: `_parse_scraped_item(item, platform)`

**Instagram**:
```python
ScrapedContent(
    video_url=item.get("videoUrl") or item.get("video_url"),
    caption=item.get("caption", ""),
    thumbnail_url=item.get("displayUrl") or item.get("thumbnailUrl"),
    author=item.get("ownerUsername", ""),
    post_type=item.get("type", "reel"),
    image_urls=item.get("images", []) if post_type == "post" else []
)
```

**YouTube**:
```python
ScrapedContent(
    video_url=item.get("downloadUrl") or item.get("url"),
    caption=item.get("title") + "\n" + item.get("description"),
    thumbnail_url=item.get("thumbnailUrl"),
    author=item.get("channelName", ""),
    post_type="youtube_video"
)
```

**TikTok**:
```python
ScrapedContent(
    video_url=item.get("videoMeta", {}).get("downloadAddr"),
    caption=item.get("text", ""),
    thumbnail_url=item.get("imageUrl"),
    author=item.get("authorMeta", {}).get("name", ""),
    post_type="tiktok_video"
)
```

**Error Handling**:
- Timeout if run exceeds 180s
- Raises exception if run fails
- Logs all errors

**Singleton**: `apify_client = ApifyClient()`

**Cost**: ~$0.01 per scrape (Apify pricing)

---

##### `youtube_client.py`
**Location**: `/infra/app/services/`  
**Purpose**: **YouTube scraper using yt-dlp** (Alternative to Apify)  
**Size**: 54 lines

**Class: `YouTubeClient`**

**Why yt-dlp?**
- ✅ Faster than Apify (no queue wait)
- ✅ Free (no API costs)
- ✅ Direct video URL
- ❌ May break if YouTube changes

**Configuration**:
```python
self.ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'format': 'best[ext=mp4]/best'  # Prefer MP4
}
```

**Main Method: `scrape_url(url)`**

**Returns**: `ScrapedContent`

**Process** (5-10 seconds):
```python
# Extract metadata (no download)
info = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)

return ScrapedContent(
    video_url=info.get("url"),  # Direct MP4 link
    caption=info.get("title") + "\n" + info.get("description"),
    thumbnail_url=info.get("thumbnail"),
    author=info.get("uploader"),
    post_type="youtube_video"
)
```

**Info Dict Contains**:
- `url`: Direct video URL
- `title`: Video title
- `description`: Full description
- `thumbnail`: Best thumbnail URL
- `uploader`: Channel name
- `duration`: Seconds
- `view_count`: Views

**Singleton**: `youtube_client = YouTubeClient()`

---

##### `openai_extractor.py`
**Location**: `/infra/app/services/`  
**Purpose**: **AI recipe extraction using OpenAI GPT-4o-mini**  
**Size**: 188 lines

**⭐ PRIMARY AI EXTRACTOR**

**Class: `OpenAIRecipeExtractor`**

**Model**: `gpt-4o-mini` (vision-capable)

**Initialization**:
```python
def __init__(self):
    self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    self.model = "gpt-4o-mini"
```

**Method 1: `extract_from_video(video_path, caption, author)`**

**Returns**: `RecipeData`

**Process** (15-20 seconds):
```
1. Extract 20 frames from video → base64 strings
2. Construct prompt with caption/author
3. Send to OpenAI API (frames + prompt)
4. Parse JSON response → RecipeData
```

**Frame Extraction**: `_extract_frames(video_path, max_frames=20)`

**Uses OpenCV**:
```python
video = cv2.VideoCapture(video_path)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
interval = max(1, total_frames // max_frames)  # Sample evenly

base64_frames = []
count = 0

while video.isOpened() and len(base64_frames) < max_frames:
    success, frame = video.read()
    if not success:
        break
    
    if count % interval == 0:
        # Resize to 512px (reduce token cost)
        height, width = frame.shape[:2]
        if width > 512 or height > 512:
            scaling_factor = 512 / max(width, height)
            frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor)
        
        # Encode to JPEG base64
        _, buffer = cv2.imencode(".jpg", frame)
        base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
    
    count += 1

video.release()
return base64_frames  # List of 20 base64 strings
```

**API Call**:
```python
messages = [
    {
        "role": "system",
        "content": "You are a professional chef and recipe extractor. Extract structured recipe data from this Instagram video. Output strictly valid JSON."
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame1}"}},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame2}"}},
            # ... 20 frames total
        ]
    }
]

response = await self.client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    response_format={"type": "json_object"},  # Force JSON
    max_tokens=2000
)

content = response.choices[0].message.content
```

**Prompt**: `_create_prompt(caption, author)`
```python
f"""
Analyze this social media content (Chef/Creator: {author}).
Caption: "{caption}"

Extract the following JSON structure:
{{
    "title": "Recipe Title",
    "prep_time_minutes": 15,
    "cook_time_minutes": 30,
    "ingredients": [
        {{"item": "ingredient name", "quantity": "amount", "unit": "unit"}}
    ],
    "steps": ["Step 1", "Step 2"],
    "tags": ["tag1", "tag2"]
}}

Rules:
1. If ingredients are missing quantities, estimate them from visual cues.
2. Infer missing steps if the visual flow implies them.
3. If it's not a recipe, return a best-guess recipe for the dish shown.
"""
```

**Response Parsing**: `_parse_response(content)`
```python
data = json.loads(content)

return RecipeData(
    title=data.get("title", "Untitled Recipe"),
    prep_time_minutes=data.get("prep_time_minutes"),
    cook_time_minutes=data.get("cook_time_minutes"),
    ingredients=[Ingredient(**i) for i in data.get("ingredients", [])],
    steps=data.get("steps", []),
    tags=data.get("tags", [])
)
```

**Method 2: `extract_from_images(image_urls, caption, author)`**

**For Instagram Posts** (no video, just images)

**Process**:
```python
messages = [
    {
        "role": "system",
        "content": "You are a professional chef. Extract structured recipe data from these images. Output strictly valid JSON."
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": img_url1}},
            {"type": "image_url", "image_url": {"url": img_url2}},
            # ... up to 5 images
        ]
    }
]

response = await self.client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    response_format={"type": "json_object"},
    max_tokens=2000
)
```

**Cost Breakdown**:
- Input: 20 frames @ 512px ≈ 8,000 tokens
- Output: Recipe JSON ≈ 500 tokens
- **Total**: ~$0.02-0.05 per recipe

**Why OpenAI over Gemini?**
- ✅ Better frame understanding
- ✅ More consistent JSON output
- ✅ Better prompt adherence
- ✅ Structured output mode

**Singleton**: `openai_extractor = OpenAIRecipeExtractor()`

---

##### `gemini_extractor.py`
**Location**: `/infra/app/services/`  
**Purpose**: **Legacy AI extractor using Google Gemini 1.5 Pro**  
**Size**: 218 lines  
**Status**: **DEPRECATED** (replaced by OpenAI)

**Still Available**: Can switch back by changing imports in `worker.py`

**Why Deprecated?**
- Gemini has less consistent JSON output
- OpenAI better at structured extraction
- Gemini video upload is slower

**If Re-enabling**:
```python
# In worker.py, change:
from app.services.openai_extractor import openai_extractor
# To:
from app.services.gemini_extractor import gemini_extractor

# Then use:
recipe = await gemini_extractor.extract_from_video(...)
```

---

##### `s3_client.py`
**Location**: `/infra/app/services/`  
**Purpose**: **Upload media to AWS S3**  
**Size**: 117 lines

**Class: `S3Client`**

**Initialization**:
```python
def __init__(self):
    self.bucket = settings.aws_s3_bucket
    
    if not settings.test_mode:
        self.s3 = boto3.client(
            's3',
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
```

**Method 1: `upload_file(file_path, s3_key, content_type)`**

**Upload local file to S3**

```python
self.s3.upload_file(
    file_path,              # /tmp/video.mp4
    self.bucket,            # eylo-recipes
    s3_key,                 # recipes/user123/job456/video.mp4
    ExtraArgs={
        'ContentType': content_type,    # video/mp4
        'ACL': 'public-read'            # Make public
    }
)

url = f"https://{self.bucket}.s3.{self.aws_region}.amazonaws.com/{s3_key}"
return url
```

**Returns**: `https://eylo-recipes.s3.us-east-1.amazonaws.com/recipes/user123/job456/video.mp4`

**Method 2: `upload_from_url(url, s3_key, content_type)`**

**Download from URL then upload to S3**

**Process**:
```python
# 1. Download to temp file
async with httpx.AsyncClient() as client:
    response = await client.get(url, follow_redirects=True)
    response.raise_for_status()
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

# 2. Upload to S3
result = await self.upload_file(tmp_path, s3_key, content_type)

# 3. Clean up
Path(tmp_path).unlink()

return result
```

**Usage in Worker**:
```python
try:
    thumbnail_s3 = await s3_client.upload_from_url(
        scraped_content.thumbnail_url,
        f"recipes/{user_id}/{job_id}/thumbnail.jpg",
        "image/jpeg"
    )
    thumbnail_url = thumbnail_s3
except Exception as e:
    logger.warning(f"S3 upload failed: {e}")
    thumbnail_url = scraped_content.thumbnail_url  # Fallback
```

**Graceful Degradation**: Falls back to original URLs if S3 fails

**Test Mode**:
```python
if settings.test_mode:
    return f"https://mock-s3.local/{bucket}/{s3_key}"
```

**S3 Key Format**: `recipes/{user_id}/{job_id}/{filename}`

**Singleton**: `s3_client = S3Client()`

---

##### `fcm_client.py`
**Location**: `/infra/app/services/`  
**Purpose**: **Send push notifications via Firebase Cloud Messaging**  
**Size**: 91 lines

**Class: `FCMClient`**

**Initialization**:
```python
def __init__(self):
    self.server_key = settings.fcm_server_key
    self.initialized = False

def initialize(credential_path=None):
    if credential_path:
        cred = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(cred)
    else:
        firebase_admin.initialize_app()
    self.initialized = True
```

**Main Method: `send_recipe_ready_notification(fcm_token, recipe_id, recipe_title)`**

**Returns**: `True` if successful

**Message Structure**:
```python
message = messaging.Message(
    # Notification (visible UI)
    notification=messaging.Notification(
        title="Recipe Ready! 🍝",
        body=f"'{recipe_title}' has been imported to your collection"
    ),
    
    # Data payload (for app logic)
    data={
        "type": "recipe_imported",
        "recipe_id": str(recipe_id),
        "deep_link": f"eylo://recipe/{recipe_id}"
    },
    
    # Device token
    token=fcm_token,
    
    # Android-specific config
    android=messaging.AndroidConfig(
        priority="high",
        notification=messaging.AndroidNotification(
            icon="ic_recipe",
            color="#FF6B35",
            sound="default"
        )
    ),
    
    # iOS-specific config
    apns=messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(
                sound="default",
                badge=1,
                category="RECIPE_READY"
            )
        )
    )
)

response = messaging.send(message)
logger.info(f"FCM notification sent: {response}")
return True
```

**Deep Link**: `eylo://recipe/{recipe_id}`
- When user taps notification
- App opens to recipe detail screen

**Usage in Worker**:
```python
if fcm_token:
    await fcm_client.send_recipe_ready_notification(
        fcm_token,
        recipe.id,
        recipe.title
    )
```

**Error Handling**:
```python
try:
    messaging.send(message)
except Exception as e:
    logger.error(f"FCM send failed: {e}")
    return False
```

**Singleton**: `fcm_client = FCMClient()`

---

#### Test Files

##### `test_api.py`
**Purpose**: Test API endpoints  
**Size**: 1,686 bytes

**Tests**:
1. `GET /health` - Health check
2. `POST /import/recipe` - Import test recipe
3. `GET /recipes` - List recipes

**Run**: `python test_api.py`

---

##### `test_real_reel.py`
**Purpose**: Test with real Instagram Reel  
**Size**: 958 bytes

**Process**:
1. POST real Instagram URL
2. Print job ID
3. User checks database manually

---

##### `test_openai_extraction.py`
**Purpose**: Test OpenAI extraction in isolation  
**Size**: 2,049 bytes

**Process**:
1. Download video
2. Extract frames
3. Call OpenAI
4. Print recipe JSON

**Run**: `python test_openai_extraction.py`

---

##### `check_db.py`
**Purpose**: Check database contents  
**Size**: 1,282 bytes

**Prints**:
- Total recipes
- Recent 5 recipes (title, source_url, created_at)
- Total import jobs

**Run**: `python check_db.py`

---

##### `check_db_detailed.py`
**Purpose**: Detailed database inspection  
**Size**: 1,336 bytes

**Prints**: Full recipe objects with all fields including `data` JSON

---

##### `manual_test.py`
**Purpose**: Manual end-to-end test  
**Size**: 1,883 bytes

**Tests full flow without API server**

---

##### `test_queue_write.py`
**Purpose**: Test queue operations  
**Size**: 684 bytes

**Tests**: Enqueue and dequeue

---

#### Batch Scripts (Windows)

##### `start_server.bat`
```batch
@echo off
cd c:\Users\shegd\OneDrive\Desktop\eylo_project2\infra
.\venv\Scripts\Activate.ps1
python -m app.main
```

##### `run_tests.bat`
```batch
@echo off
.\venv\Scripts\Activate.ps1
python test_api.py
python check_db.py
```

##### `test_full_flow.bat`
```batch
# Start API + Worker + Tests
```

---

#### Data Files

##### `queue_jobs.json`
**Purpose**: File-based job queue (local dev)  
**Format**: JSON array

```json
[
  {
    "job_id": "uuid",
    "user_id": "uuid",
    "source_url": "https://...",
    "fcm_token": "..."
  }
]
```

**Auto-created**, gitignored

---

##### `eylo_test.db`
**Purpose**: SQLite database (local dev)  
**Tables**: `recipes`, `import_jobs`

**Auto-created** by SQLAlchemy, gitignored

---

##### `last_apify_run.json`
**Purpose**: Cached Apify response for debugging  
**Contains**: Last scraped data

---

### 📍 Mobile Directory (`mobile/`)

#### iOS Files (`mobile/ios/`)

##### `EyloShare/ShareViewController.swift`
**Purpose**: iOS Share Extension controller

**Key Methods**:
- `viewDidLoad()`: Initialize
- `extractURL()`: Get URL from share sheet
- `sendToAPI()`: POST to backend
- `showToast()`: User feedback
- `completeRequest()`: Close extension

---

##### `Info.plist`
**Purpose**: Share Extension metadata

**Key Settings**:
- `NSExtensionActivationRule`: Instagram/YouTube URL patterns
- `CFBundleDisplayName`: "Save to Eylo"

---

#### Android Files (`mobile/android/`)

##### `ShareActivity.kt`
**Purpose**: Handle share intent

**Process**:
1. Extract URL from intent
2. Enqueue WorkManager job
3. Show toast
4. Close activity

---

##### `RecipeImportWorker.kt`
**Purpose**: Background worker

**Process**:
1. Get URL from input data
2. GET auth token
3. POST to API
4. Return success/retry

---

##### `ApiService.kt`
**Purpose**: Retrofit API interface

```kotlin
interface ApiService {
    @POST("/import/recipe")
    suspend fun importRecipe(@Body request: RecipeImportRequest)
    
    @GET("/recipes")
    suspend fun getRecipes(): List<Recipe>
}
```

---

##### `AndroidManifest.xml`
**Purpose**: App manifest

**Share Intent Filter**:
```xml
<activity android:name=".ShareActivity">
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
    </intent-filter>
</activity>
```

---

## 💻 Technology Stack

### Backend
- **FastAPI**: HTTP API framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: ORM
- **PostgreSQL/SQLite**: Database
- **Redis**: Job queue
- **OpenAI GPT-4o-mini**: AI extraction
- **Apify**: Instagram/TikTok scraping
- **yt-dlp**: YouTube scraping
- **boto3**: AWS S3 client
- **firebase-admin**: Push notifications
- **OpenCV**: Video frame extraction

### Mobile
- **iOS**: Swift, Share Extension
- **Android**: Kotlin, WorkManager, Retrofit

---

## 🔄 Data Flow

```
1. User shares Instagram Reel
   ↓
2. Share Extension extracts URL
   ↓
3. POST /import/recipe
   ↓
4. API creates job & enqueues
   ↓
5. Returns job_id immediately
   ↓
6. Extension shows "Recipe importing!" toast
   ↓
7. Extension closes (< 2s total)
   ↓
8. Worker dequeues job
   ↓
9. Scrape with Apify (5-10s)
   → video_url, caption, thumbnail, author
   ↓
10. Download video temporarily
   ↓
11. Extract 20 frames with OpenCV
   ↓
12. Send to OpenAI GPT-4o-mini (15-20s)
   → Structured recipe JSON
   ↓
13. Upload media to S3 (5-10s)
   → S3 URLs
   ↓
14. Save recipe to PostgreSQL
   → Recipe + ImportJob records
   ↓
15. Send FCM push notification
   ↓
16. User receives "Recipe Ready! 🍝"
   ↓
17. User taps → App opens to recipe
```

**Total Time**: 30-40 seconds

---

## 🚀 Deployment

### Local Development
```bash
cd infra
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.main        # Terminal 1
python -m app.worker      # Terminal 2
```

### Docker
```bash
docker-compose up -d
docker-compose logs -f
```

### Production
1. Deploy to AWS EC2 / DigitalOcean
2. Use Supabase for PostgreSQL
3. Use Redis Cloud for queue
4. Configure `.env` with production values
5. Run with Docker Compose

---

## 📊 File Statistics

**Backend Code**:
- Total Python files: 15
- Lines of code: ~2,000
- Test files: 7

**Configuration**:
- Environment files: 3
- Docker files: 2
- Documentation: 6 markdown files

**Services**:
- Scrapers: 2
- AI extractors: 2
- Storage: 1 (S3)
- Notifications: 1 (FCM)

---

**Last Updated**: February 2026  
**Project Version**: 2.0  
**Built with ❤️ for Eylo**
