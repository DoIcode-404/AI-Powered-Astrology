"""
Unit tests for ML response schemas.

Tests validation logic, type safety, and error handling for AI analysis responses.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from server.pydantic_schemas.ml_response import (
    MLScoreBox,
    AIAnalysisSection,
    AnalysisMetadata,
    AIAnalysisData,
    AIAnalysisResponse,
    AIAnalysisErrorResponse,
    ResponseStatus
)


class TestMLScoreBox:
    """Tests for MLScoreBox validation."""

    def test_valid_score_box(self):
        """Valid MLScoreBox should pass validation."""
        box = MLScoreBox(
            score=0.75,
            confidence=0.92,
            model_version="v1.2"
        )
        assert box.score == 0.75
        assert box.confidence == 0.92
        assert box.model_version == "v1.2"

    def test_score_out_of_range_high(self):
        """Score > 1.0 should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            MLScoreBox(score=1.5, confidence=0.9, model_version="v1.0")
        assert "score" in str(exc_info.value).lower()

    def test_score_out_of_range_low(self):
        """Score < 0.0 should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            MLScoreBox(score=-0.1, confidence=0.9, model_version="v1.0")
        assert "score" in str(exc_info.value).lower()

    def test_confidence_out_of_range(self):
        """Confidence outside [0, 1] should raise ValidationError."""
        with pytest.raises(ValidationError):
            MLScoreBox(score=0.5, confidence=1.2, model_version="v1.0")

    def test_missing_model_version(self):
        """Missing model_version should raise ValidationError."""
        with pytest.raises(ValidationError):
            MLScoreBox(score=0.5, confidence=0.9)


class TestAIAnalysisSection:
    """Tests for AIAnalysisSection validation."""

    def test_valid_analysis_section(self):
        """Valid AIAnalysisSection should pass validation."""
        section = AIAnalysisSection(
            summary="Strong compatibility",
            detailed_insights=["Good career match", "Financial stability"],
            recommendations=["Joint planning recommended"]
        )
        assert section.summary == "Strong compatibility"
        assert len(section.detailed_insights) == 2

    def test_empty_summary_raises_error(self):
        """Empty summary should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AIAnalysisSection(summary="", detailed_insights=[], recommendations=[])
        assert "summary" in str(exc_info.value).lower()

    def test_whitespace_summary_raises_error(self):
        """Whitespace-only summary should raise ValidationError."""
        with pytest.raises(ValidationError):
            AIAnalysisSection(summary="   ", detailed_insights=[], recommendations=[])

    def test_default_empty_lists(self):
        """Lists should default to empty if not provided."""
        section = AIAnalysisSection(summary="Test summary")
        assert section.detailed_insights == []
        assert section.recommendations == []


class TestAnalysisMetadata:
    """Tests for AnalysisMetadata validation."""

    def test_valid_metadata(self):
        """Valid metadata should pass validation."""
        metadata = AnalysisMetadata(
            calculation_timestamp=datetime.utcnow(),
            ml_inference_time_ms=45.2,
            astro_calc_time_ms=120.5,
            total_time_ms=165.7
        )
        assert metadata.ml_inference_time_ms == 45.2

    def test_negative_time_raises_error(self):
        """Negative time values should raise ValidationError."""
        with pytest.raises(ValidationError):
            AnalysisMetadata(
                calculation_timestamp=datetime.utcnow(),
                ml_inference_time_ms=-10,
                astro_calc_time_ms=120,
                total_time_ms=110
            )

    def test_parse_iso_timestamp(self):
        """ISO string timestamp should be parsed to datetime."""
        metadata = AnalysisMetadata(
            calculation_timestamp="2025-12-08T10:30:00Z",
            ml_inference_time_ms=45,
            astro_calc_time_ms=120,
            total_time_ms=165
        )
        assert isinstance(metadata.calculation_timestamp, datetime)


