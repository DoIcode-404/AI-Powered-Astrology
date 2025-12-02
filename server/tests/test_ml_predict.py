"""
Tests for ML prediction endpoints.
"""

import pytest


@pytest.mark.predict
@pytest.mark.unit
class TestMLPredictEndpoint:
    """Test the /ml/predict endpoint."""

    def test_predict_with_valid_features(self, client, valid_53_features):
        """Test prediction with valid 53 features."""
        response = client.post(
            "/ml/predict",
            json={"features": valid_53_features}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["status"] == "success"

    def test_predict_response_structure(self, client, valid_53_features, expected_prediction_keys):
        """Test that prediction response has all expected keys."""
        response = client.post(
            "/ml/predict",
            json={"features": valid_53_features}
        )

        data = response.json()
        assert "status" in data
        assert "success" in data
        assert "data" in data
        assert "timestamp" in data
        assert "message" in data

    def test_predict_response_has_all_predictions(self, client, valid_53_features, expected_prediction_keys):
        """Test that prediction response contains all 8 predictions."""
        response = client.post(
            "/ml/predict",
            json={"features": valid_53_features}
        )

        data = response.json()
        predictions = data["data"]

        # Check all expected keys are present
        for key in expected_prediction_keys:
            assert key in predictions, f"Missing key: {key}"

    def test_predict_values_in_valid_range(self, client, valid_53_features):
        """Test that prediction values are between 0-100."""
        response = client.post(
            "/ml/predict",
            json={"features": valid_53_features}
        )

        data = response.json()
        predictions = data["data"]

        score_fields = [
            "career_potential",
            "wealth_potential",
            "marriage_happiness",
            "children_prospects",
            "health_status",
            "spiritual_inclination",
            "chart_strength",
            "life_ease_score",
            "average_score"
        ]

        for field in score_fields:
            value = predictions[field]
            assert 0 <= value <= 100, f"{field} out of range: {value}"

    def test_predict_has_interpretation(self, client, valid_53_features):
        """Test that prediction includes human-readable interpretation."""
        response = client.post(
            "/ml/predict",
            json={"features": valid_53_features}
        )

        data = response.json()
        predictions = data["data"]

        assert "interpretation" in predictions
        assert isinstance(predictions["interpretation"], str)
        assert len(predictions["interpretation"]) > 0

    def test_predict_invalid_feature_count_too_few(self, client):
        """Test that prediction fails with too few features."""
        response = client.post(
            "/ml/predict",
            json={"features": [1.0] * 52}  # Only 52 features
        )

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "INVALID_FEATURE_COUNT" in data["error"]["code"]

    def test_predict_invalid_feature_count_too_many(self, client):
        """Test that prediction fails with too many features."""
        response = client.post(
            "/ml/predict",
            json={"features": [1.0] * 54}  # 54 features
        )

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "INVALID_FEATURE_COUNT" in data["error"]["code"]

    def test_predict_empty_feature_list(self, client):
        """Test that prediction fails with empty feature list."""
        response = client.post(
            "/ml/predict",
            json={"features": []}
        )

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_predict_missing_features_field(self, client):
        """Test that prediction fails when features field is missing."""
        response = client.post(
            "/ml/predict",
            json={}
        )

        assert response.status_code == 422

    def test_predict_non_numeric_features(self, client):
        """Test that prediction fails with non-numeric features."""
        response = client.post(
            "/ml/predict",
            json={"features": ["string"] * 53}
        )

        assert response.status_code == 422

    def test_predict_mixed_numeric_types(self, client, valid_53_features):
        """Test that prediction works with mixed int and float features."""
        # Ensure some features are int and some are float
        mixed_features = [int(f) if i % 2 == 0 else float(f) for i, f in enumerate(valid_53_features)]

        response = client.post(
            "/ml/predict",
            json={"features": mixed_features}
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_predict_average_score_is_mean(self, client, valid_53_features):
        """Test that average_score is the mean of all 8 predictions."""
        response = client.post(
            "/ml/predict",
            json={"features": valid_53_features}
        )

        data = response.json()
        predictions = data["data"]

        scores = [
            predictions["career_potential"],
            predictions["wealth_potential"],
            predictions["marriage_happiness"],
            predictions["children_prospects"],
            predictions["health_status"],
            predictions["spiritual_inclination"],
            predictions["chart_strength"],
            predictions["life_ease_score"]
        ]

        expected_average = sum(scores) / len(scores)
        actual_average = predictions["average_score"]

        # Allow small floating point difference
        assert abs(actual_average - expected_average) < 0.01


@pytest.mark.predict
@pytest.mark.unit
class TestMLPredictFromKundaliEndpoint:
    """Test the /ml/predict-from-kundali endpoint."""

    def test_predict_from_kundali_success(self, client, valid_birth_data):
        """Test successful Kundali generation and prediction."""
        response = client.post(
            "/ml/predict-from-kundali",
            json=valid_birth_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_predict_from_kundali_returns_predictions(self, client, valid_birth_data, expected_prediction_keys):
        """Test that endpoint returns all prediction fields."""
        response = client.post(
            "/ml/predict-from-kundali",
            json=valid_birth_data
        )

        data = response.json()
        predictions = data["data"]["predictions"]

        for key in expected_prediction_keys:
            assert key in predictions

    def test_predict_from_kundali_predictions_valid_range(self, client, valid_birth_data):
        """Test that returned predictions are in valid range."""
        response = client.post(
            "/ml/predict-from-kundali",
            json=valid_birth_data
        )

        data = response.json()
        predictions = data["data"]["predictions"]

        score_fields = [
            "career_potential",
            "wealth_potential",
            "marriage_happiness",
            "children_prospects",
            "health_status",
            "spiritual_inclination",
            "chart_strength",
            "life_ease_score",
            "average_score"
        ]

        for field in score_fields:
            value = predictions[field]
            assert 0 <= value <= 100, f"{field} out of range: {value}"

    def test_predict_from_kundali_invalid_timezone(self, client, invalid_birth_data_bad_timezone):
        """Test that invalid timezone is rejected."""
        response = client.post(
            "/ml/predict-from-kundali",
            json=invalid_birth_data_bad_timezone
        )

        # Should fail during Kundali generation
        assert response.status_code in [400, 500]

    def test_predict_from_kundali_invalid_date(self, client, invalid_birth_data_bad_date):
        """Test that invalid date format is rejected."""
        response = client.post(
            "/ml/predict-from-kundali",
            json=invalid_birth_data_bad_date
        )

        assert response.status_code in [400, 422, 500]

    def test_predict_from_kundali_out_of_range_latitude(self, client, invalid_birth_data_out_of_range):
        """Test that out-of-range latitude is rejected."""
        response = client.post(
            "/ml/predict-from-kundali",
            json=invalid_birth_data_out_of_range
        )

        assert response.status_code in [400, 422]

    def test_predict_from_kundali_alternative_timezone(self, client, alternative_birth_data):
        """Test prediction with alternative timezone."""
        response = client.post(
            "/ml/predict-from-kundali",
            json=alternative_birth_data
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_predict_from_kundali_missing_field(self, client, invalid_birth_data_missing_field):
        """Test that missing required field is rejected."""
        response = client.post(
            "/ml/predict-from-kundali",
            json=invalid_birth_data_missing_field
        )

        assert response.status_code == 422


@pytest.mark.predict
@pytest.mark.unit
class TestMLTestScenariosEndpoint:
    """Test the /ml/test-scenarios endpoint."""

    def test_test_scenarios_success(self, client):
        """Test that test scenarios endpoint works."""
        response = client.get("/ml/test-scenarios")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_test_scenarios_has_all_scenarios(self, client):
        """Test that all 3 scenarios are returned."""
        response = client.get("/ml/test-scenarios")
        data = response.json()

        scenarios = data["data"]
        assert "strong_chart" in scenarios
        assert "weak_chart" in scenarios
        assert "average_chart" in scenarios

    def test_test_scenarios_strong_chart_higher_than_weak(self, client):
        """Test that strong chart predictions are higher than weak chart."""
        response = client.get("/ml/test-scenarios")
        data = response.json()

        strong = data["data"]["strong_chart"]["predictions"]
        weak = data["data"]["weak_chart"]["predictions"]

        # Most predictions should be higher in strong chart
        assert strong["career_potential"] > weak["career_potential"]
        assert strong["wealth_potential"] > weak["wealth_potential"]
        assert strong["chart_strength"] > weak["chart_strength"]

    def test_test_scenarios_all_predictions_valid(self, client):
        """Test that all scenario predictions are in valid range."""
        response = client.get("/ml/test-scenarios")
        data = response.json()

        scenarios = data["data"]
        for scenario_name, scenario_data in scenarios.items():
            predictions = scenario_data["predictions"]
            for pred_name, pred_value in predictions.items():
                assert 0 <= pred_value <= 100, f"{scenario_name}: {pred_name} out of range"

    def test_test_scenarios_response_time(self, client):
        """Test that test scenarios responds quickly."""
        import time

        start_time = time.time()
        response = client.get("/ml/test-scenarios")
        elapsed_time = (time.time() - start_time) * 1000

        assert response.status_code == 200
        # Should respond in less than 1 second
        assert elapsed_time < 1000, f"Test scenarios took {elapsed_time}ms"


@pytest.mark.predict
@pytest.mark.unit
class TestMLModelInfoEndpoint:
    """Test the /ml/model-info endpoint."""

    def test_model_info_success(self, client):
        """Test that model info endpoint works."""
        response = client.get("/ml/model-info")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_model_info_has_required_fields(self, client):
        """Test that model info has required fields."""
        response = client.get("/ml/model-info")
        data = response.json()
        info = data["data"]

        assert "models_loaded" in info
        assert "available_models" in info
        assert "input_features" in info
        assert "output_targets" in info
        assert "target_names" in info

    def test_model_info_correct_feature_count(self, client):
        """Test that model info shows correct feature count."""
        response = client.get("/ml/model-info")
        data = response.json()
        info = data["data"]

        assert info["input_features"] == 53

    def test_model_info_correct_target_count(self, client):
        """Test that model info shows correct target count."""
        response = client.get("/ml/model-info")
        data = response.json()
        info = data["data"]

        assert info["output_targets"] == 8

    def test_model_info_target_names_correct(self, client, expected_prediction_keys):
        """Test that target names match expected predictions."""
        response = client.get("/ml/model-info")
        data = response.json()
        info = data["data"]

        target_names = info["target_names"]
        # Remove 'interpretation' and 'average_score' as they're not model targets
        expected_targets = [k for k in expected_prediction_keys if k not in ("interpretation", "average_score")]

        assert len(target_names) == len(expected_targets)
        for target in expected_targets:
            assert target in target_names

    def test_model_info_models_are_loaded(self, client):
        """Test that models are loaded."""
        response = client.get("/ml/model-info")
        data = response.json()
        info = data["data"]

        assert info["models_loaded"] is True
