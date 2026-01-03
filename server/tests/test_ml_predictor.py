"""
Unit tests for ML predictor module.

Tests predict() output shape, types, and MLScoreBox validation.
"""

import pytest
import numpy as np
from pathlib import Path

from server.ml.predictor import KundaliMLPredictor, get_predictor, predict
from server.pydantic_schemas.ml_response import MLScoreBox


class TestKundaliMLPredictor:
    """Tests for KundaliMLPredictor class."""

    def test_predictor_loads_successfully(self):
        """Predictor should load models without error."""
        predictor = KundaliMLPredictor()
        assert predictor.loaded is True
        assert predictor.scaler is not None
        assert predictor.xgb_model is not None
        assert len(predictor.feature_names) > 0
        assert len(predictor.target_names) > 0

    def test_get_feature_names(self):
        """Should return list of feature names."""
        predictor = KundaliMLPredictor()
        features = predictor.get_feature_names()

        assert isinstance(features, list)
        assert len(features) > 0
        assert all(isinstance(f, str) for f in features)

    def test_get_target_names(self):
        """Should return list of target names."""
        predictor = KundaliMLPredictor()
        targets = predictor.get_target_names()

        assert isinstance(targets, list)
        assert len(targets) == 8  # 8 targets expected
        assert all(isinstance(t, str) for t in targets)

    def test_get_model_info(self):
        """Should return model metadata."""
        predictor = KundaliMLPredictor()
        info = predictor.get_model_info()

        assert isinstance(info, dict)
        assert "version" in info
        assert "features" in info
        assert "targets" in info
        assert "loaded" in info
        assert info["loaded"] is True

    def test_predict_returns_dict(self):
        """predict() must return dict, never list."""
        predictor = KundaliMLPredictor()

        # Create sample features (all zeros)
        features_dict = {fname: 0.0 for fname in predictor.feature_names}

        result = predictor.predict(features_dict)

        # CRITICAL: Must be dict
        assert isinstance(result, dict), f"Expected dict, got {type(result).__name__}"
        assert not isinstance(result, list), "Result must not be a list"

    def test_predict_returns_ml_score_boxes(self):
        """Each prediction value must be MLScoreBox."""
        predictor = KundaliMLPredictor()

        features_dict = {fname: 0.5 for fname in predictor.feature_names}
        result = predictor.predict(features_dict)

        # Check each target has MLScoreBox
        for target_name in predictor.target_names:
            assert target_name in result, f"Missing target: {target_name}"

            score_box = result[target_name]
            assert isinstance(score_box, MLScoreBox), f"{target_name} is not MLScoreBox"

            # Validate MLScoreBox fields
            assert hasattr(score_box, "score")
            assert hasattr(score_box, "confidence")
            assert hasattr(score_box, "model_version")

            # Validate types
            assert isinstance(score_box.score, float)
            assert isinstance(score_box.confidence, float)
            assert isinstance(score_box.model_version, str)

            # Validate ranges
            assert 0.0 <= score_box.score <= 1.0, f"Score out of range: {score_box.score}"
            assert 0.0 <= score_box.confidence <= 1.0, f"Confidence out of range: {score_box.confidence}"

    def test_predict_with_valid_features(self):
        """Should predict successfully with valid features."""
        predictor = KundaliMLPredictor()

        # Create realistic features
        features_dict = {fname: np.random.rand() for fname in predictor.feature_names}

        result = predictor.predict(features_dict)

        assert isinstance(result, dict)
        assert len(result) >= len(predictor.target_names)  # May include metadata

        # Check all targets present
        for target_name in predictor.target_names:
            assert target_name in result

    def test_predict_includes_inference_time(self):
        """Result should include inference time metadata."""
        predictor = KundaliMLPredictor()

        features_dict = {fname: 0.5 for fname in predictor.feature_names}
        result = predictor.predict(features_dict)

        assert "_inference_time_ms" in result
        assert isinstance(result["_inference_time_ms"], (int, float))
        assert result["_inference_time_ms"] >= 0

    def test_predict_with_missing_features(self):
        """Missing features should default to 0.0."""
        predictor = KundaliMLPredictor()

        # Partial features
        features_dict = {fname: 1.0 for fname in predictor.feature_names[:10]}

        result = predictor.predict(features_dict)

        # Should still work (missing features default to 0)
        assert isinstance(result, dict)
        assert len(result) >= len(predictor.target_names)

    def test_predict_score_clipping(self):
        """Scores should be clipped to [0, 1] range."""
        predictor = KundaliMLPredictor()

        # Extreme features that might produce out-of-range predictions
        features_dict = {fname: 100.0 for fname in predictor.feature_names}

        result = predictor.predict(features_dict)

        for target_name in predictor.target_names:
            score = result[target_name].score
            assert 0.0 <= score <= 1.0, f"Score not clipped: {score}"

    def test_predict_batch(self):
        """Should handle batch predictions."""
        predictor = KundaliMLPredictor()

        features_list = [
            {fname: 0.3 for fname in predictor.feature_names},
            {fname: 0.7 for fname in predictor.feature_names}
        ]

        results = predictor.predict_batch(features_list)

        assert isinstance(results, list)
        assert len(results) == 2

        for result in results:
            assert isinstance(result, dict)
            for target_name in predictor.target_names:
                assert target_name in result
                assert isinstance(result[target_name], MLScoreBox)


