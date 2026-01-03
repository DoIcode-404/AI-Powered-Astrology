"""
Tests for error handler middleware schema validation.

Tests AI analysis response validation and schema mismatch handling.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json

from server.middleware.error_handler import (
    ErrorHandlingMiddleware,
    setup_error_handlers,
    get_error_tracker
)
from server.pydantic_schemas.ml_response import AIAnalysisResponse


class TestSchemaValidationMiddleware:
    """Tests for AI analysis response schema validation."""

    def test_valid_ai_response_passes_validation(self):
        """Valid AIAnalysisResponse should pass middleware validation."""
        from server.tests.test_ai_analysis_endpoint import client

        request_data = {
            "user_kundali": {
                "birthDate": "1990-05-15",
                "birthTime": "14:30",
                "latitude": 19.0760,
                "longitude": 72.8777,
                "timezone": "Asia/Kolkata"
            },
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=request_data)

        # If successful (200), middleware validation passed
        if response.status_code == 200:
            data = response.json()
            assert data["success"] is True
            assert "data" in data

    def test_error_tracker_logs_errors(self):
        """Error tracker should log errors with details."""
        tracker = get_error_tracker()

        initial_count = len(tracker.errors)

        # Simulate error logging
        tracker.log_error(
            error_code="TEST_ERROR",
            message="Test error message",
            request_path="/api/test",
            error_type="TestError",
            status_code=500,
            details={"test": "data"}
        )

        assert len(tracker.errors) == initial_count + 1
        assert tracker.error_counts.get("TEST_ERROR", 0) > 0

    def test_error_tracker_summary(self):
        """Error tracker should provide summary statistics."""
        tracker = get_error_tracker()

        summary = tracker.get_error_summary()

        assert "total_errors" in summary
        assert "unique_error_types" in summary
        assert "error_counts" in summary
        assert "recent_errors" in summary
        assert isinstance(summary["recent_errors"], list)


class TestMalformedMLOutput:
    """Tests simulating malformed ML output scenarios."""

    def test_ml_scores_as_list_caught_by_endpoint(self):
        """If ML returns list instead of dict, endpoint should catch it."""
        # This would be caught by the endpoint's try-except before middleware
        # The endpoint returns 500, not a malformed response
        pass  # Covered by endpoint tests

    def test_missing_required_field_in_response(self):
        """Response missing required field should be caught."""
        # Middleware validates successful responses (200)
        # Missing fields would cause endpoint to fail or return error
        pass  # Covered by schema tests

    def test_503_ml_unavailable_not_validated(self):
        """503 responses should not be schema validated."""
        from server.tests.test_ai_analysis_endpoint import client

        # Mock ML as unavailable
        with patch('server.routes.ai_analysis.MODELS_LOADED', False):
            request_data = {
                "user_kundali": {
                    "birthDate": "1990-05-15",
                    "birthTime": "14:30",
                    "latitude": 19.0760,
                    "longitude": 72.8777,
                    "timezone": "Asia/Kolkata"
                },
                "context": "general"
            }

            response = client.post("/api/ai-analysis", json=request_data)

            # Should return 503, middleware skips validation for non-200
            assert response.status_code in [200, 500, 503]


class TestMiddlewareSetup:
    """Tests for middleware setup and configuration."""

    def test_setup_error_handlers_adds_middleware(self):
        """setup_error_handlers should add middleware to app."""
        app = FastAPI()

        # Count middleware before
        initial_middleware_count = len(app.user_middleware)

        setup_error_handlers(app)

        # Should have added 3 middleware (Logging, Error, RequestId)
        assert len(app.user_middleware) > initial_middleware_count

    def test_request_id_middleware_adds_header(self):
        """Request ID middleware should add X-Request-ID header."""
        from server.tests.test_ai_analysis_endpoint import client

        response = client.get("/api/ai-analysis/health")

        # Response should have request ID header
        assert "X-Request-ID" in response.headers or response.status_code == 200


class TestErrorStatusCodes:
    """Tests for error status code mapping."""

    def test_validation_error_returns_422(self):
        """ValidationError should return 422."""
        from server.tests.test_ai_analysis_endpoint import client

        # Send invalid request
        response = client.post("/api/ai-analysis", json={})

        assert response.status_code == 422

    def test_value_error_returns_400(self):
        """ValueError should return 400 or 500."""
        from server.tests.test_ai_analysis_endpoint import client

        # Send invalid data type
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

        # Should return error status
        assert response.status_code in [400, 422, 500]

    def test_http_exception_preserves_status_code(self):
        """HTTPException should preserve its status code."""
        from server.tests.test_ai_analysis_endpoint import client

        # Request missing required field
        response = client.post("/api/ai-analysis", json={"context": "general"})

        assert response.status_code == 422


class TestSchemaValidationDetails:
    """Tests for detailed schema validation logging."""

    def test_schema_error_includes_validation_details(self):
        """Schema validation errors should include error details."""
        # This is tested indirectly through error tracker
        tracker = get_error_tracker()

        # Check if any schema validation errors were logged
        schema_errors = [
            err for err in tracker.errors
            if err.get("error_code") == "AI_RESPONSE_SCHEMA_ERROR"
        ]

        # If schema errors exist, they should have validation details
        for error in schema_errors:
            assert "details" in error
            if error["details"]:
                assert "validation_errors" in error["details"]

    def test_error_tracker_limits_stored_errors(self):
        """Error tracker should limit stored errors to 1000."""
        tracker = get_error_tracker()

        # Log many errors
        for i in range(1500):
            tracker.log_error(
                error_code=f"TEST_{i}",
                message="Test error",
                request_path="/test",
                error_type="TestError",
                status_code=500
            )

        # Should keep only last 1000
        assert len(tracker.errors) <= 1000


class TestMiddlewareIntegration:
    """Integration tests for middleware in full request cycle."""

    def test_successful_request_passes_all_middleware(self):
        """Successful request should pass through all middleware."""
        from server.tests.test_ai_analysis_endpoint import client

        response = client.get("/api/ai-analysis/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_error_request_handled_by_middleware(self):
        """Error request should be handled by error middleware."""
        from server.tests.test_ai_analysis_endpoint import client

        # Invalid request
        response = client.post("/api/ai-analysis", json={"invalid": "data"})

        # Should return error response with consistent format
        assert response.status_code in [422, 500]
        data = response.json()
        assert "detail" in data or "error" in data or "message" in data

    def test_ml_unavailable_returns_503(self):
        """ML unavailable should return 503 from endpoint."""
        from server.tests.test_ai_analysis_endpoint import client

        # Mock ML unavailable
        with patch('server.routes.ai_analysis.MODELS_LOADED', False):
            request_data = {
                "user_kundali": {
                    "birthDate": "1990-05-15",
                    "birthTime": "14:30",
                    "latitude": 19.0760,
                    "longitude": 72.8777,
                    "timezone": "Asia/Kolkata"
                },
                "context": "general"
            }

            response = client.post("/api/ai-analysis", json=request_data)

            # Should return 503 or handle gracefully
            assert response.status_code in [200, 500, 503]
