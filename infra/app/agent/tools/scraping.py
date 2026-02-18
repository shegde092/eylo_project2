
import logging
from app.agent.tools.base import BaseTool
from app.services.apify_client import apify_client
from app.services.youtube_client import youtube_client
from app.utils import get_platform
from app.schemas import ScrapedContent

logger = logging.getLogger(__name__)

class ScrapingTool(BaseTool):
    """Tool for scraping content from supported platforms (Instagram, TikTok, YouTube)"""
    
    def __init__(self):
        super().__init__(
            name="Scraper",
            description="Scrapes video/image content and metadata from a URL"
        )
    
    async def execute(self, url: str) -> ScrapedContent:
        platform = get_platform(url)
        logger.info(f"ScrapingTool: Detected platform {platform} for {url}")
        
        if platform == 'youtube':
            content = await youtube_client.scrape_url(url)
        elif platform in ['instagram', 'tiktok']:
            # Use Apify for these
            # We can bake in the retry logic here or in the agent
            content = await apify_client.scrape_url(url, platform)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
            
        if not content:
            raise Exception(f"Failed to scrape content from {platform}")
            
        return content
