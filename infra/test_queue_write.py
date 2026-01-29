"""Direct test of queue writing"""
import sys
sys.path.insert(0, 'C:\\Users\\shegd\\OneDrive\\Desktop\\eylo_project2\\infra')

import asyncio
from app.queue import enqueue_recipe_import
import json

async def test():
    print("Testing queue write...")
    job_id = await enqueue_recipe_import(
        user_id="test-user-123",
        source_url="https://www.instagram.com/reel/test/",
        fcm_token=None
    )
    print(f"Job ID: {job_id}")
    
    # Check file
    with open('queue_jobs.json', 'r') as f:
        jobs = json.load(f)
    print(f"Jobs in file: {len(jobs)}")
    print(f"File contents: {json.dumps(jobs, indent=2)}")

asyncio.run(test())
