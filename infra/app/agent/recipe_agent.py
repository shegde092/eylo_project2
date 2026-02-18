import logging
import traceback
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database import SessionLocal, Recipe, ImportJob
from app.utils import get_post_type
from app.agent.tools.scraping import ScrapingTool
from app.agent.tools.extraction import ExtractionTool

logger = logging.getLogger(__name__)


class RecipeAgent:
    """Orchestrates: Scrape -> Extract -> Save"""

    def __init__(self):
        self.scraper = ScrapingTool()
        self.extractor = ExtractionTool()

    async def process_job(self, job_data: dict):
        job_id = job_data["job_id"]
        source_url = job_data["source_url"]
        user_id = job_data["user_id"]

        logger.info(f"Agent starting job {job_id} for {source_url}")

        db: Session = SessionLocal()
        job = None

        try:
            # Create/update job record
            job = db.query(ImportJob).filter(ImportJob.id == job_id).first()
            if not job:
                job = ImportJob(id=job_id, user_id=user_id, source_url=source_url, status="processing")
                db.add(job)
            else:
                job.status = "processing"
            db.commit()

            # Step 1: Scrape
            scraped = await self.scraper.execute(source_url)

            # Step 2: Extract
            recipe_data = await self.extractor.execute(scraped)

            # Step 3: Save recipe
            recipe = Recipe(
                user_id=user_id,
                title=recipe_data.title or "Untitled Recipe",
                source_url=source_url,
                source_type=get_post_type(source_url),
                data=recipe_data.model_dump()
            )
            db.add(recipe)
            db.commit()
            db.refresh(recipe)

            # Mark job complete
            job.status = "completed"
            job.recipe_id = recipe.id
            job.completed_at = datetime.now(timezone.utc)
            db.commit()

            logger.info(f"Job {job_id} completed: {recipe_data.title}")

        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}\n{traceback.format_exc()}")
            if job:
                job.status = "failed"
                job.error_message = str(e)
                job.completed_at = datetime.now(timezone.utc)
                db.commit()
        finally:
            db.close()
