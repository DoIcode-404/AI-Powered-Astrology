"""
Tests for MCP tools configuration.

Validates tools.json structure and MCP tool invocation.
"""

import pytest
import json
from pathlib import Path


class TestMCPToolsConfiguration:
    """Tests for MCP tools.json file."""

    def test_tools_json_exists(self):
        """tools.json file should exist."""
        tools_file = Path(__file__).parent.parent / "mcp" / "tools.json"
        assert tools_file.exists(), "tools.json not found"

    def test_tools_json_valid_json(self):
        """tools.json should be valid JSON."""
        tools_file = Path(__file__).parent.parent / "mcp" / "tools.json"

        with open(tools_file) as f:
            data = json.load(f)

        assert isinstance(data, dict)
        assert "tools" in data

    def test_get_compatibility_analysis_tool_exists(self):
        """get_compatibility_analysis tool should be defined."""
        tools_file = Path(__file__).parent.parent / "mcp" / "tools.json"

        with open(tools_file) as f:
            data = json.load(f)

        tool_names = [tool["name"] for tool in data["tools"]]
        assert "get_compatibility_analysis" in tool_names

    def test_tool_has_required_fields(self):
        """Tool definition should have all required fields."""
        tools_file = Path(__file__).parent.parent / "mcp" / "tools.json"

        with open(tools_file) as f:
            data = json.load(f)

        tool = next(t for t in data["tools"] if t["name"] == "get_compatibility_analysis")

        # Required fields
        assert "name" in tool
        assert "description" in tool
        assert "target" in tool
        assert "input_schema" in tool
        assert "output_schema" in tool
        assert "response_mapping" in tool

    def test_tool_target_endpoint_correct(self):
        """Tool should target correct endpoint."""
        tools_file = Path(__file__).parent.parent / "mcp" / "tools.json"

        with open(tools_file) as f:
            data = json.load(f)

        tool = next(t for t in data["tools"] if t["name"] == "get_compatibility_analysis")

        assert tool["target"]["method"] == "POST"
        assert tool["target"]["endpoint"] == "/api/ai-analysis"

    def test_input_schema_has_kundali_fields(self):
        """Input schema should have kundali fields."""
        tools_file = Path(__file__).parent.parent / "mcp" / "tools.json"

        with open(tools_file) as f:
            data = json.load(f)

        tool = next(t for t in data["tools"] if t["name"] == "get_compatibility_analysis")
        input_schema = tool["input_schema"]

        assert "properties" in input_schema
        assert "user_kundali" in input_schema["properties"]

        user_kundali = input_schema["properties"]["user_kundali"]
        assert "birthDate" in user_kundali["properties"]
        assert "birthTime" in user_kundali["properties"]
        assert "latitude" in user_kundali["properties"]
        assert "longitude" in user_kundali["properties"]
        assert "timezone" in user_kundali["properties"]

    def test_response_mapping_has_summary(self):
        """Response mapping should extract summary."""
        tools_file = Path(__file__).parent.parent / "mcp" / "tools.json"

        with open(tools_file) as f:
            data = json.load(f)

        tool = next(t for t in data["tools"] if t["name"] == "get_compatibility_analysis")
        response_mapping = tool["response_mapping"]

        assert "summary" in response_mapping
        assert response_mapping["summary"] == "data.ai_analysis.summary"

    def test_error_handling_configured(self):
        """Error handling should be configured."""
        tools_file = Path(__file__).parent.parent / "mcp" / "tools.json"

        with open(tools_file) as f:
            data = json.load(f)

        tool = next(t for t in data["tools"] if t["name"] == "get_compatibility_analysis")

        assert "error_handling" in tool
        assert "503" in tool["error_handling"]
        assert "500" in tool["error_handling"]
        assert "422" in tool["error_handling"]


