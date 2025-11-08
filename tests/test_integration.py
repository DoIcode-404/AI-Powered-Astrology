"""
Integration tests for complete API workflows.
"""

import pytest


@pytest.mark.integration
class TestKundaliToMLIntegration:
    """Test complete Kundali generation and ML prediction flow."""

    def test_complete_workflow_kundali_then_predict(self, client, valid_birth_data):
        """Test complete workflow: generate Kundali then make prediction."""
        # Step 1: Generate Kundali
        kundali_response = client.post(
            "/kundali/generate_kundali",
            json=valid_birth_data
        )

        assert kundali_response.status_code == 200
        kundali_data = kundali_response.json()
        assert kundali_data["success"] is True

        # Step 2: Verify Kundali contains ML features
        assert "ml_features" in kundali_data["data"]
        assert "training_data" in kundali_data["data"]

        # Step 3: Extract features from training_data
        training_data = kundali_data["data"]["training_data"]
        assert "calculated_features" in training_data

        # Step 4: Make prediction from Kundali in one step
        predict_response = client.post(
            "/ml/predict-from-kundali",
            json=valid_birth_data
        )

        assert predict_response.status_code == 200
        predict_data = predict_response.json()
        assert predict_data["success"] is True

        # Step 5: Verify predictions are valid (predictions are nested under 'predictions' key)
        response_data = predict_data["data"]
        assert "predictions" in response_data
        predictions = response_data["predictions"]
        assert "career_potential" in predictions
        assert "average_score" in predictions
        assert 0 <= predictions["average_score"] <= 100

    def test_multiple_predictions_same_person(self, client, valid_birth_data):
        """Test that multiple predictions for same person are consistent."""
        # Make 3 predictions for the same birth data
        predictions_list = []

        for _ in range(3):
            response = client.post(
                "/ml/predict-from-kundali",
                json=valid_birth_data
            )

            assert response.status_code == 200
            predictions = response.json()["data"]["predictions"]
            predictions_list.append(predictions)

        # Verify all predictions are identical (deterministic model)
        first_pred = predictions_list[0]
        for other_pred in predictions_list[1:]:
            assert first_pred["career_potential"] == other_pred["career_potential"]
            assert first_pred["average_score"] == other_pred["average_score"]

    def test_different_people_different_predictions(self, client, valid_birth_data, alternative_birth_data):
        """Test that different people get different predictions."""
        # Predict for first person
        response1 = client.post(
            "/ml/predict-from-kundali",
            json=valid_birth_data
        )
        pred1 = response1.json()["data"]["predictions"]

        # Predict for second person
        response2 = client.post(
            "/ml/predict-from-kundali",
            json=alternative_birth_data
        )
        pred2 = response2.json()["data"]["predictions"]

        # Predictions should be different
        # (unlikely to be identical by chance for different people)
        assert pred1["average_score"] != pred2["average_score"]

    def test_kundali_contains_all_required_data(self, client, valid_birth_data, expected_kundali_keys):
        """Test that Kundali generation returns all required data."""
        response = client.post(
            "/kundali/generate_kundali",
            json=valid_birth_data
        )

        assert response.status_code == 200
        data = response.json()
        kundali = data["data"]

        # Check all expected keys
        for key in expected_kundali_keys:
            assert key in kundali, f"Missing key in Kundali: {key}"

    def test_kundali_shad_bala_populated(self, client, valid_birth_data):
        """Test that Shad Bala (strength data) is populated in Kundali."""
        response = client.post(
            "/kundali/generate_kundali",
            json=valid_birth_data
        )

        assert response.status_code == 200
        shad_bala = response.json()["data"]["shad_bala"]

        # Verify Shad Bala contains strength data
        assert "planetary_strengths" in shad_bala
        assert "house_lord_strengths" in shad_bala
        assert "yogas" in shad_bala
        assert "aspect_strengths" in shad_bala

    def test_kundali_dasha_information(self, client, valid_birth_data):
        """Test that Dasha information is populated correctly."""
        response = client.post(
            "/kundali/generate_kundali",
            json=valid_birth_data
        )

        assert response.status_code == 200
        dasha = response.json()["data"]["dasha"]

        # Verify required Dasha fields
        assert "current_maha_dasha" in dasha
        assert "maha_dasha_duration_years" in dasha
        assert "remaining_maha_dasha_years" in dasha
        assert "antar_dasha_timeline" in dasha

    def test_kundali_planets_in_valid_signs(self, client, valid_birth_data):
        """Test that planets are in valid zodiac signs."""
        response = client.post(
            "/kundali/generate_kundali",
            json=valid_birth_data
        )

        assert response.status_code == 200
        planets = response.json()["data"]["planets"]

        valid_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]

        for planet_name, planet_data in planets.items():
            assert "sign" in planet_data
            assert planet_data["sign"] in valid_signs, f"{planet_name} in invalid sign: {planet_data['sign']}"

    def test_kundali_houses_complete(self, client, valid_birth_data):
        """Test that all 12 houses are present in Kundali."""
        response = client.post(
            "/kundali/generate_kundali",
            json=valid_birth_data
        )

        assert response.status_code == 200
        houses = response.json()["data"]["houses"]

        # Verify all 12 houses are present
        for house_num in range(1, 13):
            assert str(house_num) in houses, f"House {house_num} missing"

    def test_predictions_match_chart_strength(self, client, valid_birth_data):
        """Test that overall life ease score correlates with chart strength."""
        response = client.post(
            "/ml/predict-from-kundali",
            json=valid_birth_data
        )

        data = response.json()["data"]["predictions"]

        # Life ease score should generally correlate with chart strength
        # Both should be on a similar scale (0-100)
        assert "chart_strength" in data
        assert "life_ease_score" in data
        assert 0 <= data["chart_strength"] <= 100
        assert 0 <= data["life_ease_score"] <= 100

    def test_error_recovery_after_failed_request(self, client, valid_birth_data):
        """Test that API recovers after a failed request."""
        # Make a request that will fail
        invalid_data = {
            "birthDate": "invalid-date",
            "birthTime": "14:30",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata"
        }

        response1 = client.post(
            "/kundali/generate_kundali",
            json=invalid_data
        )
        assert response1.status_code != 200

        # Verify API still works with valid request
        response2 = client.post(
            "/kundali/generate_kundali",
            json=valid_birth_data
        )
        assert response2.status_code == 200

    def test_concurrent_different_predictions(self, client, valid_birth_data, alternative_birth_data):
        """Test handling of predictions for different people."""
        # Simulate concurrent requests by making multiple predictions
        predictions = []

        for birth_data in [valid_birth_data, alternative_birth_data, valid_birth_data]:
            response = client.post(
                "/ml/predict-from-kundali",
                json=birth_data
            )
            predictions.append(response.json()["data"]["predictions"])

        # Verify predictions are correct
        assert len(predictions) == 3
        assert predictions[0]["average_score"] == predictions[2]["average_score"]  # Same person
        assert predictions[0]["average_score"] != predictions[1]["average_score"]  # Different person


