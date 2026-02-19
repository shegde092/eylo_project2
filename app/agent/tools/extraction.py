import base64
import logging
import tempfile
import httpx
from pathlib import Path
from app.agent.tools.base import BaseTool
from app.services.openai_extractor import openai_extractor
from app.schemas import ScrapedContent, RecipeData

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


class ExtractionTool(BaseTool):
    def __init__(self):
        super().__init__(name="Extractor", description="Extracts recipe data using AI")

    async def execute(self, content: ScrapedContent) -> RecipeData:
        # 1. Try video first
        if content.video_url:
            try:
                video_path = await self._download(content.video_url, suffix=".mp4", timeout=300.0)
                try:
                    return await openai_extractor.extract_from_video(video_path, content.caption, content.author)
                finally:
                    Path(video_path).unlink(missing_ok=True)
            except Exception as e:
                logger.warning(f"Video failed, trying images: {e}")

        # 2. Fallback to images
        if content.image_urls:
            images_b64 = await self._download_images_as_b64(content.image_urls)
            if images_b64:
                return await openai_extractor.extract_from_images(images_b64, content.caption, content.author)

        raise Exception("No media available for extraction")

    async def _download(self, url: str, suffix: str, timeout: float) -> str:
        """Download a file to a temp path and return the path."""
        async with httpx.AsyncClient(headers=HEADERS, timeout=timeout) as client:
            async with client.stream("GET", url, follow_redirects=True) as resp:
                resp.raise_for_status()
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    async for chunk in resp.aiter_bytes():
                        tmp.write(chunk)
                    return tmp.name

    async def _download_images_as_b64(self, urls: list[str]) -> list[str]:
        """Download images and return as base64 data URLs."""
        result = []
        async with httpx.AsyncClient(headers=HEADERS, timeout=60.0) as client:
            for url in urls[:5]:
                try:
                    resp = await client.get(url, follow_redirects=True)
                    if resp.status_code == 200:
                        b64 = base64.b64encode(resp.content).decode()
                        result.append(f"data:image/jpeg;base64,{b64}")
                except Exception as e:
                    logger.warning(f"Image download failed: {e}")
        return result
