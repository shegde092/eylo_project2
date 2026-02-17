# Eylo Recipe Import Backend

The backend infrastructure for **Eylo**, a mobile application that imports and digitizes recipes from social media content (Instagram, TikTok, YouTube).

## 📖 Overview

This system allows users to share a recipe video link from social media directly to the Eylo app. The backend asynchronously processes this link to:
1.  **Scrape** the content (video URL, caption, author) using Apify or yt-dlp.
2.  **Extract** structured recipe data (ingredients, steps, preparation time) using **OpenAI GPT-4o-mini**.
3.  **Store** the digitized recipe in a PostgreSQL database (Supabase).
4.  **Notify** the user via Firebase Cloud Messaging (FCM) when the import is complete.

**Key Features:**
- 🚀 **Asynchronous "Fire-and-Forget" Architecture:** Ensures instant responsiveness for the mobile client.
- 🤖 **AI-Powered Extraction:** Converts unstructured video/text into machine-readable JSON.
- 📱 **Cross-Platform Support:** Handles Instagram Reels, TikTok Videos, and YouTube Shorts.

---

## 🏗️ Architecture

The system is composed of three main components:

| Component | File | Description |
|:---|:---|:---|
| **API Gateway** | `app/main.py` | FastAPI server that accepts import requests and enqueues jobs. |
| **Task Queue** | `app/queue.py` | Manages background jobs (uses Redis in production, in-memory for local dev). |
| **Worker** | `app/worker.py` | Background process that handles scraping, AI extraction, and database storage. |

### Data Flow
1.  **Mobile App** sends URL -> **API**
2.  **API** pushes job to **Queue** -> returns `job_id`
3.  **Worker** pulls job -> Scrapes Content -> Calls OpenAI -> Saves to DB
4.  **Worker** sends Push Notification -> **Mobile App**

---

## 🛠️ Prerequisites

- **Python 3.11+**
- **PostgreSQL Database** (e.g., Supabase)
- **API Keys**:
    - **OpenAI** (for GPT-4o-mini)
    - **Apify** (for Instagram/TikTok scraping)
    - **Firebase** (optional, for push notifications)

---

## ⚡ Quick Start (Local Development)

### 1. Setup Environment

```bash
# Clone the repository and navigate to infra folder
cd infra

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
# source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the `infra` directory with your API keys:

```bash
cp .env.example .env
```

**Required `.env` Variables:**
```ini
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# API Keys
OPENAI_API_KEY=sk-...
APIFY_API_TOKEN=apify_...

# Server
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Run the System

You must run the API Server and the Worker in **separate terminals**.

**Terminal 1: API Server**
```bash
python -m app.main
```

**Terminal 2: Background Worker**
```bash
python -m app.worker
```

---

## 🧪 Testing & Verification

1.  **Health Check:**
    ```bash
    curl http://localhost:8000/health
    ```

2.  **Trigger an Import:**
    ```bash
    curl -X POST http://localhost:8000/import/recipe \
      -H "Content-Type: application/json" \
      -d '{"url": "https://www.instagram.com/reel/C8..."}'
    ```

3.  **Monitor Progress:**
    Watch the **Worker Terminal**. You should see:
    > - `[INFO] Scraped content from instagram`
    > - `[INFO] OpenAI raw response: ...`
    > - `[INFO] Completed: Chocolate Cake`

---

## 📝 API Endpoints

| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/` | Service root/status |
| `GET` | `/health` | Kubernetes/Docker health check |
| `POST` | `/import/recipe` | Submit a URL for processing |
| `GET` | `/recipes` | Retrieve list of saved recipes |

---

## 📦 Deployment (Docker)

To run the entire stack (API + Worker) using Docker Compose:

```bash
# Build and Start
docker-compose up -d --build

# View Logs
docker-compose logs -f
```

---

## 📄 License

This project is licensed under the MIT License.
