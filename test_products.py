#!/usr/bin/env python3
"""
Test script to verify Products endpoints are working
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_create_product():
    """Test creating a product"""
    print("Testing product creation...")
    product_data = {
        "name": "Test Product",
        "description": "A great test product",
        "price": 29.99,
        "category": "Electronics",
        "stock_quantity": 100,
        "is_active": True
    }
    response = requests.post(f"{BASE_URL}/products/", json=product_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print(f"Product created: {response.json()}")
        return response.json()["id"]
    else:
        print(f"Error: {response.json()}")
        return None

def test_get_products():
    """Test getting all products"""
    print("Testing get products...")
    response = requests.get(f"{BASE_URL}/products/")
    print(f"Status: {response.status_code}")
    print(f"Products: {response.json()}")
    print()

def test_get_active_products():
    """Test getting active products"""
    print("Testing get active products...")
    response = requests.get(f"{BASE_URL}/products/active")
    print(f"Status: {response.status_code}")
    print(f"Active products: {response.json()}")
    print()

def test_get_product(product_id):
    """Test getting a specific product"""
    print(f"Testing get product {product_id}...")
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Product: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    print()

def test_update_product(product_id):
    """Test updating a product"""
    print(f"Testing update product {product_id}...")
    update_data = {
        "name": "Updated Test Product",
        "price": 39.99,
        "stock_quantity": 50
    }
    response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Product updated: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    print()

def main():
    """Run all product tests"""
    print("Starting Products API Tests...")
    print("=" * 50)
    
    # Wait a moment for the server to be ready
    time.sleep(2)
    
    # Test product operations
    product_id = test_create_product()
    test_get_products()
    test_get_active_products()
    
    if product_id:
        test_get_product(product_id)
        test_update_product(product_id)
    
    print("Products API tests completed!")
    print("=" * 50)
    print("You can also visit http://localhost:8000/docs for interactive API documentation")

if __name__ == "__main__":
    main() 