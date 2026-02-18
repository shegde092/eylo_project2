import asyncio
import logging
from app.config import get_settings
from app.queue import dequeue_recipe_import
from app.agent.recipe_agent import RecipeAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

async def run():
    """Main worker loop using Agent architecture"""
    logger.info("🚀 Recipe Agent Worker started")
    
    # Initialize Agent
    agent = RecipeAgent()
    
    attempts = settings.retry_attempts
    delay = settings.retry_delay_seconds
    
    while True:
        try:
            # Get next job from queue (blocking)
            job_data = dequeue_recipe_import()
            
            if job_data:
                # Delegate processing to the Agent
                # Agent handles its own error update logic for the specific job
                await agent.process_job(job_data)
            else:
                # No job found, wait before checking again
                await asyncio.sleep(2)
            
        except KeyboardInterrupt:
            logger.info("Worker shutting down...")
            break
        except Exception as e:
            logger.error(f"Worker loop error: {str(e)}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run())