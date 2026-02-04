import logging
import yt_dlp
from typing import Optional
from app.services.apify_client import ScrapedContent

logger = logging.getLogger(__name__)

class YouTubeClient:
    """Client for downloading/scraping YouTube videos using yt-dlp"""
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best[ext=mp4]/best', # Prefer mp4, fallback to best
        }

    async def scrape_url(self, url: str) -> Optional[ScrapedContent]:
        """
        Get metadata and direct video URL from YouTube
        """
        try:
            logger.info(f"Extracting YouTube info for: {url}")
            
            # Run yt-dlp extraction (synchronous, but fast for just metadata)
            # In a heavy automated system, this should run in a thread pool
            info = self._get_info(url)
            
            if not info:
                return None
                
            return ScrapedContent(
                video_url=info.get("url"), # Direct video URL
                caption=info.get("title", "") + "\n" + info.get("description", ""),
                thumbnail_url=info.get("thumbnail"),
                author=info.get("uploader", ""),
                post_type="youtube_video",
                image_urls=[]
            )
            
        except Exception as e:
            logger.error(f"YouTube extraction failed using yt-dlp: {str(e)}")
            raise

    def _get_info(self, url: str) -> Optional[dict]:
        """Wrapper to run yt-dlp extraction"""
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            # extract_info=True downloads by default, so we set download=False
            return ydl.extract_info(url, download=False)


# Singleton instance
youtube_client = YouTubeClient()
