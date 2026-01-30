
import asyncio
import logging
import uuid
import sys
import os

# Ensure the current directory is in the path so we can import app modules
sys.path.append(os.getcwd())

from app.worker import RecipeProcessor
from app.database import SessionLocal, Recipe

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_openai_extraction():
    print("=" * 50)
    print("Testing OpenAI Recipe Extraction directly")
    print("=" * 50)

    # Use a real Instagram Reel that we know contains a recipe
    # Using the one from test_real_reel.py
    reel_url = "https://www.instagram.com/reel/DQ4DViXCe1B/?igsh=ZXBmYWJsdWV3cnF6"
    
    job_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4()) # Dummy user ID
    
    job_data = {
        "job_id": job_id,
        "user_id": user_id,
        "source_url": reel_url,
        "fcm_token": "test_token_openai_direct"
    }
    
    processor = RecipeProcessor()
    
    print(f"Creating job {job_id} for URL: {reel_url}")
    
    try:
        await processor.process_job(job_data)
        print("\n[OK] Job processing finished without exception.")
        
        # Verify data in DB
        db = SessionLocal()
        recipe = db.query(Recipe).filter(Recipe.source_url == reel_url).order_by(Recipe.created_at.desc()).first()
        
        if recipe:
            print(f"\n[OK] Recipe found in DB! ID: {recipe.id}")
            print(f"Title: {recipe.title}")
            print(f"Data: {recipe.data}")
            print(f"Thumbnail URL: {recipe.thumbnail_url}")
            print(f"Video URL: {recipe.video_url}")
        else:
            print("\n[FAIL] Recipe NOT found in DB despite success message.")
            
        db.close()
        
    except Exception as e:
        print(f"\n[FAIL] Test Failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_openai_extraction())
