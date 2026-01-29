"""Simple test script for the Eylo API"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_root():
    """Test root endpoint"""
    print("Testing / endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_import_recipe():
    """Test recipe import endpoint"""
    print("Testing /import/recipe endpoint...")
    payload = {
        "url": "https://www.instagram.com/reel/test123/",
        "fcm_token": "test_device_token_12345"
    }
    response = requests.post(
        f"{BASE_URL}/import/recipe",
        json=payload
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    return response.json() if response.status_code == 200 else None

def test_list_recipes():
    """Test listing recipes"""
    print("Testing /recipes endpoint...")
    response = requests.get(f"{BASE_URL}/recipes")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("=== Eylo API Tests ===\n")
    
    # Run tests
    test_health()
    test_root()
    result = test_import_recipe()
    test_list_recipes()
    
    print("=== Tests Complete ===")
