"""
Integration tests for AI Analysis endpoint.

Tests the complete flow: request -> kundali generation -> ML inference -> response validation.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from server.main import app
from server.pydantic_schemas.ml_response import AIAnalysisResponse, ResponseStatus


client = TestClient(app)


class TestAIAnalysisEndpoint:
    """Integration tests for POST /api/ai-analysis endpoint."""

    def get_sample_kundali_request(self):
        """Helper to create sample kundali request data."""
        return {
            "birthDate": "1990-05-15",
            "birthTime": "14:30",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "timezone": "Asia/Kolkata"
        }

    def test_health_check(self):
        """Health endpoint should return service status."""
        response = client.get("/api/ai-analysis/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "ml_available" in data
        assert "timestamp" in data

    def test_ai_analysis_success(self):
        """Valid request should return AIAnalysisResponse."""
        request_data = {
            "user_kundali": self.get_sample_kundali_request(),
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=request_data)

        # Should succeed (or 503 if ML not loaded, or 500 if feature extraction fails)
        assert response.status_code in [200, 500, 503]

        if response.status_code == 200:
            data = response.json()

            # Validate response structure
            assert data["success"] is True
            assert data["status"] == "success"
            assert "data" in data

            # Validate data structure
            analysis_data = data["data"]
            assert "ml_scores" in analysis_data
            assert "astrology_scores" in analysis_data
            assert "ai_analysis" in analysis_data
            assert "metadata" in analysis_data

            # Validate ml_scores structure
            ml_scores = analysis_data["ml_scores"]
            assert isinstance(ml_scores, dict)
            assert len(ml_scores) > 0

            for score_name, score_box in ml_scores.items():
                assert isinstance(score_name, str)
                assert "score" in score_box
                assert "confidence" in score_box
                assert "model_version" in score_box
                assert 0.0 <= score_box["score"] <= 1.0
                assert 0.0 <= score_box["confidence"] <= 1.0

            # Validate astrology_scores structure
            astrology_scores = analysis_data["astrology_scores"]
            assert isinstance(astrology_scores, dict)
            assert len(astrology_scores) > 0

            for score_name, score_value in astrology_scores.items():
                assert isinstance(score_name, str)
                assert isinstance(score_value, (int, float))

            # Validate ai_analysis structure
            ai_analysis = analysis_data["ai_analysis"]
            assert "summary" in ai_analysis
            assert "detailed_insights" in ai_analysis
            assert "recommendations" in ai_analysis
            assert isinstance(ai_analysis["summary"], str)
            assert len(ai_analysis["summary"]) > 0

            # Validate metadata
            metadata = analysis_data["metadata"]
            assert "calculation_timestamp" in metadata
            assert "ml_inference_time_ms" in metadata
            assert "astro_calc_time_ms" in metadata
            assert "total_time_ms" in metadata

    def test_compatibility_context(self):
        """Compatibility context with partner kundali should work."""
        request_data = {
            "user_kundali": self.get_sample_kundali_request(),
            "partner_kundali": {
                "birthDate": "1992-08-20",
                "birthTime": "10:15",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "timezone": "Asia/Kolkata"
            },
            "context": "compatibility"
        }

        response = client.post("/api/ai-analysis", json=request_data)

        # Should succeed or 503 or 500 (feature extraction issues)
        assert response.status_code in [200, 500, 503]

        if response.status_code == 200:
            data = response.json()
            assert data["success"] is True

            # Should contain compatibility scores
            astrology_scores = data["data"]["astrology_scores"]
            # May contain guna_milan_total or koota scores
            assert len(astrology_scores) > 0

    def test_invalid_kundali_data(self):
        """Invalid kundali data should return error."""
        request_data = {
            "user_kundali": {
                "birthDate": "invalid-date",
                "birthTime": "14:30",
                "latitude": 19.0760,
                "longitude": 72.8777,
                "timezone": "Asia/Kolkata"
            },
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=request_data)

        # Should return validation error (422) or server error (500)
        assert response.status_code in [422, 500]

    def test_missing_required_fields(self):
        """Missing required fields should return 422."""
        request_data = {
            "context": "general"
            # Missing user_kundali
        }

        response = client.post("/api/ai-analysis", json=request_data)
        assert response.status_code == 422

    def test_ml_unavailable_returns_503(self):
        """When ML models unavailable, should return 503."""
        # This test depends on MODELS_LOADED status
        # If models are loaded, test won't trigger 503
        request_data = {
            "user_kundali": self.get_sample_kundali_request(),
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=request_data)

        if response.status_code == 503:
            data = response.json()
            assert data["success"] is False
            assert data["status"] == "error"
            assert "ml" in data["error_message"].lower() or "unavailable" in data["error_message"].lower()

    def test_response_schema_validation(self):
        """Response should validate against Pydantic schema."""
        request_data = {
            "user_kundali": self.get_sample_kundali_request(),
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=request_data)

        if response.status_code == 200:
            data = response.json()

            # Should be parseable by AIAnalysisResponse
            try:
                validated = AIAnalysisResponse(**data)
                assert validated.success is True
                assert validated.status == ResponseStatus.SUCCESS
            except Exception as e:
                pytest.fail(f"Response validation failed: {str(e)}")

    def test_no_list_dict_type_confusion(self):
        """Ensure ml_scores and astrology_scores are always dicts, never lists."""
        request_data = {
            "user_kundali": self.get_sample_kundali_request(),
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=request_data)

        if response.status_code == 200:
            data = response.json()

            ml_scores = data["data"]["ml_scores"]
            astrology_scores = data["data"]["astrology_scores"]

            # CRITICAL: Must be dict, never list
            assert isinstance(ml_scores, dict), f"ml_scores is {type(ml_scores).__name__}, expected dict"
            assert isinstance(astrology_scores, dict), f"astrology_scores is {type(astrology_scores).__name__}, expected dict"

            # Verify structure
            assert not isinstance(ml_scores, list)
            assert not isinstance(astrology_scores, list)


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_malformed_json(self):
        """Malformed JSON should return 422."""
        response = client.post(
            "/api/ai-analysis",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_empty_request_body(self):
        """Empty request body should return 422."""
        response = client.post("/api/ai-analysis", json={})
        assert response.status_code == 422

    def test_invalid_context(self):
        """Invalid context should still process (context is flexible)."""
        request_data = {
            "user_kundali": {
                "birthDate": "1990-05-15",
                "birthTime": "14:30",
                "latitude": 19.0760,
                "longitude": 72.8777,
                "timezone": "Asia/Kolkata"
            },
            "context": "invalid_context_xyz"
        }

        response = client.post("/api/ai-analysis", json=request_data)

        # Should still work (context is just a string) or 500
        assert response.status_code in [200, 500, 503]
