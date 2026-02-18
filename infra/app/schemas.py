from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Union
from datetime import datetime
from uuid import UUID


class Ingredient(BaseModel):
    """Single ingredient with quantity and unit"""
    item: str = Field(..., description="Ingredient name")
    quantity: Union[str, int, float] = Field(..., description="Amount (can be numeric or text like '2-3')")
    unit: str = Field(..., description="Unit of measurement (g, cup, tsp, etc.)")


class RecipeData(BaseModel):
    """Structured recipe data extracted by AI"""
    title: str = Field(..., description="Recipe title")
    prep_time_minutes: Optional[int] = Field(None, description="Preparation time")
    cook_time_minutes: Optional[int] = Field(None, description="Cooking time")
    ingredients: List[Ingredient] = Field(..., description="List of ingredients")
    steps: List[str] = Field(..., description="Cooking instructions")
    tags: List[str] = Field(default_factory=list, description="Tags like cuisine, meal type")


class RecipeImportRequest(BaseModel):
    """Request to import a recipe from a URL"""
    url: HttpUrl = Field(..., description="Instagram URL (Reel, Post, or Picture)")



class RecipeImportResponse(BaseModel):
    """Response after enqueueing recipe import job"""
    job_id: UUID
    status: str = "processing"
    message: str = "Recipe import started. You'll receive a notification when it's ready."


class RecipeResponse(BaseModel):
    """Complete recipe response"""
    id: str
    user_id: str
    title: str
    source_url: str
    source_type: str
    data: RecipeData
    created_at: datetime
    imported_at: datetime
    
    class Config:
        from_attributes = True


class ScrapedContent(BaseModel):
    """Data returned from Apify scraper"""
    video_url: Optional[str] = Field(None, description="Direct link to video MP4")
    caption: str = Field("", description="Post caption/description")
    # removed thumbnail_url
    author: str = Field("", description="Instagram username")
    post_type: str = Field("reel", description="Type: reel, post, or carousel")
    image_urls: List[str] = Field(default_factory=list, description="For posts with images")
    duration: Optional[float] = Field(None, description="Video duration in seconds")
