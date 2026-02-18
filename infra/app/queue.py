import json
import uuid
import time
from typing import Dict, Any, Optional
from pathlib import Path
from app.config import get_settings

settings = get_settings()

# Minimal file-based queue for local dev without Redis
QUEUE_FILE = Path(__file__).parent.parent / "queue_jobs.json"
RECIPE_QUEUE = "eylo:recipe_import"

# Check for Redis availability
USE_REDIS = not settings.redis_url.startswith("memory://")
if USE_REDIS:
    try:
        import redis
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        redis_client.ping()
    except Exception:
        print("⚠️ Redis unavailable, using file queue")
        USE_REDIS = False

async def enqueue_recipe_import(user_id: str, source_url: str) -> str:
    """Add a recipe import job to the queue"""
    job_id = str(uuid.uuid4())
    job_data = {
        "job_id": job_id, 
        "user_id": user_id, 
        "source_url": source_url, 

        "created_at": time.time()
    }
    
    if USE_REDIS:
        redis_client.lpush(RECIPE_QUEUE, json.dumps(job_data))
    else:
        # Minimal file queue
        try:
            current_jobs = json.loads(QUEUE_FILE.read_text()) if QUEUE_FILE.exists() else []
        except:
            current_jobs = []
        current_jobs.append(job_data)
        QUEUE_FILE.write_text(json.dumps(current_jobs))
    
    return job_id

def dequeue_recipe_import() -> Optional[Dict[str, Any]]:
    """Get next job from queue"""
    if USE_REDIS:
        item = redis_client.rpop(RECIPE_QUEUE)
        return json.loads(item) if item else None
    
    # Minimal file queue pop
    if not QUEUE_FILE.exists(): return None
    try:
        jobs = json.loads(QUEUE_FILE.read_text())
        if not jobs: return None
        job = jobs.pop(0)
        QUEUE_FILE.write_text(json.dumps(jobs))
        return job
    except: return None
