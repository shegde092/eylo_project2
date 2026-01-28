from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging

from app.config import get_settings
from app.database import get_db, init_db, Recipe
from app.schemas import RecipeImportRequest, RecipeImportResponse, RecipeResponse
from app.queue import enqueue_recipe_import
from app.utils import is_instagram_url

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Eylo Recipe Import API",
    description="Backend API for importing recipes from Instagram",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your mobile app domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Initializing database...")
    init_db()
    logger.info("✅ Database initialized")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "eylo-recipe-import-api"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected"
    }


@app.post("/import/recipe", response_model=RecipeImportResponse)
async def import_recipe(
    request: RecipeImportRequest,
    db: Session = Depends(get_db),
    # TODO: Add authentication with user_id = Depends(get_current_user)
):
    """
    Import a recipe from Instagram URL
    
    This endpoint:
    1. Validates the Instagram URL
    2. Enqueues a background job
    3. Returns immediately (Fire and Forget pattern)
    
    The actual scraping, AI extraction, and DB save happens asynchronously.
    User receives a push notification when complete.
    """
    
    # For now, using a mock user_id (replace with actual auth)
    user_id = "00000000-0000-0000-0000-000000000001"
    
    # Validate URL
    if not is_instagram_url(str(request.url)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Instagram URL. Only Instagram Reels, Posts, and TV videos are supported."
        )
    
    # Enqueue job
    try:
        job_id = await enqueue_recipe_import(
            user_id=user_id,
            source_url=str(request.url),
            fcm_token=request.fcm_token
        )
        
        logger.info(f"Enqueued recipe import job {job_id} for URL: {request.url}")
        
        return RecipeImportResponse(
            job_id=job_id,
            status="processing",
            message="Recipe import started. You'll receive a notification when it's ready."
        )
        
    except Exception as e:
        logger.error(f"Failed to enqueue job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start recipe import"
        )


@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: str, db: Session = Depends(get_db)):
    """
    Get a recipe by ID
    
    Used when user taps the push notification to view the imported recipe
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    return recipe


@app.get("/recipes", response_model=list[RecipeResponse])
async def list_recipes(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    List all recipes for a user
    
    TODO: Filter by authenticated user_id
    """
    recipes = db.query(Recipe).offset(skip).limit(limit).all()
    return recipes


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
