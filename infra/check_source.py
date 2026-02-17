
import os
import requests
import sys

# Hardcoded check: try to fetch recipes from the API
# If the API returns the recipes we saw in SQLite earlier (IDs ending in ...7d4d, ...f191), 
# then it is still connected to SQLite.

try:
    print("Checking API source...")
    response = requests.get("http://localhost:8000/recipes", timeout=5)
    if response.status_code == 200:
        recipes = response.json()
        print(f"API returned {len(recipes)} recipes.")
        
        # Check for known SQLite IDs
        sqlite_ids = [
            "c824540d-e4b1-4610-a652-c8b14b177d4d",
            "0a12f7a9-4bd0-4794-8c30-4bce8916f191",
            "7a1bc7bd-4d04-4319-b5af-a1dd27bc7215"
        ]
        
        found_local = False
        for r in recipes:
            if r['id'] in sqlite_ids:
                found_local = True
                print(f"FOUND LOCAL RECIPE: {r['title']} (ID: {r['id']})")
        
        if found_local:
            print("\nCONCLUSION: The server is still using the LOCAL SQLite database.")
            print("Action: You must RESTART the server to use Supabase.")
        else:
            print("\nCONCLUSION: The server might be using Supabase (or it's just empty).")
            
    else:
        print(f"API Error: {response.status_code}")
except Exception as e:
    print(f"Error checking API: {e}")
