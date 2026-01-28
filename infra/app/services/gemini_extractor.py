import google.generativeai as genai
import logging
import json
import httpx
from typing import Optional, List
from pathlib import Path
from app.config import get_settings
from app.schemas import RecipeData, ScrapedContent, Ingredient

logger = logging.getLogger(__name__)
settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)


class GeminiRecipeExtractor:
    """Extract structured recipe data using Gemini 1.5 Pro multimodal AI"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.schema = self._get_recipe_schema()
    
    def _get_recipe_schema(self) -> dict:
        """Define the expected JSON schema for recipe extraction"""
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Recipe name"},
                "prep_time_minutes": {"type": "integer", "description": "Preparation time in minutes"},
                "cook_time_minutes": {"type": "integer", "description": "Cooking time in minutes"},
                "ingredients": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "item": {"type": "string"},
                            "quantity": {"type": "string"},
                            "unit": {"type": "string"}
                        },
                        "required": ["item", "quantity", "unit"]
                    }
                },
                "steps": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["title", "ingredients", "steps"]
        }
    
    async def extract_from_video(
        self,
        video_path: str,
        caption: str,
        author: str = ""
    ) -> Optional[RecipeData]:
        """
        Extract recipe from video + caption using multimodal AI
        
        Args:
            video_path: Local path to downloaded video file
            caption: Instagram caption text
            author: Instagram username
            
        Returns:
            RecipeData with structured recipe information
        """
        try:
            # Upload video to Gemini
            video_file = genai.upload_file(video_path)
            logger.info(f"Uploaded video to Gemini: {video_file.name}")
            
            # Wait for processing
            import time
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise Exception("Video processing failed")
            
            # Create prompt
            prompt = self._create_prompt(caption, author)
            
            # Generate content with structured output
            response = self.model.generate_content(
                [video_file, prompt],
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=self.schema
                )
            )
            
            # Parse response
            recipe_json = json.loads(response.text)
            logger.info(f"Extracted recipe: {recipe_json.get('title', 'Unknown')}")
            
            # Convert to Pydantic model
            return RecipeData(
                prep_time_minutes=recipe_json.get("prep_time_minutes"),
                cook_time_minutes=recipe_json.get("cook_time_minutes"),
                ingredients=[
                    Ingredient(**ing) for ing in recipe_json["ingredients"]
                ],
                steps=recipe_json["steps"],
                tags=recipe_json.get("tags", [])
            )
            
        except Exception as e:
            logger.error(f"Gemini extraction failed: {str(e)}")
            raise
        finally:
            # Clean up video file from Gemini
            try:
                if 'video_file' in locals():
                    genai.delete_file(video_file.name)
            except:
                pass
    
    async def extract_from_images(
        self,
        image_urls: List[str],
        caption: str,
        author: str = ""
    ) -> Optional[RecipeData]:
        """
        Extract recipe from images + caption (for Instagram Posts)
        
        Args:
            image_urls: List of image URLs
            caption: Instagram caption text
            author: Instagram username
            
        Returns:
            RecipeData with structured recipe information
        """
        try:
            # Download images
            async with httpx.AsyncClient() as client:
                image_data = []
                for url in image_urls[:5]:  # Limit to first 5 images
                    response = await client.get(url)
                    response.raise_for_status()
                    image_data.append(response.content)
            
            # Create prompt
            prompt = self._create_prompt(caption, author)
            
            # Prepare content parts (images + prompt)
            content_parts = []
            for img_bytes in image_data:
                content_parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_bytes
                    }
                })
            content_parts.append(prompt)
            
            # Generate content
            response = self.model.generate_content(
                content_parts,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=self.schema
                )
            )
            
            # Parse response
            recipe_json = json.loads(response.text)
            logger.info(f"Extracted recipe from images: {recipe_json.get('title', 'Unknown')}")
            
            return RecipeData(
                prep_time_minutes=recipe_json.get("prep_time_minutes"),
                cook_time_minutes=recipe_json.get("cook_time_minutes"),
                ingredients=[
                    Ingredient(**ing) for ing in recipe_json["ingredients"]
                ],
                steps=recipe_json["steps"],
                tags=recipe_json.get("tags", [])
            )
            
        except Exception as e:
            logger.error(f"Gemini image extraction failed: {str(e)}")
            raise
    
    def _create_prompt(self, caption: str, author: str) -> str:
        """Create the prompt for Gemini"""
        return f"""You are a recipe extraction expert. Analyze this Instagram cooking content.

CAPTION: "{caption}"
AUTHOR: @{author}

Extract a complete recipe including:

1. **Title**: A concise, appealing recipe name
2. **Ingredients**: Watch the video/images carefully! Ingredients are often shown visually (e.g., "200g flour" written on a measuring cup or shown on screen). If quantities aren't visible, estimate reasonable amounts.
3. **Steps**: Clear, numbered cooking instructions. Watch the video/images for the cooking process.
4. **Timing**: Estimate prep and cook times based on the video/images
5. **Tags**: Classify the recipe (cuisine type, meal category, dietary info, cooking method)

CRITICAL RULES:
- Ingredients must include quantity and unit (e.g., "2 cups" not just "flour")
- If ingredients appear only in the video/images (not caption), you MUST extract them
- Steps should be clear and actionable
- If this is NOT a recipe (e.g., just a food photo), return a simple recipe based on the visible dish

Return ONLY valid JSON matching the required schema. Do not include any other text."""


# Singleton instance
gemini_extractor = GeminiRecipeExtractor()
