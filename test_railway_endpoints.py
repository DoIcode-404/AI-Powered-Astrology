#!/usr/bin/env python3
"""
Test newly added Compatibility & Horoscope endpoints on Railway
"""

import requests
import json

# Railway URL
BASE_URL = "https://web-production-743d0.up.railway.app/api"

# Sample Kundali data for testing
SAMPLE_KUNDALI_A = {
    "user_id": "user_a_123",
    "name": "Person A",
    "dob": "1990-05-15",
    "tob": "10:30:00",
    "location": {"latitude": 28.7041, "longitude": 77.1025, "timezone": 5.5},
    "sun_sign": "Taurus",
    "moon_sign": "Libra",
    "ascendant": "Gemini",
    "planets": {
        "Sun": {"sign": "Taurus", "degree": 25.5, "house": 10},
        "Moon": {"sign": "Libra", "degree": 12.3, "house": 4},
        "Mars": {"sign": "Leo", "degree": 18.7, "house": 2},
    }
}

SAMPLE_KUNDALI_B = {
    "user_id": "user_b_456",
    "name": "Person B",
    "dob": "1992-08-22",
    "tob": "14:15:00",
    "location": {"latitude": 28.7041, "longitude": 77.1025, "timezone": 5.5},
    "sun_sign": "Virgo",
    "moon_sign": "Sagittarius",
    "ascendant": "Leo",
    "planets": {
        "Sun": {"sign": "Virgo", "degree": 29.2, "house": 11},
        "Moon": {"sign": "Sagittarius", "degree": 16.8, "house": 5},
    }
}

def test_endpoint(name, method, endpoint, data=None):
    """Test an endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    print(f"URL: {url}")

    try:
        if method == "GET":
            response = requests.get(url, timeout=15)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=15)

        print(f"Status Code: {response.status_code}")

        if response.status_code in [200, 201]:
            try:
                resp_json = response.json()
                print(f"[✓] SUCCESS")
                print(f"Response: {json.dumps(resp_json, indent=2)[:500]}...")
                return True
            except:
                print(f"[✓] SUCCESS (non-JSON response)")
                print(f"Response: {response.text[:200]}")
                return True
        else:
            print(f"[✗] FAILED")
            print(f"Response: {response.text[:300]}")
            return False

    except Exception as e:
        print(f"[✗] ERROR: {str(e)}")
        return False

def main():
    print("\n" + "="*70)
    print("TESTING RAILWAY DEPLOYMENT - COMPATIBILITY & HOROSCOPE ENDPOINTS")
    print("="*70)

    results = {
        "passed": 0,
        "failed": 0,
        "tests": []
    }

    # Test 1: Health Check
    if test_endpoint(
        "Health Check",
        "GET",
        "/health"
    ):
        results["passed"] += 1
        results["tests"].append(("Health Check", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Health Check", "FAIL"))

    # Test 2: Compatibility Quick
    if test_endpoint(
        "Compatibility Quick",
        "POST",
        "/compatibility/quick",
        {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }
    ):
        results["passed"] += 1
        results["tests"].append(("Compatibility Quick", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Compatibility Quick", "FAIL"))

    # Test 3: Compatibility Detailed
    if test_endpoint(
        "Compatibility Detailed",
        "POST",
        "/compatibility/detailed",
        {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }
    ):
        results["passed"] += 1
        results["tests"].append(("Compatibility Detailed", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Compatibility Detailed", "FAIL"))

    # Test 4: Compatibility Batch
    if test_endpoint(
        "Compatibility Batch",
        "POST",
        "/compatibility/batch",
        {
            "user_kundali": SAMPLE_KUNDALI_A,
            "candidates": [SAMPLE_KUNDALI_B],
            "relationship_type": "romantic"
        }
    ):
        results["passed"] += 1
        results["tests"].append(("Compatibility Batch", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Compatibility Batch", "FAIL"))

    # Test 5: Horoscope Daily
    if test_endpoint(
        "Horoscope Daily (Aries)",
        "GET",
        "/predictions/horoscope/daily/aries"
    ):
        results["passed"] += 1
        results["tests"].append(("Horoscope Daily", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Horoscope Daily", "FAIL"))

    # Test 6: Horoscope Weekly
    if test_endpoint(
        "Horoscope Weekly (Taurus)",
        "GET",
        "/predictions/horoscope/weekly/taurus"
    ):
        results["passed"] += 1
        results["tests"].append(("Horoscope Weekly", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Horoscope Weekly", "FAIL"))

    # Test 7: Horoscope Monthly
    if test_endpoint(
        "Horoscope Monthly (Gemini)",
        "GET",
        "/predictions/horoscope/monthly/gemini"
    ):
        results["passed"] += 1
        results["tests"].append(("Horoscope Monthly", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Horoscope Monthly", "FAIL"))

    # Test 8: Horoscope All-Signs
    if test_endpoint(
        "Horoscope All-Signs Daily",
        "GET",
        "/predictions/horoscope/all-signs/daily"
    ):
        results["passed"] += 1
        results["tests"].append(("Horoscope All-Signs", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Horoscope All-Signs", "FAIL"))

    # Test 9: Horoscope Archive
    if test_endpoint(
        "Horoscope Archive (Leo)",
        "GET",
        "/predictions/horoscope/archive/leo"
    ):
        results["passed"] += 1
        results["tests"].append(("Horoscope Archive", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Horoscope Archive", "FAIL"))

    # Print Summary
    print(f"\n\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")

    for test_name, status in results["tests"]:
        symbol = "✓" if status == "PASS" else "✗"
        print(f"  [{symbol}] {test_name}: {status}")

    print(f"\n{'='*70}")
    print(f"Total: {results['passed']} PASSED, {results['failed']} FAILED")
    print(f"Success Rate: {results['passed']/9*100:.1f}%")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
