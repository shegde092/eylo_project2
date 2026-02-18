import logging
import yt_dlp
from app.schemas import ScrapedContent

logger = logging.getLogger(__name__)


class YouTubeClient:
    def __init__(self):
        self.ydl_opts = {"quiet": True, "no_warnings": True, "format": "best[ext=mp4]/best"}

    async def scrape_url(self, url: str) -> ScrapedContent:
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        if not info:
            raise Exception(f"yt-dlp returned no info for {url}")
        return ScrapedContent(
            video_url=info.get("url"),
            caption=f"{info.get('title', '')}\n{info.get('description', '')}",
            author=info.get("uploader", ""),
            post_type="youtube_video",
            image_urls=[],
        )


youtube_client = YouTubeClient()
