import httpx
import logging
from typing import Optional
from app.config import get_settings
from app.schemas import ScrapedContent

logger = logging.getLogger(__name__)
settings = get_settings()


class ApifyClient:
    """Client for Apify Scraper APIs (Instagram, YouTube, TikTok)"""
    
    def __init__(self):
        self.api_token = settings.apify_api_token
        self.base_url = "https://api.apify.com/v2"
        
        # Actor IDs
        self.actors = {
            "instagram": "shu8hvrXbJbY3Eb9W",                  # Instagram Scraper
            "youtube": "jefer/youtube-video-downloader",        # YouTube Downloader (Jefer)
            "tiktok": "OtzYfK1ndEGdwWFKQ"                     # Clockworks Free TikTok Scraper (Unique ID)
        }
    
    async def scrape_url(self, url: str, platform: str) -> Optional[ScrapedContent]:
        """
        Scrape content from any supported platform
        """
        if platform not in self.actors:
            raise ValueError(f"Unsupported platform: {platform}")
            
        actor_id = self.actors[platform]
        
        try:
            # Construct input based on platform
            run_input = self._get_actor_input(platform, url)
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Start the actor run
                run_response = await client.post(
                    f"{self.base_url}/acts/{actor_id}/runs",
                    params={"token": self.api_token},
                    json=run_input
                )
                run_response.raise_for_status()
                run_data = run_response.json()
                run_id = run_data["data"]["id"]
                
                logger.info(f"Started Apify run {run_id} for {platform}: {url}")
                
                # Wait for the run to finish
                dataset_id = await self._wait_for_run(client, run_id)
                
                # Get the scraped data
                items = await self._get_dataset_items(client, dataset_id)
                
                if not items:
                    logger.warning(f"No data scraped for {platform} URL: {url}")
                    return None
                
                # Parse the first item
                item = items[0]
                return self._parse_scraped_item(item, platform)
                
        except Exception as e:
            logger.error(f"Apify scraping failed for {url} ({platform}): {str(e)}")
            raise

    def _get_actor_input(self, platform: str, url: str) -> dict:
        """Get actor-specific input parameters"""
        if platform == "instagram":
            return {
                "directUrls": [url],
                "resultsType": "details",
                "resultsLimit": 1,
                "addParentData": False
            }
        elif platform == "youtube":
            return {
                "videos": [url],
                "preferredQuality": "1080p",
                "preferredFormat": "mp4"
            }
        elif platform == "tiktok":
            return {
                "postURLs": [url],
                "shouldDownloadCovers": False,
                "shouldDownloadSlideshowImages": False,
                "shouldDownloadSubtitles": False,
                "shouldDownloadVideos": True,
            }
        return {}

    async def _wait_for_run(self, client: httpx.AsyncClient, run_id: str, max_wait: int = 180) -> str:
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
    
    def _parse_scraped_item(self, item: dict, platform: str) -> ScrapedContent:
        """Parse Apify response based on platform"""
        
        # DEBUG: Log keys
        logger.info(f"Apify Item Keys ({platform}): {list(item.keys())}")
        
        if "error" in item:
            error_msg = item.get("errorDescription") or item.get("error")
            raise Exception(f"Apify Scraper Error: {error_msg}")

        if platform == "instagram":
            post_type = item.get("type", "reel")
            
            # Basic fields
            video_url = item.get("videoUrl") or item.get("video_url") or item.get("displayUrl")
            
            # Handle images (sometimes it's 'images' list, sometimes 'image' string)
            images = item.get("images", [])
            if not images and item.get("image"):
                images = [item.get("image")]
            
            # Fallback: if no images found (e.g. Reel), use displayUrl or thumbnailUrl as image
            if not images:
                fallback_image = item.get("displayUrl") or item.get("thumbnailUrl")
                if fallback_image:
                    images = [fallback_image]
                
            return ScrapedContent(
                video_url=video_url,
                caption=item.get("caption", ""),
                # removed thumbnail_url
                author=item.get("ownerUsername", "") or item.get("owner", {}).get("username", ""),
                post_type=post_type,
                image_urls=images
            )
            
        elif platform == "youtube":
            return ScrapedContent(
                video_url=item.get("downloadUrl") or item.get("url"), # Downloader usually returns downloadUrl
                caption=item.get("title", "") + "\n" + item.get("description", ""),
                # removed thumbnail_url
                author=item.get("channelName", "") or item.get("viewCount", ""), # Fallback for metadata
                post_type="youtube_video",
                image_urls=[]
            )
            
        elif platform == "tiktok":
            return ScrapedContent(
                video_url=item.get("videoMeta", {}).get("downloadAddr"), 
                caption=item.get("text", ""),
                # removed thumbnail_url
                author=item.get("authorMeta", {}).get("name", "") or item.get("authorMeta", {}).get("nickName", ""),
                post_type="tiktok_video",
                image_urls=[]
            )
            
        return ScrapedContent(
            video_url="", caption="", author="", post_type="unknown", image_urls=[]
        )


# Singleton instance
apify_client = ApifyClient()
