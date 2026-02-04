import logging
import uuid
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base, Recipe, ImportJob
from app.schemas import RecipeImportRequest, RecipeImportResponse, RecipeResponse
from app.queue import enqueue_recipe_import
from app.config import get_settings

# Create database tables
Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(title="Eylo Recipe Import API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Eylo Recipe Import API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/import/recipe", response_model=RecipeImportResponse)
async def import_recipe(request: RecipeImportRequest, db: Session = Depends(get_db)):
    """
    Submit a URL for recipe extraction.
    Returns a job ID to track progress.
    """
    # Generate a dummy user ID for now (no auth yet)
    # In a real app, this would come from the JWT token
    user_id = str(uuid.uuid4())
    
    # 1. Enqueue the job
    job_id = await enqueue_recipe_import(
        user_id=user_id,
        source_url=str(request.url),
        fcm_token=request.fcm_token
    )
    
    # 2. Create initial job record
    # Although worker handles this, creating it here ensures immediate feedback if we query DB
    import_job = ImportJob(
        id=job_id,
        user_id=user_id,
        source_url=str(request.url),
        status="queued"
    )
    db.add(import_job)
    db.commit()
    
    return RecipeImportResponse(
        job_id=job_id,
        status="queued",
        message="Recipe import started"
    )

@app.get("/recipes", response_model=List[RecipeResponse])
def list_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all saved recipes"""
    recipes = db.query(Recipe).order_by(Recipe.created_at.desc()).offset(skip).limit(limit).all()
    return recipes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
