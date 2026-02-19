from typing import Dict, Any, Optional
import json
import time
from sqlalchemy.orm import Session
from app.database import SessionLocal, ImportJob
from app.config import get_settings

settings = get_settings()

RECIPE_QUEUE = "eylo:recipe_import"

# Check for Redis availability
USE_REDIS = not settings.redis_url.startswith("memory://")
if USE_REDIS:
    try:
        import redis
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        redis_client.ping()
    except Exception:
        print("⚠️ Redis unavailable, using DB queue")
        USE_REDIS = False
else:
    redis_client = None

async def enqueue_recipe_import(job_id: str, user_id: str, source_url: str) -> str:
    """Add a recipe import job to the queue"""
    job_data = {
        "job_id": job_id,
        "user_id": user_id,
        "source_url": source_url,
        "created_at": time.time()
    }
    
    if USE_REDIS and redis_client:
        redis_client.lpush(RECIPE_QUEUE, json.dumps(job_data))
    
    # If using DB Queue (no Redis), the job is already inserted in 'queued' status by main.py
    # so we don't need to do anything here.
    
    return job_id

def dequeue_recipe_import() -> Optional[Dict[str, Any]]:
    """Get next job from queue"""
    if USE_REDIS and redis_client:
        item = redis_client.rpop(RECIPE_QUEUE)
        return json.loads(item) if item else None
    
    # DB Polling Queue
    db: Session = SessionLocal()
    try:
        # Transactional fetch: find oldest queued job and lock it/mark as processing
        # Simple implementation: fetch first, then update. 
        # For higher concurrency, consider SELECT FOR UPDATE.
        job = db.query(ImportJob).filter(ImportJob.status == "queued").order_by(ImportJob.created_at.asc()).first()
        
        if job:
            job.status = "processing"
            db.commit()
            
            return {
                "job_id": job.id,
                "user_id": job.user_id,
                "source_url": job.source_url,
                "created_at": job.created_at.timestamp() if job.created_at else time.time()
            }
            
        return None
    except Exception as e:
        print(f"Error polling DB queue: {e}")
        return None
    finally:
        db.close()
