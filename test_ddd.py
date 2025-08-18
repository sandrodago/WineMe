#!/usr/bin/env python3
"""
Test script to demonstrate the DDD architecture
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

def test_create_user_ddd():
    """Test creating a user using DDD architecture"""
    print("Testing DDD user creation...")
    user_data = {
        "email": "ddd@example.com",
        "username": "ddduser",
        "full_name": "DDD Test User"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print(f"User created: {response.json()}")
        return response.json()["id"]
    else:
        print(f"Error: {response.json()}")
        return None

def test_get_users_ddd():
    """Test getting all users using DDD architecture"""
    print("Testing DDD get users...")
    response = requests.get(f"{BASE_URL}/users/")
    print(f"Status: {response.status_code}")
    print(f"Users: {response.json()}")
    print()

def test_get_user_ddd(user_id):
    """Test getting a specific user using DDD architecture"""
    print(f"Testing DDD get user {user_id}...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"User: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    print()

def test_update_user_ddd(user_id):
    """Test updating a user using DDD architecture"""
    print(f"Testing DDD update user {user_id}...")
    update_data = {
        "full_name": "Updated DDD User",
        "is_active": True
    }
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"User updated: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    print()

def main():
    """Run all DDD tests"""
    print("Starting DDD Architecture Tests...")
    print("=" * 50)
    
    # Wait a moment for the server to be ready
    time.sleep(2)
    
    # Test health check
    test_health_check()
    
    # Test user operations with DDD
    user_id = test_create_user_ddd()
    test_get_users_ddd()
    
    if user_id:
        test_get_user_ddd(user_id)
        test_update_user_ddd(user_id)
    
    print("DDD Architecture tests completed!")
    print("=" * 50)
    print("You can also visit http://localhost:8000/docs for interactive API documentation")
    print("Architecture: Domain Driven Design (DDD)")

if __name__ == "__main__":
    main() 