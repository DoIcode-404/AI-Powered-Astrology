"""
Integration Tests for Compatibility Analysis Feature
Tests all compatibility endpoints and business logic.
"""

import pytest
import json
from datetime import datetime
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

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
        "Mercury": {"sign": "Aries", "degree": 8.2, "house": 9},
        "Jupiter": {"sign": "Cancer", "degree": 20.1, "house": 1},
        "Venus": {"sign": "Gemini", "degree": 14.5, "house": 11},
        "Saturn": {"sign": "Capricorn", "degree": 5.3, "house": 6}
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
        "Mars": {"sign": "Aries", "degree": 22.4, "house": 8},
        "Mercury": {"sign": "Leo", "degree": 11.6, "house": 10},
        "Jupiter": {"sign": "Libra", "degree": 9.7, "house": 3},
        "Venus": {"sign": "Cancer", "degree": 28.3, "house": 9},
        "Saturn": {"sign": "Pisces", "degree": 12.5, "house": 7}
    }
}


class TestCompatibilityQuickEndpoint:
    """Test the quick compatibility check endpoint"""

    def test_quick_compatibility_valid_request(self):
        """Test quick compatibility with valid kundali data"""
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/quick", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "compatibility_percentage" in data["data"]
        assert "rating" in data["data"]
        assert 0 <= data["data"]["compatibility_percentage"] <= 100

    def test_quick_compatibility_missing_kundali_a(self):
        """Test quick compatibility with missing kundali_a"""
        payload = {
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/quick", json=payload)

        assert response.status_code == 422  # Validation error

    def test_quick_compatibility_invalid_relationship_type(self):
        """Test quick compatibility with invalid relationship type"""
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "invalid_type"
        }

        response = client.post("/api/compatibility/quick", json=payload)

        # Should either reject or use default
        assert response.status_code in [200, 422]

    def test_quick_compatibility_different_relationship_types(self):
        """Test quick compatibility with different relationship types"""
        relationship_types = ["romantic", "business", "friendship", "family"]

        for rel_type in relationship_types:
            payload = {
                "kundali_a": SAMPLE_KUNDALI_A,
                "kundali_b": SAMPLE_KUNDALI_B,
                "relationship_type": rel_type
            }

            response = client.post("/api/compatibility/quick", json=payload)

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "data" in data


class TestCompatibilityDetailedEndpoint:
    """Test the detailed compatibility analysis endpoint"""

    def test_detailed_compatibility_valid_request(self):
        """Test detailed compatibility with valid kundali data"""
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/detailed", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data

        # Check for comprehensive analysis fields
        analysis = data["data"]
        assert "compatibility_percentage" in analysis
        assert "compatibility_rating" in analysis
        assert "strengths" in analysis
        assert "challenges" in analysis
        assert "remedies" in analysis
        assert "relationship_timeline" in analysis
        assert "life_area_predictions" in analysis

    def test_detailed_compatibility_strengths_structure(self):
        """Test that strengths have proper structure"""
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/detailed", json=payload)

        assert response.status_code == 200
        data = response.json()
        strengths = data["data"]["strengths"]

        # Strengths should be a list
        assert isinstance(strengths, list)

        # Each strength should have required fields
        for strength in strengths:
            assert "factor_name" in strength
            assert "description" in strength
            assert "impact_score" in strength or "area_of_life" in strength

    def test_detailed_compatibility_challenges_structure(self):
        """Test that challenges have proper structure"""
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/detailed", json=payload)

        assert response.status_code == 200
        data = response.json()
        challenges = data["data"]["challenges"]

        # Challenges should be a list
        assert isinstance(challenges, list)

        # Each challenge should have mitigation strategies
        for challenge in challenges:
            if len(challenges) > 0:
                assert "factor_name" in challenge
                if "mitigation_strategies" in challenge:
                    assert isinstance(challenge["mitigation_strategies"], list)

    def test_detailed_compatibility_remedies_structure(self):
        """Test that remedies have proper structure"""
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/detailed", json=payload)

        assert response.status_code == 200
        data = response.json()
        remedies = data["data"]["remedies"]

        # Remedies should be a list
        assert isinstance(remedies, list)

        # Each remedy should have type
        for remedy in remedies:
            assert "type" in remedy
            assert remedy["type"] in ["Gemstone", "Mantra", "Ritual", "Lifestyle"]


