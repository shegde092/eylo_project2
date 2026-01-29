"""Test importing a real Instagram reel"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Real Instagram reel URL
reel_url = "https://www.instagram.com/reel/DQ4DViXCe1B/?igsh=ZXBmYWJsdWV3cnF6"

print("=" * 50)
print("Testing Real Instagram Reel Import")
print("=" * 50)
print(f"\nReel URL: {reel_url}\n")

# Import the recipe
print("Sending import request...")
response = requests.post(
    f"{BASE_URL}/import/recipe",
    json={
        "url": reel_url,
        "fcm_token": "test_device_token_real_reel"
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    job_id = response.json()["job_id"]
    print(f"\n✅ Job created successfully!")
    print(f"Job ID: {job_id}")
    print("\nTo process this job, start the worker:")
    print("  python -m app.worker")
else:
    print(f"\n❌ Failed to create job")