class TestAIAnalysisData:
    """Tests for AIAnalysisData validation."""

    def get_valid_payload(self):
        """Helper to create valid AIAnalysisData payload."""
        return {
            "ml_scores": {
                "wealth": MLScoreBox(score=0.75, confidence=0.92, model_version="v1.2"),
                "career": MLScoreBox(score=0.68, confidence=0.88, model_version="v1.2")
            },
            "astrology_scores": {
                "guna_milan": 24,
                "tara": 3,
                "yoni": 4
            },
            "ai_analysis": AIAnalysisSection(
                summary="High compatibility",
                detailed_insights=["Good match"],
                recommendations=["Joint planning"]
            ),
            "metadata": AnalysisMetadata(
                calculation_timestamp=datetime.utcnow(),
                ml_inference_time_ms=45.2,
                astro_calc_time_ms=120.5,
                total_time_ms=165.7
            )
        }

    def test_valid_analysis_data(self):
        """Valid AIAnalysisData should pass validation."""
        data = AIAnalysisData(**self.get_valid_payload())
        assert "wealth" in data.ml_scores
        assert "guna_milan" in data.astrology_scores

    def test_ml_scores_as_list_raises_error(self):
        """ml_scores as List should raise ValidationError."""
        payload = self.get_valid_payload()
        payload["ml_scores"] = [{"score": 0.5}]  # Wrong: List instead of Dict

        with pytest.raises(ValidationError) as exc_info:
            AIAnalysisData(**payload)
        error_msg = str(exc_info.value).lower()
        assert "dict" in error_msg and "list" in error_msg

    def test_empty_ml_scores_raises_error(self):
        """Empty ml_scores dict should raise ValidationError."""
        payload = self.get_valid_payload()
        payload["ml_scores"] = {}

        with pytest.raises(ValidationError) as exc_info:
            AIAnalysisData(**payload)
        assert "cannot be empty" in str(exc_info.value).lower()

    def test_astrology_scores_as_list_raises_error(self):
        """astrology_scores as List should raise ValidationError."""
        payload = self.get_valid_payload()
        payload["astrology_scores"] = [24, 3, 4]  # Wrong: List instead of Dict

        with pytest.raises(ValidationError) as exc_info:
            AIAnalysisData(**payload)
        error_msg = str(exc_info.value).lower()
        assert "dict" in error_msg and "list" in error_msg

    def test_empty_astrology_scores_raises_error(self):
        """Empty astrology_scores dict should raise ValidationError."""
        payload = self.get_valid_payload()
        payload["astrology_scores"] = {}

        with pytest.raises(ValidationError) as exc_info:
            AIAnalysisData(**payload)
        assert "cannot be empty" in str(exc_info.value).lower()

    def test_astrology_score_wrong_type_raises_error(self):
        """Non-numeric astrology score should raise ValidationError."""
        payload = self.get_valid_payload()
        payload["astrology_scores"] = {"guna_milan": "invalid"}  # Wrong: non-numeric string

        with pytest.raises(ValidationError):
            AIAnalysisData(**payload)


