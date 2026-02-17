
import sqlite3
import pandas as pd

try:
    conn = sqlite3.connect('eylo.db')
    
    print("--- IMPORT JOBS ---")
    jobs = pd.read_sql_query("SELECT * FROM import_jobs", conn)
    if jobs.empty:
        print("No import jobs found.")
    else:
        print(jobs)
        
    print("\n--- RECIPES ---")
    recipes = pd.read_sql_query("SELECT * FROM recipes", conn)
    if recipes.empty:
        print("No recipes found.")
    else:
        print(recipes)
        
    conn.close()
except Exception as e:
    print(f"Error checking database: {e}")
