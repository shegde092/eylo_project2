import asyncio
import logging
import tempfile
import httpx
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal, Recipe, ImportJob
from app.queue import dequeue_recipe_import
from app.services.apify_client import apify_client
from app.services.gemini_extractor import gemini_extractor
from app.services.s3_client import s3_client
from app.services.fcm_client import fcm_client
from app.utils import get_instagram_post_type

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


class RecipeProcessor:
    """Background worker that processes recipe import jobs"""
    
    def __init__(self):
        self.retry_attempts = settings.retry_attempts
        self.retry_delay = settings.retry_delay_seconds
    
    async def process_job(self, job_data: dict):
        """
        Process a single recipe import job
        
        Flow:
        1. Scrape Instagram content (Apify)
        2. Extract recipe data (Gemini AI)
        3. Upload media to S3
        4. Save recipe to database
        5. Send push notification
        """
        job_id = job_data["job_id"]
        user_id = job_data["user_id"]
        source_url = job_data["source_url"]
        fcm_token = job_data.get("fcm_token")
        
        logger.info(f"Processing job {job_id} for user {user_id}: {source_url}")
        
        db = SessionLocal()
        import_job = None
        
        try:
            # Create import job record
            import_job = ImportJob(
                id=job_id,
                user_id=user_id,
                source_url=source_url,
                status="processing"
            )
            db.add(import_job)
            db.commit()
            
            # Step 1: Scrape Instagram content
            logger.info(f"[{job_id}] Scraping Instagram...")
            scraped_content = await self._scrape_with_retry(source_url)
            
            if not scraped_content:
                raise Exception("Failed to scrape Instagram content")
            
            # Step 2: Extract recipe using AI
            logger.info(f"[{job_id}] Extracting recipe with Gemini AI...")
            post_type = get_instagram_post_type(source_url)
            
            if scraped_content.video_url:
                # Download video temporarily
                video_path = await self._download_video(scraped_content.video_url)
                recipe_data = await gemini_extractor.extract_from_video(
                    video_path,
                    scraped_content.caption,
                    scraped_content.author
                )
                # Clean up
                Path(video_path).unlink()
            elif scraped_content.image_urls:
                # Extract from images
                recipe_data = await gemini_extractor.extract_from_images(
                    scraped_content.image_urls,
                    scraped_content.caption,
                    scraped_content.author
                )
            else:
                raise Exception("No video or images found in scraped content")
            
            # Step 3: Upload media to S3 (optional - gracefully handle failures)
            logger.info(f"[{job_id}] Uploading media to S3...")
            thumbnail_url = None
            video_url = None
            
            try:
                if scraped_content.thumbnail_url:
                    thumbnail_url = await s3_client.upload_from_url(
                        scraped_content.thumbnail_url,
                        f"recipes/{user_id}/{job_id}/thumbnail.jpg",
                        "image/jpeg"
                    )
                    logger.info(f"[{job_id}] Thumbnail uploaded to S3")
            except Exception as e:
                logger.warning(f"[{job_id}] Failed to upload thumbnail: {str(e)} (continuing anyway)")
            
            try:
                if scraped_content.video_url:
                    video_url = await s3_client.upload_from_url(
                        scraped_content.video_url,
                        f"recipes/{user_id}/{job_id}/video.mp4",
                        "video/mp4"
                    )
                    logger.info(f"[{job_id}] Video uploaded to S3")
            except Exception as e:
                logger.warning(f"[{job_id}] Failed to upload video: {str(e)} (continuing anyway)")

            
            # Step 4: Save recipe to database
            logger.info(f"[{job_id}] Saving recipe to database...")
            recipe = Recipe(
                user_id=user_id,
                title=recipe_data.title if hasattr(recipe_data, 'title') else "Untitled Recipe",
                source_url=source_url,
                source_type=post_type,
                data=recipe_data.dict(),
                thumbnail_url=thumbnail_url,
                video_url=video_url
            )
            db.add(recipe)
            db.commit()
            db.refresh(recipe)
            
            # Update import job
            import_job.status = "completed"
            import_job.recipe_id = recipe.id
            import_job.completed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"[{job_id}] ✅ Recipe saved: {recipe.title} (ID: {recipe.id})")
            
            # Step 5: Send push notification
            if fcm_token:
                logger.info(f"[{job_id}] Sending push notification...")
                await fcm_client.send_recipe_ready_notification(
                    fcm_token,
                    str(recipe.id),
                    recipe.title
                )
            
            logger.info(f"[{job_id}] ✅ Job completed successfully!")
            
        except Exception as e:
            logger.error(f"[{job_id}] ❌ Job failed: {str(e)}")
            
            if import_job:
                import_job.status = "failed"
                import_job.error_message = str(e)
                import_job.completed_at = datetime.utcnow()
                db.commit()
        
        finally:
            db.close()
    
    async def _scrape_with_retry(self, url: str):
        """Scrape with retry logic"""
        for attempt in range(self.retry_attempts):
            try:
                return await apify_client.scrape_instagram_url(url)
            except Exception as e:
                if attempt < self.retry_attempts - 1:
                    logger.warning(f"Scraping attempt {attempt + 1} failed, retrying...")
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise e
    
    async def _download_video(self, video_url: str) -> str:
        """Download video to temporary file"""
        async with httpx.AsyncClient() as client:
            response = await client.get(video_url, follow_redirects=True)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(response.content)
                return tmp.name
    
    async def run(self):
        """Main worker loop"""
        logger.info("🚀 Recipe worker started")
        
        # Initialize FCM
        fcm_client.initialize()
        
        while True:
            try:
                # Get next job from queue (blocking)
                job_data = dequeue_recipe_import()
                
                if job_data:
                    # Process asynchronously
                    await self.process_job(job_data)
                
            except KeyboardInterrupt:
                logger.info("Worker shutting down...")
                break
            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
                await asyncio.sleep(5)


if __name__ == "__main__":
    processor = RecipeProcessor()
    asyncio.run(processor.run())
