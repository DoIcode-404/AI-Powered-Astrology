"""
Quick test script for compatibility and horoscope endpoints
"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"

# Sample test data
SAMPLE_KUNDALI_A = {
    "user_id": "test_user_123",
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
        "Mercury": {"sign": "Aries", "degree": 8.2, "house": 9},
        "Jupiter": {"sign": "Cancer", "degree": 20.1, "house": 1},
        "Venus": {"sign": "Gemini", "degree": 14.5, "house": 11},
        "Saturn": {"sign": "Capricorn", "degree": 5.3, "house": 6}
    }
}

SAMPLE_KUNDALI_B = {
    "user_id": "test_user_456",
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
        "Mars": {"sign": "Aries", "degree": 22.4, "house": 8},
        "Mercury": {"sign": "Leo", "degree": 11.6, "house": 10},
        "Jupiter": {"sign": "Libra", "degree": 9.7, "house": 3},
        "Venus": {"sign": "Cancer", "degree": 28.3, "house": 9},
        "Saturn": {"sign": "Pisces", "degree": 12.5, "house": 7}
    }
}

def test_health_check():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Response received successfully")
            print("[OK] PASSED")
        else:
            print(f"[FAIL] FAILED: {response.text}")
    except Exception as e:
        print(f"[ERROR] {str(e)}")

def test_compatibility_quick():
    """Test quick compatibility endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Compatibility Quick Endpoint")
    print("="*60)
    try:
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }
        response = requests.post(f"{BASE_URL}/api/compatibility/quick", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                compatibility_data = data["data"]
                print(f"[OK] Compatibility Score: {compatibility_data['compatibility_percentage']}%")
                print(f"[OK] Rating: {compatibility_data['rating']}")
                print("[OK] PASSED")
            else:
                print(f"[FAIL] API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"[FAIL] FAILED: {response.text}")
    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")

def test_compatibility_detailed():
    """Test detailed compatibility endpoint"""
    print("\n" + "="*60)
    print("TEST 3: Compatibility Detailed Endpoint")
    print("="*60)
    try:
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }
        response = requests.post(f"{BASE_URL}/api/compatibility/detailed", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                analysis = data["data"]
                print(f"[OK] Compatibility Score: {analysis['compatibility_percentage']}%")
                print(f"[OK] Strengths Found: {len(analysis.get('strengths', []))}")
                print(f"[OK] Challenges Found: {len(analysis.get('challenges', []))}")
                print(f"[OK] Remedies Found: {len(analysis.get('remedies', []))}")
                if analysis.get('remedies'):
                    print(f"   Sample Remedy: {analysis['remedies'][0]['type']}")
                print("[OK] PASSED")
            else:
                print(f"[FAIL] API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"[FAIL] FAILED: {response.text}")
    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")

def test_compatibility_batch():
    """Test batch compatibility endpoint"""
    print("\n" + "="*60)
    print("TEST 4: Compatibility Batch Endpoint")
    print("="*60)
    try:
        payload = {
            "user_kundali": SAMPLE_KUNDALI_A,
            "candidates": [SAMPLE_KUNDALI_B, SAMPLE_KUNDALI_B],
            "relationship_type": "romantic"
        }
        response = requests.post(f"{BASE_URL}/api/compatibility/batch", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                results = data["data"]
                print(f"[OK] Comparisons Made: {len(results)}")
                if results:
                    print(f"[OK] First Result Score: {results[0]['compatibility_percentage']}%")
                print("[OK] PASSED")
            else:
                print(f"[FAIL] API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"[FAIL] FAILED: {response.text}")
    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")

def test_horoscope_daily():
    """Test daily horoscope endpoint"""
    print("\n" + "="*60)
    print("TEST 5: Horoscope Daily Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/api/predictions/horoscope/daily/aries")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                horoscope = data["data"]
                print(f"[OK] Zodiac Sign: {horoscope['zodiac_sign']}")
                print(f"[OK] Date: {horoscope['date']}")
                print(f"[OK] Overall Score: {horoscope['overall_score']}/100")
                print(f"[OK] Grade: {horoscope.get('grade', 'N/A')}")
                print(f"[OK] Life Areas: {len(horoscope.get('life_areas', []))}")
                if horoscope.get('affirmations'):
                    print(f"[OK] Affirmations: {len(horoscope['affirmations'])}")
                print("[OK] PASSED")
            else:
                print(f"[FAIL] API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"[FAIL] FAILED: {response.text}")
    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")

def test_horoscope_weekly():
    """Test weekly horoscope endpoint"""
    print("\n" + "="*60)
    print("TEST 6: Horoscope Weekly Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/api/predictions/horoscope/weekly/taurus")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                horoscope = data["data"]
                print(f"[OK] Zodiac Sign: {horoscope['zodiac_sign']}")
                print(f"[OK] Week Overview Length: {len(horoscope.get('week_overview', ''))}")
                if 'daily_breakdown' in horoscope:
                    print(f"[OK] Daily Breakdown: {len(horoscope['daily_breakdown'])} days")
                print(f"[OK] Weekly Grade: {horoscope.get('weekly_grade', 'N/A')}")
                print("[OK] PASSED")
            else:
                print(f"[FAIL] API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"[FAIL] FAILED: {response.text}")
    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")

def test_horoscope_monthly():
    """Test monthly horoscope endpoint"""
    print("\n" + "="*60)
    print("TEST 7: Horoscope Monthly Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/api/predictions/horoscope/monthly/gemini")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                horoscope = data["data"]
                print(f"[OK] Zodiac Sign: {horoscope['zodiac_sign']}")
                print(f"[OK] Month Overview Length: {len(horoscope.get('month_overview', ''))}")
                print(f"[OK] Monthly Grade: {horoscope.get('monthly_grade', 'N/A')}")
                print(f"[OK] Life Areas: {len(horoscope.get('life_areas', []))}")
                print("[OK] PASSED")
            else:
                print(f"[FAIL] API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"[FAIL] FAILED: {response.text}")
    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")

def test_horoscope_all_signs():
    """Test all signs daily horoscope endpoint"""
    print("\n" + "="*60)
    print("TEST 8: Horoscope All-Signs Daily Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/api/predictions/horoscope/all-signs/daily")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                horoscopes = data["data"]
                print(f"[OK] Total Horoscopes: {len(horoscopes)}")
                if horoscopes:
                    print(f"[OK] First Sign: {horoscopes[0]['zodiac_sign']}")
                    print(f"[OK] First Sign Score: {horoscopes[0]['overall_score']}")
                print("[OK] PASSED")
            else:
                print(f"[FAIL] API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"[FAIL] FAILED: {response.text}")
    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")

def test_horoscope_archive():
    """Test horoscope archive endpoint"""
    print("\n" + "="*60)
    print("TEST 9: Horoscope Archive Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/api/predictions/horoscope/archive/leo")
        print(f"Status Code: {response.status_code}")
        if response.status_code in [200, 404]:
            print(f"[OK] Endpoint accessible")
            print("[OK] PASSED")
        else:
            print(f"[FAIL] FAILED: {response.text}")
    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("TESTING COMPATIBILITY AND HOROSCOPE ENDPOINTS")
    print("="*60)

    test_health_check()
    test_compatibility_quick()
    test_compatibility_detailed()
    test_compatibility_batch()
    test_horoscope_daily()
    test_horoscope_weekly()
    test_horoscope_monthly()
    test_horoscope_all_signs()
    test_horoscope_archive()

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_all_tests()
