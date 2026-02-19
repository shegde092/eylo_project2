import asyncio
import httpx
import logging
from app.config import get_settings
from app.schemas import ScrapedContent

logger = logging.getLogger(__name__)
settings = get_settings()

BASE_URL = "https://api.apify.com/v2"
TOKEN = settings.apify_api_token

ACTORS = {
    "instagram": "shu8hvrXbJbY3Eb9W",
    "tiktok": "OtzYfK1ndEGdwWFKQ",
}

ACTOR_INPUTS = {
    "instagram": lambda url: {"directUrls": [url], "resultsType": "details", "resultsLimit": 1, "addParentData": False},
    "tiktok": lambda url: {"postURLs": [url], "shouldDownloadVideos": True, "shouldDownloadCovers": False, "shouldDownloadSubtitles": False, "shouldDownloadSlideshowImages": False},
}


class ApifyClient:
    async def scrape_url(self, url: str, platform: str) -> ScrapedContent:
        actor_id = ACTORS[platform]
        run_input = ACTOR_INPUTS[platform](url)

        async with httpx.AsyncClient(timeout=120.0) as client:
            # Start run
            resp = await client.post(f"{BASE_URL}/acts/{actor_id}/runs", params={"token": TOKEN}, json=run_input)
            resp.raise_for_status()
            run_id = resp.json()["data"]["id"]
            logger.info(f"Apify run {run_id} started for {platform}")

            # Poll until done
            dataset_id = await self._wait(client, run_id)

            # Fetch results
            items = (await client.get(f"{BASE_URL}/datasets/{dataset_id}/items", params={"token": TOKEN})).json()
            if not items:
                raise Exception(f"No data returned from Apify for {url}")

            return self._parse(items[0], platform)

    async def _wait(self, client: httpx.AsyncClient, run_id: str, max_wait: int = 180) -> str:
        for _ in range(max_wait // 5):
            data = (await client.get(f"{BASE_URL}/actor-runs/{run_id}", params={"token": TOKEN})).json()["data"]
            if data["status"] == "SUCCEEDED":
                return data["defaultDatasetId"]
            if data["status"] in ["FAILED", "ABORTED", "TIMED-OUT"]:
                raise Exception(f"Apify run failed: {data['status']}")
            await asyncio.sleep(5)
        raise TimeoutError(f"Apify run {run_id} timed out")

    def _parse(self, item: dict, platform: str) -> ScrapedContent:
        if "error" in item:
            error_msg = item.get("errorDescription") or item["error"]
            # "Restricted access" means partial data — log warning but continue with what we have
            if "restricted" in error_msg.lower() or "partial" in error_msg.lower():
                import logging
                logging.getLogger(__name__).warning(f"Apify partial data warning: {error_msg}")
            else:
                raise Exception(f"Apify error: {error_msg}")

        # Variable to hold content
        content = None

        if platform == "instagram":
            images = item.get("images") or ([item["image"]] if item.get("image") else [])
            if not images:
                images = [x for x in [item.get("displayUrl"), item.get("thumbnailUrl")] if x]
            caption = item.get("caption", "")
            author = item.get("ownerUsername") or item.get("owner", {}).get("username", "")
            import logging
            # downloadedVideo = pre-downloaded MP4 on Apify servers (no CDN blocks, no region restrictions)
            video_url = item.get("downloadedVideo") or item.get("videoUrl") or item.get("displayUrl")
            logging.getLogger(__name__).info(f"Instagram scraped — author: {author}, caption length: {len(caption)}, images: {len(images)}, has_downloaded_video: {bool(item.get('downloadedVideo'))}")
            
            content = ScrapedContent(
                video_url=video_url,
                caption=caption,
                author=author,
                post_type=item.get("type", "reel"),
                image_urls=images,
                duration=item.get("videoDuration"),
            )

        elif platform == "tiktok":
            content = ScrapedContent(
                video_url=item.get("videoMeta", {}).get("downloadAddr"),
                caption=item.get("text", ""),
                author=item.get("authorMeta", {}).get("name") or item.get("authorMeta", {}).get("nickName", ""),
                post_type="tiktok_video",
                image_urls=[],
                duration=item.get("videoMeta", {}).get("duration"),
            )
            
        else:
            raise ValueError(f"Unknown platform: {platform}")
            
        # PRINT TO TERMINAL (User Request)
        print(f"\n=== {platform.upper()} SCRAPED DATA ===")
        print(content.model_dump_json(indent=2))
        print("===============================\n")
        
        return content


apify_client = ApifyClient()
