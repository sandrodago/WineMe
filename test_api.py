#!/usr/bin/env python3
"""
Test script to demonstrate the API functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_user():
    """Test creating a user"""
    print("Testing user creation...")
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print(f"User created: {response.json()}")
        return response.json()["id"]
    else:
        print(f"Error: {response.json()}")
        return None

def test_get_users():
    """Test getting all users"""
    print("Testing get users...")
    response = requests.get(f"{BASE_URL}/users/")
    print(f"Status: {response.status_code}")
    print(f"Users: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("Starting API tests...")
    print("=" * 50)
    
    # Wait a moment for the server to be ready
    time.sleep(2)
    
    # Test health check
    test_health_check()
    
    # Test user operations
    user_id = test_create_user()
    test_get_users()
    
    print("API tests completed!")
    print("=" * 50)
    print("You can also visit http://localhost:8000/docs for interactive API documentation")

if __name__ == "__main__":
    main() 