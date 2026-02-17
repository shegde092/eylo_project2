
import requests
import sys

def import_recipe():
    print("Please enter the recipe URL (Instagram, TikTok, or YouTube):")
    url = input("> ").strip()
    
    if not url:
        print("Error: No URL provided.")
        return

    try:
        response = requests.post(
            "http://localhost:8000/import/recipe",
            json={"url": url},
            timeout=10
        )
        
        if response.status_code == 200:
            print("\nSUCCESS! Recipe import started.")
            print(f"Response: {response.json()}")
        else:
            print(f"\nERROR: Request failed with status code {response.status_code}")
            print(f"Details: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the server. make sure 'python -m app.main' is running.")
    except Exception as e:
        print(f"\nERROR: An unexpected error occurred: {e}")

if __name__ == "__main__":
    import_recipe()
