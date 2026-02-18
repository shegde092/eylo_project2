import asyncio
import logging
import tempfile
import httpx
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal, Recipe, ImportJob
from app.queue import dequeue_recipe_import
from app.services.apify_client import apify_client
from app.services.youtube_client import youtube_client
from app.services.openai_extractor import openai_extractor
from app.services.fcm_client import fcm_client
from app.utils import get_post_type, get_platform

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
settings = get_settings()


async def download_video(video_url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(video_url, follow_redirects=True)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(response.content)
            return tmp.name


async def scrape_with_retry(url: str, platform: str, attempts: int, delay: int):
    for i in range(attempts):
        try:
            return await apify_client.scrape_url(url, platform)
        except Exception as e:
            if i < attempts - 1:
                logger.warning(f"Scraping attempt {i + 1} failed, retrying...")
                await asyncio.sleep(delay * (i + 1))
            else:
                raise


async def scrape(source_url: str, platform: str, attempts: int, delay: int):
    if platform == 'youtube':
        return await youtube_client.scrape_url(source_url)
    return await scrape_with_retry(source_url, platform, attempts, delay)


async def extract_recipe(scraped, post_type):
    if scraped.video_url:
        video_path = await download_video(scraped.video_url)
        recipe = await openai_extractor.extract_from_video(video_path, scraped.caption, scraped.author)
        Path(video_path).unlink()
        return recipe
    if scraped.image_urls:
        return await openai_extractor.extract_from_images(scraped.image_urls, scraped.caption, scraped.author)
    raise Exception("No video or images found in scraped content")


async def process_job(job_data: dict, retry_attempts: int, retry_delay: int):
    job_id = job_data["job_id"]
    user_id = job_data["user_id"]
    source_url = job_data["source_url"]

    db = SessionLocal()
    import_job = None

    try:
        import_job = db.query(ImportJob).filter(ImportJob.id == job_id).first()
        if not import_job:
            import_job = ImportJob(id=job_id, user_id=user_id, source_url=source_url, status="processing")
            db.add(import_job)
        else:
            logger.info(f"[{job_id}] Job already exists, resuming...")
            import_job.status = "processing"
            import_job.error_message = None
        db.commit()

        platform = get_platform(source_url)
        if platform == 'unknown':
            raise Exception(f"Unsupported platform for URL: {source_url}")

        scraped = await scrape(source_url, platform, retry_attempts, retry_delay)
        if not scraped:
            raise Exception(f"Failed to scrape content from {platform}")

        recipe_data = await extract_recipe(scraped, get_post_type(source_url))

        recipe = Recipe(
            user_id="dummy_user",
            title=getattr(recipe_data, 'title', "Untitled Recipe"),
            source_url=source_url,
            source_type=get_post_type(source_url),
            data=recipe_data.model_dump()
        )
        db.add(recipe)
        db.commit()
        db.refresh(recipe)

        import_job.status = "completed"
        import_job.recipe_id = recipe.id
        import_job.completed_at = datetime.now(timezone.utc)
        db.commit()

        logger.info(f"[{job_id}] Completed: {recipe.title}")

    except Exception as e:
        db.rollback()
        logger.error(f"[{job_id}] ❌ Job failed: {e}")
        if import_job:
            import_job.status = "failed"
            import_job.error_message = str(e)
            import_job.completed_at = datetime.now(timezone.utc)
            db.commit()
    finally:
        db.close()


async def run():
    logger.info("🚀 Recipe worker started")
    fcm_client.initialize()

    attempts = settings.retry_attempts
    delay = settings.retry_delay_seconds

    while True:
        try:
            job_data = dequeue_recipe_import()
            if job_data:
                await process_job(job_data, attempts, delay)
            else:
                await asyncio.sleep(2)
        except KeyboardInterrupt:
            logger.info("Worker shutting down...")
            break
        except Exception as e:
            logger.error(f"Worker error: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(run())