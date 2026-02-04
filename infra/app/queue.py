import json
import uuid
import os
import time
import random
from typing import Dict, Any, Optional
from pathlib import Path
from app.config import get_settings

settings = get_settings()

# File-based queue for local testing (works across processes!)
QUEUE_FILE = Path(__file__).parent.parent / "queue_jobs.json"

# Check if we should use Redis or file-based queue
USE_REDIS = not settings.redis_url.startswith("memory://")

if USE_REDIS:
    try:
        import redis
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        redis_client.ping()  # Test connection
    except:
        print("⚠️  Redis not available, using file-based queue")
        USE_REDIS = False

# Queue name
RECIPE_QUEUE = "eylo:recipe_import"


def _load_queue(retries=5):
    """Load jobs from file with retries"""
    if not QUEUE_FILE.exists():
        return []
        
    for attempt in range(retries):
        try:
            with open(QUEUE_FILE, 'r') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (PermissionError, json.JSONDecodeError):
            if attempt < retries - 1:
                time.sleep(0.1 + random.random() * 0.2)  # Random sleep 100-300ms
            else:
                return []
    return []


def _save_queue(jobs, retries=5):
    """Save jobs to file with retries"""
    for attempt in range(retries):
        try:
            with open(QUEUE_FILE, 'w') as f:
                json.dump(jobs, f)
            return
        except PermissionError:
            if attempt < retries - 1:
                time.sleep(0.1 + random.random() * 0.2)
            else:
                print(f"[ERROR] Failed to save queue after {retries} attempts")


async def enqueue_recipe_import(user_id: str, source_url: str, fcm_token: str = None) -> str:
    """
    Add a recipe import job to the queue
    
    Args:
        user_id: UUID of the user
        source_url: Instagram URL
        fcm_token: Optional FCM token for push notifications
        
    Returns:
        job_id: UUID of the created job
    """
    job_id = str(uuid.uuid4())
    
    job_data = {
        "job_id": job_id,
        "user_id": user_id,
        "source_url": source_url,
        "fcm_token": fcm_token
    }
    
    if USE_REDIS:
        # Push to Redis list (queue)
        redis_client.rpush(RECIPE_QUEUE, json.dumps(job_data))
    else:
        # Push to file-based queue (works across processes!)
        jobs = _load_queue()
        jobs.append(job_data)
        _save_queue(jobs)
        print(f"[OK] Job {job_id} added to queue (file-based)")
    
    return job_id


def dequeue_recipe_import(timeout: int = 5) -> Optional[Dict[str, Any]]:
    """
    Get next job from queue (blocking)
    
    Returns:
        Job data dictionary or None if timeout
    """
    if USE_REDIS:
        # BLPOP blocks until an item is available
        result = redis_client.blpop(RECIPE_QUEUE, timeout=timeout)
        if result:
            _, job_json = result
            return json.loads(job_json)
        return None
    else:
        # Pop from file-based queue with polling
        start_time = time.time()
        while time.time() - start_time < timeout:
            jobs = _load_queue()
            if jobs:
                job = jobs.pop(0)
                _save_queue(jobs)
                print(f"[OK] Job {job['job_id']} dequeued from file")
                return job
            # Wait a bit before checking again
            time.sleep(0.5)
        return None
