import cv2
import base64
import json
import logging
import asyncio
from openai import AsyncOpenAI
from app.config import get_settings
from app.schemas import RecipeData, Ingredient

logger = logging.getLogger(__name__)
settings = get_settings()

SYSTEM_PROMPT = "You are a recipe extractor. Extract structured recipe data from the provided content. Output strictly valid JSON."

RECIPE_PROMPT = """
Creator: {author}
Caption: "{caption}"

Return this JSON:
{{
    "title": "Recipe Title",
    "prep_time_minutes": 10,
    "cook_time_minutes": 20,
    "ingredients": [{{"item": "name", "quantity": "1", "unit": "cup"}}],
    "steps": ["Step 1", "Step 2"],
    "tags": ["tag1"]
}}

Rules:
- Analyze the video frames carefully. Describe the visual steps performed by the chef.
- Even if text/captions are missing, infer the recipe process from the actions shown.
- Do your best to identify ingredients visually if they are not listed.
- Only return "NO_RECIPE_FOUND" if the video is completely unrelated to cooking/food.
"""


class OpenAIRecipeExtractor:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=120.0)
        self.model = "gpt-4o-mini"

    async def extract_from_video(self, video_path: str, caption: str, author: str = "") -> RecipeData:
        frames = await asyncio.get_event_loop().run_in_executor(None, self._extract_frames, video_path)
        if not frames:
            raise Exception("No frames extracted from video")
        images = [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{f}"}} for f in frames]
        return await self._ask(caption, author, images)

    async def extract_from_images(self, image_data: list[str], caption: str, author: str = "") -> RecipeData:
        images = [{"type": "image_url", "image_url": {"url": url}} for url in image_data[:5]]
        return await self._ask(caption, author, images)

    async def _ask(self, caption: str, author: str, images: list) -> RecipeData:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [{"type": "text", "text": RECIPE_PROMPT.format(caption=caption, author=author)}, *images]},
        ]
        
        # Debug logging
        logger.info(f"Sending request to OpenAI model={self.model}")
        
        # PRINT TO TERMINAL (User Request)
        print("\n=== OPENAI PROMPT ===")
        print(f"--- System Prompt ---\n{SYSTEM_PROMPT}\n")
        print(f"--- User Prompt ---\n{RECIPE_PROMPT.format(caption=caption, author=author)}")
        print(f"[Plus {len(images)} images]")
        print("=====================\n")
        
        resp = await self.client.chat.completions.create(model=self.model, messages=messages, response_format={"type": "json_object"}, max_tokens=2000)
        
        content = resp.choices[0].message.content
        
        # PRINT TO TERMINAL (User Request)
        print("\n=== OPENAI RESPONSE ===")
        print(content)
        print("=======================\n")
        
        return self._parse(content)

    def _extract_frames(self, video_path: str, max_frames: int = 20) -> list[str]:
        video = cv2.VideoCapture(video_path)
        total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = max(1, total // max_frames) if total > 0 else 30
        frames, count = [], 0
        while video.isOpened() and len(frames) < max_frames:
            ok, frame = video.read()
            if not ok:
                break
            if count % interval == 0:
                h, w = frame.shape[:2]
                if max(w, h) > 512:
                    scale = 512 / max(w, h)
                    frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                
                _, buf = cv2.imencode(".jpg", frame)
                frames.append(base64.b64encode(buf).decode())
            count += 1
        video.release()
        return frames

    def _parse(self, content: str) -> RecipeData:
        data = json.loads(content)
        return RecipeData(
            title=data.get("title", "Untitled Recipe"),
            prep_time_minutes=data.get("prep_time_minutes"),
            cook_time_minutes=data.get("cook_time_minutes"),
            ingredients=[Ingredient(**i) for i in data.get("ingredients", [])],
            steps=data.get("steps", []),
            tags=data.get("tags", []),
        )


openai_extractor = OpenAIRecipeExtractor()
