import logging
from app.agent.tools.base import BaseTool
from app.services.apify_client import apify_client
from app.services.youtube_client import youtube_client
from app.utils import get_platform
from app.schemas import ScrapedContent

logger = logging.getLogger(__name__)


class ScrapingTool(BaseTool):
    def __init__(self):
        super().__init__(name="Scraper", description="Scrapes content from Instagram, TikTok, or YouTube")

    async def execute(self, url: str) -> ScrapedContent:
        platform = get_platform(url)
        logger.info(f"Scraping {platform}: {url}")

        if platform == "youtube":
            content = await youtube_client.scrape_url(url)
        elif platform in ["instagram", "tiktok"]:
            content = await apify_client.scrape_url(url, platform)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        if not content:
            raise Exception(f"No content scraped from {platform}")

        return content
