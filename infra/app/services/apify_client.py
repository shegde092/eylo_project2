import httpx
import logging
from typing import Optional
from app.config import get_settings
from app.schemas import ScrapedContent

logger = logging.getLogger(__name__)
settings = get_settings()


class ApifyClient:
    """Client for Apify Instagram Scraper API"""
    
    def __init__(self):
        self.api_token = settings.apify_api_token
        self.base_url = "https://api.apify.com/v2"
        # Using the official Instagram Scraper actor
        self.actor_id = "shu8hvrXbJbY3Eb9W"
    
    async def scrape_instagram_url(self, url: str) -> Optional[ScrapedContent]:
        """
        Scrape Instagram content using Apify
        
        Args:
            url: Instagram URL (Reel, Post, or TV)
            
        Returns:
            ScrapedContent with video, caption, and metadata
        """
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Start the actor run
                run_response = await client.post(
                    f"{self.base_url}/acts/{self.actor_id}/runs",
                    params={"token": self.api_token},
                    json={
                        "directUrls": [url],
                        "resultsType": "posts",
                        "resultsLimit": 1,
                        "addParentData": False
                    }
                )
                run_response.raise_for_status()
                run_data = run_response.json()
                run_id = run_data["data"]["id"]
                
                logger.info(f"Started Apify run {run_id} for URL: {url}")
                
                # Wait for the run to finish (polling)
                dataset_id = await self._wait_for_run(client, run_id)
                
                # Get the scraped data
                items = await self._get_dataset_items(client, dataset_id)
                
                if not items:
                    logger.warning(f"No data scraped for URL: {url}")
                    return None
                
                # Parse the first item
                item = items[0]
                return self._parse_scraped_item(item)
                
        except Exception as e:
            logger.error(f"Apify scraping failed for {url}: {str(e)}")
            raise
    
    async def _wait_for_run(self, client: httpx.AsyncClient, run_id: str, max_wait: int = 120) -> str:
        """Poll the run status until it's finished"""
        import asyncio
        
        waited = 0
        while waited < max_wait:
            response = await client.get(
                f"{self.base_url}/actor-runs/{run_id}",
                params={"token": self.api_token}
            )
            response.raise_for_status()
            data = response.json()["data"]
            
            status = data["status"]
            if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
                if status == "SUCCEEDED":
                    return data["defaultDatasetId"]
                else:
                    raise Exception(f"Apify run failed with status: {status}")
            
            await asyncio.sleep(5)
            waited += 5
        
        raise TimeoutError(f"Apify run {run_id} timed out after {max_wait}s")
    
    async def _get_dataset_items(self, client: httpx.AsyncClient, dataset_id: str) -> list:
        """Get items from the dataset"""
        response = await client.get(
            f"{self.base_url}/datasets/{dataset_id}/items",
            params={"token": self.api_token}
        )
        response.raise_for_status()
        return response.json()
    
    def _parse_scraped_item(self, item: dict) -> ScrapedContent:
        """Parse Apify response into ScrapedContent schema"""
        # Apify Instagram Scraper returns different structures for different post types
        post_type = item.get("type", "reel")
        
        return ScrapedContent(
            video_url=item.get("videoUrl"),
            caption=item.get("caption", ""),
            thumbnail_url=item.get("displayUrl") or item.get("thumbnailUrl"),
            author=item.get("ownerUsername", ""),
            post_type=post_type,
            image_urls=item.get("images", []) if post_type == "post" else []
        )


# Singleton instance
apify_client = ApifyClient()