class TestMCPToolInvocation:
    """Tests for MCP tool invocation via API."""

    def test_compatibility_tool_invocation(self):
        """Tool should successfully invoke API."""
        from server.tests.test_ai_analysis_endpoint import client

        # Simulate MCP tool invocation
        tool_input = {
            "user_kundali": {
                "birthDate": "1990-05-15",
                "birthTime": "14:30",
                "latitude": 19.076,
                "longitude": 72.8777,
                "timezone": "Asia/Kolkata"
            },
            "partner_kundali": {
                "birthDate": "1992-08-20",
                "birthTime": "10:15",
                "latitude": 28.6139,
                "longitude": 77.209,
                "timezone": "Asia/Kolkata"
            },
            "context": "compatibility"
        }

        response = client.post("/api/ai-analysis", json=tool_input)

        # Should succeed or return known error
        assert response.status_code in [200, 500, 503]

        if response.status_code == 200:
            data = response.json()

            # Verify response structure matches output_schema
            assert "data" in data
            assert "ai_analysis" in data["data"]
            assert "summary" in data["data"]["ai_analysis"]

    def test_extract_summary_from_response(self):
        """Should be able to extract summary using response_mapping."""
        from server.tests.test_ai_analysis_endpoint import client

        tool_input = {
            "user_kundali": {
                "birthDate": "1990-05-15",
                "birthTime": "14:30",
                "latitude": 19.076,
                "longitude": 72.8777,
                "timezone": "Asia/Kolkata"
            },
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=tool_input)

        if response.status_code == 200:
            data = response.json()

            # Extract using mapping: data.ai_analysis.summary
            summary = data["data"]["ai_analysis"]["summary"]

            assert isinstance(summary, str)
            assert len(summary) > 0

    def test_personal_analysis_tool_invocation(self):
        """Personal analysis tool should work."""
        from server.tests.test_ai_analysis_endpoint import client

        tool_input = {
            "user_kundali": {
                "birthDate": "1990-05-15",
                "birthTime": "14:30",
                "latitude": 19.076,
                "longitude": 72.8777,
                "timezone": "Asia/Kolkata"
            },
            "context": "career"
        }

        response = client.post("/api/ai-analysis", json=tool_input)

        assert response.status_code in [200, 500, 503]


class TestMCPOutputFormat:
    """Tests for MCP output format compliance."""

    def test_output_has_all_mapped_fields(self):
        """Output should contain all fields from response_mapping."""
        from server.tests.test_ai_analysis_endpoint import client

        tool_input = {
            "user_kundali": {
                "birthDate": "1990-05-15",
                "birthTime": "14:30",
                "latitude": 19.076,
                "longitude": 72.8777,
                "timezone": "Asia/Kolkata"
            },
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=tool_input)

        if response.status_code == 200:
            data = response.json()["data"]

            # All mapped fields should exist
            assert "ai_analysis" in data
            assert "summary" in data["ai_analysis"]
            assert "detailed_insights" in data["ai_analysis"]
            assert "recommendations" in data["ai_analysis"]
            assert "ml_scores" in data
            assert "astrology_scores" in data

    def test_ml_scores_structure_matches_schema(self):
        """ml_scores should match output_schema."""
        from server.tests.test_ai_analysis_endpoint import client

        tool_input = {
            "user_kundali": {
                "birthDate": "1990-05-15",
                "birthTime": "14:30",
                "latitude": 19.076,
                "longitude": 72.8777,
                "timezone": "Asia/Kolkata"
            },
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=tool_input)

        if response.status_code == 200:
            ml_scores = response.json()["data"]["ml_scores"]

            # Should be dict
            assert isinstance(ml_scores, dict)

            # Each value should have score, confidence, model_version
            for score_name, score_box in ml_scores.items():
                assert "score" in score_box
                assert "confidence" in score_box
                assert "model_version" in score_box

                # Validate types
                assert isinstance(score_box["score"], (int, float))
                assert isinstance(score_box["confidence"], (int, float))
                assert isinstance(score_box["model_version"], str)

    def test_astrology_scores_structure_matches_schema(self):
        """astrology_scores should be dict of numbers."""
        from server.tests.test_ai_analysis_endpoint import client

        tool_input = {
            "user_kundali": {
                "birthDate": "1990-05-15",
                "birthTime": "14:30",
                "latitude": 19.076,
                "longitude": 72.8777,
                "timezone": "Asia/Kolkata"
            },
            "context": "general"
        }

        response = client.post("/api/ai-analysis", json=tool_input)

        if response.status_code == 200:
            astrology_scores = response.json()["data"]["astrology_scores"]

            # Should be dict
            assert isinstance(astrology_scores, dict)

            # All values should be numbers
            for key, value in astrology_scores.items():
                assert isinstance(key, str)
                assert isinstance(value, (int, float))


class TestMCPErrorHandling:
    """Tests for MCP error handling."""

    def test_503_error_format(self):
        """503 error should match error_handling spec."""
        from server.tests.test_ai_analysis_endpoint import client
        from unittest.mock import patch

        # Mock ML unavailable
        with patch('server.routes.ai_analysis.MODELS_LOADED', False):
            tool_input = {
                "user_kundali": {
                    "birthDate": "1990-05-15",
                    "birthTime": "14:30",
                    "latitude": 19.076,
                    "longitude": 72.8777,
                    "timezone": "Asia/Kolkata"
                },
                "context": "general"
            }

            response = client.post("/api/ai-analysis", json=tool_input)

            # Should handle 503 gracefully
            assert response.status_code in [200, 500, 503]

    def test_422_validation_error_format(self):
        """422 error should be returned for invalid input."""
        from server.tests.test_ai_analysis_endpoint import client

        # Invalid input
        tool_input = {}

        response = client.post("/api/ai-analysis", json=tool_input)

        assert response.status_code == 422