class TestAIAnalysisResponse:
    """Tests for AIAnalysisResponse validation."""

    def get_valid_response_payload(self):
        """Helper to create valid AIAnalysisResponse payload."""
        return {
            "status": "success",
            "success": True,
            "data": {
                "ml_scores": {
                    "wealth": {
                        "score": 0.75,
                        "confidence": 0.92,
                        "model_version": "v1.2"
                    }
                },
                "astrology_scores": {
                    "guna_milan": 24
                },
                "ai_analysis": {
                    "summary": "High compatibility",
                    "detailed_insights": ["Good match"],
                    "recommendations": ["Joint planning"]
                },
                "metadata": {
                    "calculation_timestamp": datetime.utcnow().isoformat(),
                    "ml_inference_time_ms": 45.2,
                    "astro_calc_time_ms": 120.5,
                    "total_time_ms": 165.7
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    def test_valid_response(self):
        """Valid AIAnalysisResponse should pass validation."""
        response = AIAnalysisResponse(**self.get_valid_response_payload())
        assert response.success is True
        assert response.status == ResponseStatus.SUCCESS

    def test_success_without_data_raises_error(self):
        """Success response without data should raise ValidationError."""
        payload = self.get_valid_response_payload()
        payload["data"] = None

        with pytest.raises(ValidationError):
            AIAnalysisResponse(**payload)

    def test_serialization_round_trip(self):
        """Response should serialize and deserialize correctly."""
        response = AIAnalysisResponse(**self.get_valid_response_payload())
        json_str = response.model_dump_json()

        # Parse back from JSON
        import json
        parsed = json.loads(json_str)

        assert parsed["success"] is True
        assert "ml_scores" in parsed["data"]

    def test_example_schema_is_valid(self):
        """Schema example should pass validation."""
        example = AIAnalysisResponse.model_config['json_schema_extra']['example']
        response = AIAnalysisResponse(**example)
        assert response.success is True


class TestAIAnalysisErrorResponse:
    """Tests for AIAnalysisErrorResponse validation."""

    def test_valid_error_response(self):
        """Valid error response should pass validation."""
        error_response = AIAnalysisErrorResponse(
            error_message="ML model unavailable",
            error_code="ML_SERVICE_DOWN"
        )
        assert error_response.success is False
        assert error_response.status == ResponseStatus.ERROR

    def test_error_with_details(self):
        """Error response with details should pass validation."""
        error_response = AIAnalysisErrorResponse(
            error_message="Validation failed",
            error_code="VALIDATION_ERROR",
            details={"field": "kundali_id", "reason": "Invalid format"}
        )
        assert error_response.details is not None
        assert "field" in error_response.details


class TestTypeSafety:
    """Tests to prevent Map<String, dynamic> vs List<dynamic> errors."""

    def test_cannot_pass_list_as_ml_scores(self):
        """Passing List instead of Dict for ml_scores must fail."""
        with pytest.raises(ValidationError):
            AIAnalysisData(
                ml_scores=[0.75, 0.68],  # WRONG: List
                astrology_scores={"guna_milan": 24},
                ai_analysis=AIAnalysisSection(summary="Test"),
                metadata=AnalysisMetadata(
                    calculation_timestamp=datetime.utcnow(),
                    ml_inference_time_ms=45,
                    astro_calc_time_ms=120,
                    total_time_ms=165
                )
            )

    def test_cannot_pass_list_as_astrology_scores(self):
        """Passing List instead of Dict for astrology_scores must fail."""
        with pytest.raises(ValidationError):
            AIAnalysisData(
                ml_scores={"wealth": MLScoreBox(score=0.75, confidence=0.9, model_version="v1")},
                astrology_scores=[24, 3, 4],  # WRONG: List
                ai_analysis=AIAnalysisSection(summary="Test"),
                metadata=AnalysisMetadata(
                    calculation_timestamp=datetime.utcnow(),
                    ml_inference_time_ms=45,
                    astro_calc_time_ms=120,
                    total_time_ms=165
                )
            )

    def test_mixed_types_in_dict_values_fail(self):
        """Mixed types in dict values should fail validation."""
        with pytest.raises(ValidationError):
            AIAnalysisData(
                ml_scores={
                    "wealth": MLScoreBox(score=0.75, confidence=0.9, model_version="v1"),
                    "career": {"score": 0.5}  # WRONG: Plain dict instead of MLScoreBox
                },
                astrology_scores={"guna_milan": 24},
                ai_analysis=AIAnalysisSection(summary="Test"),
                metadata=AnalysisMetadata(
                    calculation_timestamp=datetime.utcnow(),
                    ml_inference_time_ms=45,
                    astro_calc_time_ms=120,
                    total_time_ms=165
                )
            )
