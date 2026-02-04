import os
import cv2
import base64
import json
import logging
import asyncio
from typing import Optional, List
from pathlib import Path
import httpx
from openai import AsyncOpenAI
from app.config import get_settings
from app.schemas import RecipeData, Ingredient

logger = logging.getLogger(__name__)
settings = get_settings()

class OpenAIRecipeExtractor:
    """Extract structured recipe data using OpenAI GPT-4o-mini"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4o-mini"
    
    def _encode_image(self, image_path):
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _extract_frames(self, video_path: str, max_frames: int = 20) -> List[str]:
        """Extract frames from video and return as base64 strings"""
        video = cv2.VideoCapture(video_path)
        base64_frames = []
        
        # Get total frame count to calculate interval
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            logger.warning("Could not determine frame count, using default interval")
            interval = 30 # Default to 1 frame per second assumption
        else:
            interval = max(1, total_frames // max_frames)
            
        count = 0
        frame_idx = 0
        
        while video.isOpened() and len(base64_frames) < max_frames:
            success, frame = video.read()
            if not success:
                break
                
            if count % interval == 0:
                # Resize frame to reduce token usage (max 512px)
                height, width = frame.shape[:2]
                if width > 512 or height > 512:
                    scaling_factor = 512 / max(width, height)
                    frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

                _, buffer = cv2.imencode(".jpg", frame)
                base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
                
            count += 1
            
        video.release()
        logger.info(f"Extracted {len(base64_frames)} frames from video")
        return base64_frames

    async def extract_from_video(
        self,
        video_path: str,
        caption: str,
        author: str = ""
    ) -> Optional[RecipeData]:
        """Extract recipe from video + caption using GPT-4o Vision"""
        try:
            # Extract frames
            # Run blocking OpenCV code in executor
            loop = asyncio.get_event_loop()
            base64_frames = await loop.run_in_executor(None, self._extract_frames, video_path)
            
            if not base64_frames:
                raise Exception("No frames extracted from video")
                
            # Construct message
            messages = [
                {
                    "role": "system",
                    "content": "You are a professional chef and recipe extractor. Extract structured recipe data from this Instagram video. Output strictly valid JSON."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self._create_prompt(caption, author)},
                        *map(lambda x: {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{x}"}}, base64_frames)
                    ]
                }
            ]
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={ "type": "json_object" },
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            logger.info(f"OpenAI raw response: {content[:100]}...")
            
            return self._parse_response(content)
            
        except Exception as e:
            logger.error(f"OpenAI video extraction failed: {str(e)}")
            raise

    async def extract_from_images(
        self,
        image_urls: List[str],
        caption: str,
        author: str = ""
    ) -> Optional[RecipeData]:
        """Extract recipe from images + caption"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a professional chef. Extract structured recipe data from these images. Output strictly valid JSON."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self._create_prompt(caption, author)},
                        *map(lambda x: {"type": "image_url", "image_url": {"url": x}}, image_urls[:5])
                    ]
                }
            ]
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={ "type": "json_object" },
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return self._parse_response(content)
            
        except Exception as e:
            logger.error(f"OpenAI image extraction failed: {str(e)}")
            raise

    def _create_prompt(self, caption: str, author: str) -> str:
        return f"""
        Analyze this social media content (Chef/Creator: {author}).
        Caption: "{caption}"
        
        Extract the following JSON structure:
        {{
            "title": "Recipe Title",
            "prep_time_minutes": 15,
            "cook_time_minutes": 30,
            "ingredients": [
                {{"item": "ingredient name", "quantity": "amount", "unit": "unit"}}
            ],
            "steps": ["Step 1", "Step 2"],
            "tags": ["tag1", "tag2"]
        }}
        
        Rules:
        1. If ingredients are missing quantities, estimate them from visual cues.
        2. Infer missing steps if the visual flow implies them.
        3. If it's not a recipe, return a best-guess recipe for the dish shown.
        """

    def _parse_response(self, content: str) -> RecipeData:
        try:
            data = json.loads(content)
            return RecipeData(
                title=data.get("title", "Untitled Recipe"),
                prep_time_minutes=data.get("prep_time_minutes"),
                cook_time_minutes=data.get("cook_time_minutes"),
                ingredients=[Ingredient(**i) for i in data.get("ingredients", [])],
                steps=data.get("steps", []),
                tags=data.get("tags", [])
            )
        except Exception as e:
            logger.error(f"Failed to parse OpenAI JSON: {e}")
            raise

openai_extractor = OpenAIRecipeExtractor()
