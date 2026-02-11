"""Quick script to check the SQLite database contents"""
import sqlite3

# Connect to database
conn = sqlite3.connect('eylo_test.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

# Check import_jobs table
print("\nImport Jobs:")
cursor.execute("SELECT id, user_id, source_url, status, created_at FROM import_jobs;")
jobs = cursor.fetchall()
if jobs:
    for job in jobs:
        print(f"  Job ID: {job[0]}")
        print(f"    User: {job[1]}")
        print(f"    URL: {job[2]}")
        print(f"    Status: {job[3]}")
        print(f"    Created: {job[4]}")
else:
    print("  No jobs found")

# Check recipes table  
print("\nRecipes:")
cursor.execute("SELECT id, title, source_url, created_at, imported_at FROM recipes;")
recipes = cursor.fetchall()
if recipes:
    for recipe in recipes:
        print(f"  Recipe: {recipe[1]}")
        print(f"    ID: {recipe[0]}")
        print(f"    URL: {recipe[2]}")
        print(f"    Created: {recipe[3]}")
        print(f"    Imported: {recipe[4]}")
        print()
else:
    print("  No recipes found")

conn.close()