class TestGlobalPredictor:
    """Tests for global predictor singleton."""

    def test_get_predictor_singleton(self):
        """get_predictor() should return same instance."""
        predictor1 = get_predictor()
        predictor2 = get_predictor()

        assert predictor1 is predictor2

    def test_global_predict_function(self):
        """Global predict() function should work."""
        predictor = get_predictor()
        features_dict = {fname: 0.5 for fname in predictor.feature_names}

        result = predict(features_dict)

        assert isinstance(result, dict)
        for target_name in predictor.target_names:
            assert target_name in result
            assert isinstance(result[target_name], MLScoreBox)


class TestOutputShape:
    """Tests to ensure correct output shape (dict, not list)."""

    def test_never_returns_list(self):
        """predict() must NEVER return a list."""
        predictor = KundaliMLPredictor()
        features_dict = {fname: 0.5 for fname in predictor.feature_names}

        result = predictor.predict(features_dict)

        assert not isinstance(result, list), "CRITICAL: predict() returned list instead of dict"
        assert isinstance(result, dict), f"Expected dict, got {type(result).__name__}"

    def test_all_keys_are_strings(self):
        """All dict keys must be strings."""
        predictor = KundaliMLPredictor()
        features_dict = {fname: 0.5 for fname in predictor.feature_names}

        result = predictor.predict(features_dict)

        for key in result.keys():
            assert isinstance(key, str), f"Key {key} is not a string"

    def test_no_numeric_keys(self):
        """Dict must not have numeric keys (would indicate wrong structure)."""
        predictor = KundaliMLPredictor()
        features_dict = {fname: 0.5 for fname in predictor.feature_names}

        result = predictor.predict(features_dict)

        for key in result.keys():
            assert not isinstance(key, int), f"Found numeric key: {key}"

    def test_target_names_as_keys(self):
        """All target names must be dict keys."""
        predictor = KundaliMLPredictor()
        features_dict = {fname: 0.5 for fname in predictor.feature_names}

        result = predictor.predict(features_dict)

        for target_name in predictor.target_names:
            assert target_name in result, f"Missing target in result: {target_name}"


class TestModelVersion:
    """Tests for model version tracking."""

    def test_model_version_present(self):
        """Each MLScoreBox should have model_version."""
        predictor = KundaliMLPredictor()
        features_dict = {fname: 0.5 for fname in predictor.feature_names}

        result = predictor.predict(features_dict)

        for target_name in predictor.target_names:
            score_box = result[target_name]
            assert score_box.model_version is not None
            assert len(score_box.model_version) > 0

    def test_model_version_consistent(self):
        """All predictions should have same model version."""
        predictor = KundaliMLPredictor()
        features_dict = {fname: 0.5 for fname in predictor.feature_names}

        result = predictor.predict(features_dict)

        versions = [result[t].model_version for t in predictor.target_names]
        assert len(set(versions)) == 1, "Model versions inconsistent"
