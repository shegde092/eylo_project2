
import logging
import asyncio
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database import SessionLocal, Recipe, ImportJob
from app.utils import get_post_type
from app.agent.tools.scraping import ScrapingTool
from app.agent.tools.extraction import ExtractionTool

logger = logging.getLogger(__name__)

class RecipeAgent:
    """
    Intelligent Agent for Recipe Import.
    Orchestrates tools (Scraper -> Extractor -> DB) to complete the job.
    """
    
    def __init__(self):
        self.scraper = ScrapingTool()
        self.extractor = ExtractionTool()
    
    async def process_job(self, job_data: dict):
        """Main entry point for processing a job"""
        job_id = job_data["job_id"]
        source_url = job_data["source_url"]
        user_id = job_data["user_id"]
        
        logger.info(f"Agent starting job {job_id} for {source_url}")
        
        db: Session = SessionLocal()
        import_job = None
        
        try:
            # 1. Update Job Status
            import_job = self._update_job_status(db, job_id, user_id, source_url, "processing")
            
            # 2. Tool: Scrape Content
            logger.info("Agent: invoking Scraper Tool...")
            scraped_content = await self.scraper.execute(source_url)
            
            # 3. Tool: Extract Recipe
            logger.info("Agent: invoking Extractor Tool...")
            recipe_data = await self.extractor.execute(scraped_content)
            
            # 4. Save to Database
            logger.info("Agent: Saving results...")
            recipe = Recipe(
                user_id=user_id,
                title=getattr(recipe_data, 'title', "Untitled Recipe"),
                source_url=source_url,
                source_type=get_post_type(source_url),
                data=recipe_data.model_dump()
            )
            db.add(recipe)
            db.commit()
            db.refresh(recipe)
            
            # 5. Complete Job
            import_job.status = "completed"
            import_job.recipe_id = recipe.id
            import_job.completed_at = datetime.now(timezone.utc)
            db.commit()
            
            logger.info(f"Agent successfully completed job {job_id}")
            
        except Exception as e:
            import traceback
            logger.error(f"Agent failed job {job_id}: {e}")
            logger.error(traceback.format_exc())
            if import_job:
                import_job.status = "failed"
                import_job.error_message = str(e)
                import_job.completed_at = datetime.now(timezone.utc)
                db.commit()
        finally:
            db.close()

    def _update_job_status(self, db, job_id, user_id, url, status):
        """Helper to create or update job record"""
        job = db.query(ImportJob).filter(ImportJob.id == job_id).first()
        if not job:
            job = ImportJob(id=job_id, user_id=user_id, source_url=url, status=status)
            db.add(job)
        else:
            job.status = status
            job.error_message = None
        db.commit()
        return job
