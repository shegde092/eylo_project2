from app.database import SessionLocal, Recipe
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def clean_failed_recipes():
    print("Connecting to database...")
    db = SessionLocal()
    try:
        # Delete recipes with title "NO_RECIPE_FOUND"
        query = db.query(Recipe).filter(Recipe.title == "NO_RECIPE_FOUND")
        count = query.count()
        
        if count > 0:
            query.delete()
            db.commit()
            print(f"SUCCESS: Deleted {count} failed recipes.")
        else:
            print("No failed recipes found.")
        
        # List remaining recipes
        recipes = db.query(Recipe).all()
        print(f"\nRemaining Recipes ({len(recipes)}):")
        for r in recipes:
            print(f"- [{r.id}] {r.title} ({r.source_url})")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clean_failed_recipes()
