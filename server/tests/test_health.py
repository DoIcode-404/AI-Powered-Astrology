"""
Tests for health check endpoint.
"""

import pytest


@pytest.mark.health
class TestHealthEndpoint:
    """Test the /health endpoint."""

    def test_health_check_success(self, client):
        """Test that health check returns successful response."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["status"] == "success"

    def test_health_check_response_structure(self, client):
        """Test that health check response has expected structure."""
        response = client.get("/health")
        data = response.json()

        # Check required fields
        assert "status" in data
        assert "success" in data
        assert "data" in data
        assert "timestamp" in data
        assert "message" in data

    def test_health_check_data_fields(self, client):
        """Test that health check data contains expected fields."""
        response = client.get("/health")
        data = response.json()

        # Check data object
        assert "status" in data["data"]
        assert "timestamp" in data["data"]
        assert "ephemeris" in data["data"]
        assert "database" in data["data"]

        # Check values
        assert data["data"]["status"] == "healthy"
        assert data["data"]["ephemeris"] == "initialized"
        assert data["data"]["database"] == "connected"

    def test_health_check_timestamp_format(self, client):
        """Test that timestamp is in ISO 8601 format."""
        import re
        from datetime import datetime

        response = client.get("/health")
        data = response.json()

        # Check if timestamp is valid ISO 8601
        timestamp = data["timestamp"]
        iso_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
        assert re.match(iso_pattern, timestamp), f"Invalid timestamp format: {timestamp}"

        # Try parsing the timestamp
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Cannot parse timestamp: {timestamp}")

    def test_health_check_no_auth_required(self, client):
        """Test that health check doesn't require authentication."""
        # Health check should work without any auth headers
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_time(self, client):
        """Test that health check responds quickly."""
        import time

        start_time = time.time()
        response = client.get("/health")
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms

        assert response.status_code == 200
        # Health check should respond in less than 100ms
        assert elapsed_time < 100, f"Health check took {elapsed_time}ms"
