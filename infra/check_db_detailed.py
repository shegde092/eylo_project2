"""Check database with detailed output"""
import sys
sys.path.insert(0, 'C:\\Users\\shegd\\OneDrive\\Desktop\\eylo_project2\\infra')

from app.database import SessionLocal, ImportJob, Recipe
import json

db = SessionLocal()

print("=" * 60)
print("IMPORT JOBS")
print("=" * 60)

jobs = db.query(ImportJob).order_by(ImportJob.created_at.desc()).limit(5).all()
if jobs:
    for job in jobs:
        print(f"\nJob ID: {job.id}")
        print(f"User ID: {job.user_id}")
        print(f"Status: {job.status}")
        print(f"Source: {job.source_url}")
        print(f"Recipe ID: {job.recipe_id}")
        print(f"Created: {job.created_at}")
        print(f"Completed: {job.completed_at}")
        if job.error_message:
            print(f"Error: {job.error_message}")
else:
    print("No import jobs found")

print("\n" + "=" * 60)
print("RECIPES")
print("=" * 60)

recipes = db.query(Recipe).order_by(Recipe.created_at.desc()).limit(5).all()
if recipes:
    for recipe in recipes:
        print(f"\nRecipe ID: {recipe.id}")
        print(f"Title: {recipe.title}")
        print(f"Source: {recipe.source_url}")
        print(f"Created: {recipe.created_at}")
        if recipe.data:
            print(f"Data: {json.dumps(recipe.data, indent=2)}")
else:
    print("No recipes found")

db.close()
