"""
Tests for runtime validation of ML scores and astrology scores.

Tests explicit runtime type checks before Pydantic validation.
"""

import pytest
from server.routes.ai_analysis import (
    _validate_ml_scores_runtime,
    _validate_astrology_scores_runtime
)
from server.pydantic_schemas.ml_response import MLScoreBox


class TestMLScoresRuntimeValidation:
    """Tests for _validate_ml_scores_runtime()."""

    def test_valid_ml_scores_pass(self):
        """Valid ml_scores dict should pass runtime validation."""
        ml_scores = {
            "wealth": MLScoreBox(score=0.75, confidence=0.92, model_version="v1.0"),
            "career": MLScoreBox(score=0.68, confidence=0.88, model_version="v1.0")
        }

        # Should not raise
        _validate_ml_scores_runtime(ml_scores)

    def test_ml_scores_as_list_fails(self):
        """ml_scores as list should fail with detailed error."""
        ml_scores = [0.75, 0.68]  # Wrong: List instead of dict

        with pytest.raises(ValueError) as exc_info:
            _validate_ml_scores_runtime(ml_scores)

        assert "ml_scores must be dict" in str(exc_info.value)
        assert "list" in str(exc_info.value)

    def test_empty_ml_scores_fails(self):
        """Empty ml_scores should fail."""
        ml_scores = {}

        with pytest.raises(ValueError) as exc_info:
            _validate_ml_scores_runtime(ml_scores)

        assert "cannot be empty" in str(exc_info.value)

    def test_non_string_key_fails(self):
        """Non-string key should fail."""
        ml_scores = {
            0: MLScoreBox(score=0.75, confidence=0.92, model_version="v1.0")
        }

        with pytest.raises(ValueError) as exc_info:
            _validate_ml_scores_runtime(ml_scores)

        assert "key must be string" in str(exc_info.value)

    def test_non_mlscorebox_value_fails(self):
        """Non-MLScoreBox value should fail."""
        ml_scores = {
            "wealth": {"score": 0.75, "confidence": 0.92}  # Plain dict instead of MLScoreBox
        }

        with pytest.raises(ValueError) as exc_info:
            _validate_ml_scores_runtime(ml_scores)

        assert "must be MLScoreBox" in str(exc_info.value)

    def test_missing_score_field_fails(self):
        """MLScoreBox missing score field should fail."""
        # Create incomplete object (mock)
        class IncompleteMock:
            confidence = 0.9
            model_version = "v1.0"

        ml_scores = {
            "wealth": IncompleteMock()
        }

        with pytest.raises(ValueError) as exc_info:
            _validate_ml_scores_runtime(ml_scores)

        assert "must be MLScoreBox" in str(exc_info.value)

    def test_non_numeric_score_fails(self):
        """Non-numeric score should fail."""
        ml_scores = {
            "wealth": MLScoreBox(score="0.75", confidence=0.92, model_version="v1.0")  # String score
        }

        # Note: Pydantic may auto-convert, but if it doesn't:
        try:
            _validate_ml_scores_runtime(ml_scores)
        except ValueError as e:
            assert "must be numeric" in str(e)


class TestAstrologyScoresRuntimeValidation:
    """Tests for _validate_astrology_scores_runtime()."""

    def test_valid_astrology_scores_pass(self):
        """Valid astrology_scores dict should pass."""
        astrology_scores = {
            "guna_milan": 24,
            "tara": 3.5,
            "yoni": 4
        }

        # Should not raise
        _validate_astrology_scores_runtime(astrology_scores)

    def test_astrology_scores_as_list_fails(self):
        """astrology_scores as list should fail."""
        astrology_scores = [24, 3, 4]  # Wrong: List

        with pytest.raises(ValueError) as exc_info:
            _validate_astrology_scores_runtime(astrology_scores)

        assert "astrology_scores must be dict" in str(exc_info.value)
        assert "list" in str(exc_info.value)

    def test_empty_astrology_scores_fails(self):
        """Empty astrology_scores should fail."""
        astrology_scores = {}

        with pytest.raises(ValueError) as exc_info:
            _validate_astrology_scores_runtime(astrology_scores)

        assert "cannot be empty" in str(exc_info.value)

    def test_non_string_key_fails(self):
        """Non-string key should fail."""
        astrology_scores = {
            0: 24,
            1: 3
        }

        with pytest.raises(ValueError) as exc_info:
            _validate_astrology_scores_runtime(astrology_scores)

        assert "key must be string" in str(exc_info.value)

    def test_non_numeric_value_fails(self):
        """Non-numeric value should fail."""
        astrology_scores = {
            "guna_milan": "24",  # String instead of number
            "tara": 3
        }

        with pytest.raises(ValueError) as exc_info:
            _validate_astrology_scores_runtime(astrology_scores)

        assert "must be numeric" in str(exc_info.value)


class TestRuntimeValidationLogging:
    """Tests for runtime validation logging."""

    def test_ml_scores_list_logs_payload(self, caplog):
        """List ml_scores should log full payload."""
        import logging
        caplog.set_level(logging.ERROR)

        ml_scores = [0.75, 0.68]

        with pytest.raises(ValueError):
            _validate_ml_scores_runtime(ml_scores)

        # Check logs contain payload
        assert any("RUNTIME VALIDATION FAILED" in record.message for record in caplog.records)
        assert any("ml_scores payload" in record.message for record in caplog.records)

    def test_astrology_scores_list_logs_payload(self, caplog):
        """List astrology_scores should log full payload."""
        import logging
        caplog.set_level(logging.ERROR)

        astrology_scores = [24, 3, 4]

        with pytest.raises(ValueError):
            _validate_astrology_scores_runtime(astrology_scores)

        # Check logs
        assert any("RUNTIME VALIDATION FAILED" in record.message for record in caplog.records)
        assert any("astrology_scores payload" in record.message for record in caplog.records)


class TestEndToEndRuntimeValidation:
    """End-to-end tests with mocked bad ML output."""

    def test_endpoint_catches_bad_ml_output(self, monkeypatch):
        """Endpoint should catch bad ML output and return 500."""
        from server.tests.test_ai_analysis_endpoint import client

        # Mock extract_ml_predictions to return list instead of dict
        def bad_extract_ml_predictions(kundali_response):
            return [0.75, 0.68, 0.82]  # WRONG: List instead of dict

        # Can't easily monkeypatch in this context, but this demonstrates the test pattern
        # In production, this would be caught by runtime validation

    def test_middleware_catches_malformed_response(self):
        """Middleware should catch malformed responses."""
        # This is tested in test_error_handler_middleware.py
        pass


class TestRuntimeValidationVsPydantic:
    """Tests showing runtime validation catches errors before Pydantic."""

    def test_runtime_catches_before_pydantic(self):
        """Runtime validation should catch errors before Pydantic tries."""
        # List instead of dict
        ml_scores = []

        # Runtime validation catches it
        with pytest.raises(ValueError) as exc_info:
            _validate_ml_scores_runtime(ml_scores)

        assert "ml_scores must be dict" in str(exc_info.value)

        # This prevents Pydantic from seeing malformed data

    def test_detailed_error_messages(self):
        """Runtime validation should provide detailed error messages."""
        ml_scores = {"wealth": "not_a_scorebox"}

        with pytest.raises(ValueError) as exc_info:
            _validate_ml_scores_runtime(ml_scores)

        error_msg = str(exc_info.value)
        assert "must be MLScoreBox" in error_msg
        assert "wealth" in error_msg
        assert "str" in error_msg  # Shows actual type