class TestCompatibilityBatchEndpoint:
    """Test the batch compatibility comparison endpoint"""

    def test_batch_compatibility_valid_request(self):
        """Test batch compatibility with valid data"""
        payload = {
            "user_kundali": SAMPLE_KUNDALI_A,
            "candidates": [SAMPLE_KUNDALI_B],
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/batch", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_batch_compatibility_multiple_candidates(self):
        """Test batch compatibility with multiple candidates"""
        candidates = [SAMPLE_KUNDALI_B] * 3  # Use same person 3 times for testing

        payload = {
            "user_kundali": SAMPLE_KUNDALI_A,
            "candidates": candidates,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/batch", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 3

    def test_batch_compatibility_empty_candidates(self):
        """Test batch compatibility with empty candidates list"""
        payload = {
            "user_kundali": SAMPLE_KUNDALI_A,
            "candidates": [],
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/batch", json=payload)

        # Should either return empty list or validation error
        assert response.status_code in [200, 422]


class TestCompatibilityIntegration:
    """Integration tests for overall compatibility flow"""

    def test_quick_vs_detailed_consistency(self):
        """Test that quick and detailed endpoints return consistent scores"""
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        # Get quick result
        quick_response = client.post("/api/compatibility/quick", json=payload)
        quick_percentage = quick_response.json()["data"]["compatibility_percentage"]

        # Get detailed result
        detailed_response = client.post("/api/compatibility/detailed", json=payload)
        detailed_percentage = detailed_response.json()["data"]["compatibility_percentage"]

        # Percentages should be identical
        assert quick_percentage == detailed_percentage

    def test_batch_single_candidate_vs_quick(self):
        """Test that batch with 1 candidate matches quick endpoint"""
        payload_quick = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        payload_batch = {
            "user_kundali": SAMPLE_KUNDALI_A,
            "candidates": [SAMPLE_KUNDALI_B],
            "relationship_type": "romantic"
        }

        # Get quick result
        quick_response = client.post("/api/compatibility/quick", json=payload_quick)
        quick_percentage = quick_response.json()["data"]["compatibility_percentage"]

        # Get batch result
        batch_response = client.post("/api/compatibility/batch", json=payload_batch)
        batch_percentage = batch_response.json()["data"][0]["compatibility_percentage"]

        # Percentages should match
        assert quick_percentage == batch_percentage

    def test_response_format_consistency(self):
        """Test that all endpoints return consistent response format"""
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/quick", json=payload)
        data = response.json()

        # Check APIResponse format
        assert "success" in data
        assert "status" in data
        assert "message" in data
        assert "timestamp" in data
        assert "data" in data


@pytest.mark.asyncio
class TestCompatibilityEdgeCases:
    """Test edge cases and error scenarios"""

    def test_same_kundali_compatibility(self):
        """Test compatibility of same person with themselves"""
        payload = {
            "kundali_a": SAMPLE_KUNDALI_A,
            "kundali_b": SAMPLE_KUNDALI_A,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/quick", json=payload)

        assert response.status_code == 200
        # Same person should have high compatibility
        percentage = response.json()["data"]["compatibility_percentage"]
        assert percentage >= 50

    def test_compatibility_with_missing_planets(self):
        """Test compatibility when planet data is incomplete"""
        incomplete_kundali = {
            "user_id": "user_incomplete",
            "name": "Incomplete Person",
            "dob": "1990-05-15",
            "tob": "10:30:00",
            "location": {"latitude": 28.7041, "longitude": 77.1025, "timezone": 5.5},
            "sun_sign": "Taurus",
            "moon_sign": "Libra",
            "ascendant": "Gemini",
            "planets": {}
        }

        payload = {
            "kundali_a": incomplete_kundali,
            "kundali_b": SAMPLE_KUNDALI_B,
            "relationship_type": "romantic"
        }

        response = client.post("/api/compatibility/quick", json=payload)

        # Should either handle gracefully or return error
        assert response.status_code in [200, 400, 422]
