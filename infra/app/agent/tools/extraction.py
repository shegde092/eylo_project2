
import logging
import tempfile
import httpx
from pathlib import Path
from app.agent.tools.base import BaseTool
from app.services.openai_extractor import openai_extractor
from app.schemas import ScrapedContent, RecipeData

logger = logging.getLogger(__name__)

class ExtractionTool(BaseTool):
    """Tool for extracting structured recipe data using AI"""
    
    def __init__(self):
        super().__init__(
            name="Extractor",
            description="Extracts recipe ingredients and steps from video/images"
        )
    
    async def execute(self, content: ScrapedContent) -> RecipeData:
        logger.info(f"ExtractionTool: Processing content from {content.author}")
        
        # Try Video First
        if content.video_url:
            try:
                logger.info(f"Attempting video extraction from {content.video_url[:30]}...")
                video_path = await self._download_video(content.video_url)
                try:
                    # If video works, return immediately
                    return await openai_extractor.extract_from_video(
                        video_path, content.caption, content.author
                    )
                finally:
                    Path(video_path).unlink(missing_ok=True)
            except Exception as e:
                logger.warning(f"⚠️ Video extraction failed: {e}")
                logger.info("Falling back to image extraction...")
        
        # Fallback to Images (or if no video existed)
        if content.image_urls:
            logger.info(f"Attempting extraction from {len(content.image_urls)} images...")
            
            # Download and encode images locally to avoid OpenAI download errors
            base64_images = await self._download_and_encode_images(content.image_urls)
            if not base64_images:
                raise Exception("Failed to download any images for extraction")

            return await openai_extractor.extract_from_images(
                base64_images, content.caption, content.author
            )
            
        raise Exception("No media found for extraction (Video failed and no images available)")

    async def _download_video(self, video_url: str) -> str:
        """Helper to download video temporarily"""
        # Increase timeout to 5 minutes (300s) for slow connections
        timeout = httpx.Timeout(300.0, connect=60.0)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        logger.info(f"Downloading video from: {video_url}")
        
        async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
            async with client.stream('GET', video_url, follow_redirects=True) as response:
                response.raise_for_status()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    for chunk in response.aiter_bytes():
                        tmp.write(chunk)
                    return tmp.name

    async def _download_and_encode_images(self, urls: list[str]) -> list[str]:
        """Download images and convert to base64 data URLs"""
        import base64
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        encoded_images = []
        # Increase timeout to 60s and add retries
        async with httpx.AsyncClient(headers=headers, timeout=60.0) as client:
            for url in urls[:5]: # Limit to 5 images
                for attempt in range(3): # Retry up to 3 times
                    try:
                        resp = await client.get(url, follow_redirects=True)
                        if resp.status_code == 200:
                            b64_data = base64.b64encode(resp.content).decode('utf-8')
                            encoded_images.append(f"data:image/jpeg;base64,{b64_data}")
                            break # Success, move to next image
                        else:
                            logger.warning(f"Image download failed (Attempt {attempt+1}): Status {resp.status_code}")
                    except Exception as e:
                        logger.warning(f"Image download error (Attempt {attempt+1}): {e}")
                        if attempt == 2: # Last attempt
                            logger.error(f"Failed to download image after 3 attempts: {url}")
                            
        return encoded_images
