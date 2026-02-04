"""Interactive test script for importing Instagram recipes"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def get_url_from_user():
    print("=" * 50)
    print("Manual Recipe Import Test")
    print("=" * 50)
    print("\nPaste the Instagram Reel/Post URL below:")
    
    # Support for both Python 2 and 3
    if sys.version_info[0] < 3:
        url = raw_input("> ").strip()
    else:
        url = input("> ").strip()
        
    return url

def import_recipe(url):
    if not url:
        print("❌ No URL provided. Exiting.")
        return

    print(f"\nSending import request for: {url}...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/import/recipe",
            json={
                "url": url,
                "fcm_token": "manual_test_device_token"
            },
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if response.status_code == 200:
                job_id = data.get("job_id")
                print(f"\n✅ Job created successfully!")
                print(f"Job ID: {job_id}")
                print("\nCheck the 'Worker' terminal to see it processing...")
            else:
                print(f"\n❌ API returned error")
                
        except json.JSONDecodeError:
            print(f"Response (Raw): {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to the API.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python -m app.main")

if __name__ == "__main__":
    url = get_url_from_user()
    import_recipe(url)
