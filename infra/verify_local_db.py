from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Recipe, Base

# Connect to local SQLite DB
# We are in infra/, so DB is ./eylo.db
DATABASE_URL = "sqlite:///./eylo.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify():
    db = SessionLocal()
    try:
        recipes = db.query(Recipe).all()
        print(f"\n--- Checking Local Database (eylo.db) ---")
        print(f"Total Recipes Found: {len(recipes)}")
        
        for r in recipes:
            print(f"\n[Recipe] {r.title}")
            print(f" - ID: {r.id}")
            print(f" - Created: {r.created_at}")
            print(f" - Data Length: {len(str(r.data))} chars")
            
        if len(recipes) == 0:
             print("\n(Database is empty. Did you run the manual test?)")
             
    except Exception as e:
        print(f"Error reading DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify()
