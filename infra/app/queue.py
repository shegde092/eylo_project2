import json
import uuid
from typing import Dict, Any, Optional
from collections import deque
from app.config import get_settings

settings = get_settings()

# In-memory queue for local testing (when Redis not available)
_memory_queue = deque()

# Check if we should use Redis or in-memory queue
USE_REDIS = not settings.redis_url.startswith("memory://")

if USE_REDIS:
    try:
        import redis
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        redis_client.ping()  # Test connection
    except:
        print("⚠️  Redis not available, using in-memory queue")
        USE_REDIS = False

# Queue name
RECIPE_QUEUE = "eylo:recipe_import"


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
        # Push to in-memory queue
        _memory_queue.append(job_data)
    
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
        # Pop from in-memory queue
        if _memory_queue:
            return _memory_queue.popleft()
        return None
