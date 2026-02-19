# Eylo Project 2 - Recipe Import Backend

Backend service for extracting recipes from social media (Instagram, TikTok, YouTube) using AI.

## Features
- **Scraping**: Fetches content from social media URLs using Apify and yt-dlp.
- **AI Extraction**: Uses OpenAI GPT-4o-mini to parse video/text into structured recipe data.
- **Queue System**: Supports Redis or Database-backed job queue for background processing.
- **API**: FastAPI endpoints for submitting URLs and retrieving recipes.

## Prerequisites
- Python 3.10+
- (Optional) Redis server

## Setup

1.  **Create and Activate Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Configuration**
    Copy `.env.example` to `.env` and fill in your keys:
    ```bash
    cp .env.example .env
    ```
    - **Database**: Set `DATABASE_URL`.
    - **Queue**: Set `REDIS_URL=memory://` to use the database as a queue (simple setup), or a real Redis URL for production.

## Running the Application

### 1. Start the API Server
The API handles incoming requests and manages the database.
```bash
python -m uvicorn app.main:app --reload
```
API Docs available at: `http://localhost:8000/docs`

### 2. Start the Background Worker
The worker processes queued jobs to scrape and extract recipes.
```bash
python -m app.worker
```

### 3. Usage
You can test the import process using the manual script:
```bash
python manual_import.py
```
Enter a URL (e.g., Instagram Reel) when prompted.

## Project Structure
- `app/`: Main application code.
    - `main.py`: API entry point.
    - `worker.py`: Background worker entry point.
    - `queue.py`: Queue logic (Redis or DB polling).
    - `agent/`: AI and Scraping logic.
- `manual_import.py`: CLI tool for testing.

## Detailed Documentation
For a deep dive into the code flow and file structure, please read [explain.md](explain.md).
