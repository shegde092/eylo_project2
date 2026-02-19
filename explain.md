# Eylo Project Flow Explanation

This document details the step-by-step execution flow of the Eylo backend, from the moment a URL is submitted to when a recipe is saved.

## 1. Input: Submitting the URL
The process begins when a user (or the `manual_import.py` script) sends a POST request to the API.

- **Endpoint**: `POST /import/recipe`
- **Payload**: `{"url": "https://www.instagram.com/reel/..."}`
- **Handler**: `app.main.import_recipe`

### What happens in `import_recipe`:
1.  **Validation**: It cleans the URL (removes query parameters).
2.  **Duplicate Check**: It checks the database (`Recipe` table) to see if this URL was already imported. If yes, it returns the existing data.
3.  **Job Creation**: It checks the `ImportJob` table.
    - If a job is already `queued` or `processing`, it returns that job ID.
    - If not, it creates a **new** `ImportJob` in the database with status `queued`.
4.  **Response**: Returns the `job_id` to the client immediately. The client can now poll for updates.

## 2. Queueing Strategy
The system uses the `import_jobs` database table as a queue (when Redis is disabled).

- **Queued State**: The API has inserted a row in `ImportJob` with `status="queued"`.
- **Worker Polling**: The background worker (`app.worker`) is running in a separate process/terminal.

## 3. Worker Processing
The worker (`app/worker.py`) runs an infinite loop managed by `app.queue.dequeue_recipe_import`.

### Polling Logic (`app/queue.py`):
1.  It queries the `ImportJob` table for the oldest job where `status == "queued"`.
2.  **Locking**: If it finds one, it immediately updates the status to `processing`.
3.  It returns the job data (`url`, `job_id`) to the worker.

### Execution Logic (`app/agent/recipe_agent.py`):
The worker passes the job to `RecipeAgent.process_job`.

#### Step A: Scraping (`app/agent/tools/scraping.py`)
- The agent determines the platform (Instagram, TikTok, YouTube).
- **Instagram/TikTok**: Uses `ApifyClient` to call an Apify Actor. This downloads metadata (caption, author) and the video file URL.
- **YouTube**: Uses `yt-dlp` to extract video info.
- **Result**: A `ScrapedContent` object containing video URL, caption, and author.

#### Step B: Extraction (`app/agent/tools/extraction.py`)
- The agent downloads the video (or images) to a temporary file.
- **OpenAI Call**: It sends frames from the video + the caption to GPT-4o-mini.
- **Prompt**: "Extract structured recipe data... Return JSON with title, ingredients, steps..."
- **Result**: A `RecipeData` object with structured ingredients and instructions.

#### Step C: Saving (`app/agent/recipe_agent.py`)
1.  **Save Recipe**: A new row is added to the `Recipe` table with the extracted JSON data.
2.  **Update Job**: The `ImportJob` is updated:
    - `status` → `completed`
    - `recipe_id` → Linked to the new Recipe.

## 4. Final Result
The client (who was holding the `job_id`) can now see that the job is `completed`. They can fetch the final recipe using:
- `GET /recipes`



## 5. Project File Structure

### Root Directory
- **`app/`**: Main application source code.
- **`manual_import.py`**: A CLI script to trigger the import process manually for testing.
- **`requirements.txt`**: List of Python dependencies.
- **`.env`**: Configuration file for API keys and database URL.
- **`README.md`**: Setup and usage instructions.

### App Directory (`app/`)
- **`main.py`**: The entry point for the FastAPI server. Defines routes (`/import/recipe`, `/recipes`).
- **`worker.py`**: The entry point for the background worker. Runs the infinite polling loop.
- **`queue.py`**: Handles queue logic. Switches between Redis (if configured) and DB Polling (default).
- **`database.py`**: Setup for SQLAlchemy database connection and `SessionLocal`.
- **`models.py`** (merged into `database.py`): Defines `Recipe` and `ImportJob` tables.
- **`schemas.py`**: Pydantic models for request/response validation (e.g., `RecipeData`).
- **`config.py`**: Loads settings from `.env` using Pydantic Settings.
- **`utils.py`**: Helper functions for URL parsing and platform detection.

### Agent Directory (`app/agent/`)
- **`recipe_agent.py`**: The core logic coordinator. Orchestrates scraping -> extraction -> saving.
- **`tools/`**:
    - **`scraping.py`**: Routes URLs to the correct scraper (Apify or YouTube).
    - **`extraction.py`**: Handles downloading media and calling OpenAI.
    - **`base.py`**: Abstract base class for tools.

### Services Directory (`app/services/`)
- **`apify_client.py`**: Wrapper for Apify API to scrape Instagram/TikTok.
- **`youtube_client.py`**: Wrapper for `yt-dlp` to scrape YouTube.
- **`openai_extractor.py`**: logic to extract frames from video and query OpenAI GPT-4o.
