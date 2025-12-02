#!/usr/bin/env python3
"""
Simple endpoint diagnostic test for debugging
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api"
TEST_USER_EMAIL = f"testuser_{int(time.time())}@test.com"
TEST_USER_USERNAME = f"testuser_{int(time.time())}"
TEST_USER_PASSWORD = "TestPassword123!"

print("=" * 80)
print("ENDPOINT DIAGNOSTIC TEST")
print("=" * 80)

# Test 1: Register endpoint
print("\nTest 1: Register new user")
print(f"URL: {BASE_URL}/auth/register")
print(f"Data: {json.dumps({
    'email': TEST_USER_EMAIL,
    'username': TEST_USER_USERNAME,
    'password': TEST_USER_PASSWORD,
    'full_name': 'Test User'
}, indent=2)}")

try:
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": TEST_USER_EMAIL,
            "username": TEST_USER_USERNAME,
            "password": TEST_USER_PASSWORD,
            "full_name": "Test User"
        },
        timeout=10
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

# Test 2: ML health check (should work)
print("\n" + "=" * 80)
print("Test 2: ML Health Check (should pass)")
print(f"URL: {BASE_URL}/ml/health")

try:
    response = requests.get(
        f"{BASE_URL}/ml/health",
        timeout=10
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

# Test 3: Transit endpoint
print("\n" + "=" * 80)
print("Test 3: Transit Calculate")
print(f"URL: {BASE_URL}/transits/calculate")

birth_details = {
    "birth_date": "1990-01-15",
    "birth_time": "14:30",
    "birth_place": "Mumbai",
    "latitude": 19.0760,
    "longitude": 72.8777,
    "timezone_offset": 330
}

try:
    response = requests.post(
        f"{BASE_URL}/transits/calculate",
        json=birth_details,
        timeout=10
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        resp_json = response.json()
        print(json.dumps(resp_json, indent=2)[:500] + "...")
    except:
        print(response.text[:500] + "...")

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

print("\n" + "=" * 80)