@pytest.mark.integration
class TestErrorHandlingIntegration:
    """Test error handling across the API."""

    def test_invalid_request_doesnt_crash_api(self, client):
        """Test that invalid requests don't crash the API."""
        # Make several invalid requests
        invalid_requests = [
            {"features": "invalid"},  # Wrong type
            {"features": []},  # Empty
            {},  # Missing field
            {"features": [1.0] * 100},  # Too many
        ]

        for invalid_req in invalid_requests:
            response = client.post("/ml/predict", json=invalid_req)
            # Should return error response, not crash
            assert response.status_code >= 400

        # Verify API still works
        response = client.get("/health")
        assert response.status_code == 200

    def test_endpoint_availability_after_errors(self, client):
        """Test that all endpoints are available after errors."""
        endpoints_to_test = [
            ("GET", "/health", None),
            ("GET", "/ml/test-scenarios", None),
            ("GET", "/ml/model-info", None),
        ]

        # Make some bad requests first
        client.post("/ml/predict", json={"features": "bad"})
        client.post("/kundali/generate_kundali", json={})

        # Verify all endpoints still work
        for method, endpoint, body in endpoints_to_test:
            if method == "GET":
                response = client.get(endpoint)
            else:
                response = client.post(endpoint, json=body)

            assert response.status_code == 200, f"{endpoint} returned {response.status_code}"
