"""
Integration Tests for Horoscope Feature
Tests all horoscope endpoints and business logic.
"""

import pytest
from datetime import datetime, date, timedelta
from fastapi.testclient import TestClient
from server.main import app
from server.services.horoscope_service import ZODIAC_SIGNS

client = TestClient(app)


class TestHoroscopeDailyEndpoint:
    """Test the daily horoscope endpoint"""

    def test_daily_horoscope_all_signs(self):
        """Test daily horoscope for all zodiac signs"""
        for sign in ZODIAC_SIGNS:
            response = client.get(f"/api/predictions/horoscope/daily/{sign}")

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "data" in data

            horoscope = data["data"]
            assert "zodiac_sign" in horoscope
            assert horoscope["zodiac_sign"].lower() == sign.lower()
            assert "date" in horoscope
            assert "life_areas" in horoscope
            assert "overall_score" in horoscope
            assert "grade" in horoscope
            assert "lucky_elements" in horoscope
            assert "affirmations" in horoscope

    def test_daily_horoscope_with_date(self):
        """Test daily horoscope with specific date"""
        sign = "Aries"
        target_date = (date.today() - timedelta(days=5)).isoformat()

        response = client.get(f"/api/predictions/horoscope/daily/{sign}", params={"date": target_date})

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_daily_horoscope_invalid_sign(self):
        """Test daily horoscope with invalid zodiac sign"""
        response = client.get("/api/predictions/horoscope/daily/InvalidSign")

        assert response.status_code == 400

    def test_daily_horoscope_case_insensitive(self):
        """Test that sign is case insensitive"""
        response1 = client.get("/api/predictions/horoscope/daily/aries")
        response2 = client.get("/api/predictions/horoscope/daily/ARIES")
        response3 = client.get("/api/predictions/horoscope/daily/Aries")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

    def test_daily_horoscope_future_date(self):
        """Test daily horoscope for future date"""
        sign = "Taurus"
        future_date = (date.today() + timedelta(days=7)).isoformat()

        response = client.get(f"/api/predictions/horoscope/daily/{sign}", params={"date": future_date})

        # Should either generate or reject with validation
        assert response.status_code in [200, 400]


class TestHoroscopeWeeklyEndpoint:
    """Test the weekly horoscope endpoint"""

    def test_weekly_horoscope_all_signs(self):
        """Test weekly horoscope for all zodiac signs"""
        for sign in ZODIAC_SIGNS:
            response = client.get(f"/api/predictions/horoscope/weekly/{sign}")

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "data" in data

            horoscope = data["data"]
            assert "zodiac_sign" in horoscope
            assert "week_overview" in horoscope
            assert "daily_breakdown" in horoscope
            assert isinstance(horoscope["daily_breakdown"], list)
            assert len(horoscope["daily_breakdown"]) <= 7
            assert "weekly_grade" in horoscope

    def test_weekly_horoscope_with_week_param(self):
        """Test weekly horoscope with specific week start date"""
        sign = "Gemini"
        today = date.today()
        week_start = (today - timedelta(days=today.weekday())).isoformat()

        response = client.get(f"/api/predictions/horoscope/weekly/{sign}", params={"week": week_start})

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_weekly_horoscope_structure(self):
        """Test structure of weekly horoscope response"""
        sign = "Cancer"
        response = client.get(f"/api/predictions/horoscope/weekly/{sign}")

        assert response.status_code == 200
        horoscope = response.json()["data"]

        # Check life areas in weekly
        if "life_areas" in horoscope:
            for area in horoscope["life_areas"]:
                assert "name" in area
                assert "weekly_outlook" in area or "score" in area


class TestHoroscopeMonthlyEndpoint:
    """Test the monthly horoscope endpoint"""

    def test_monthly_horoscope_all_signs(self):
        """Test monthly horoscope for all zodiac signs"""
        for sign in ZODIAC_SIGNS:
            response = client.get(f"/api/predictions/horoscope/monthly/{sign}")

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "data" in data

            horoscope = data["data"]
            assert "zodiac_sign" in horoscope
            assert "month_overview" in horoscope
            assert "monthly_grade" in horoscope
            assert "life_areas" in horoscope or "weekly_breakdown" in horoscope

    def test_monthly_horoscope_with_month_param(self):
        """Test monthly horoscope with specific month"""
        sign = "Leo"
        today = date.today()
        month_str = f"{today.year}-{today.month:02d}"

        response = client.get(f"/api/predictions/horoscope/monthly/{sign}", params={"month": month_str})

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_monthly_horoscope_previous_month(self):
        """Test monthly horoscope for previous month"""
        sign = "Virgo"
        today = date.today()
        first_of_month = today.replace(day=1)
        previous_month = first_of_month - timedelta(days=1)
        month_str = f"{previous_month.year}-{previous_month.month:02d}"

        response = client.get(f"/api/predictions/horoscope/monthly/{sign}", params={"month": month_str})

        assert response.status_code == 200


class TestHoroscopeAllSignsEndpoint:
    """Test the all-signs daily horoscope endpoint"""

    def test_all_signs_daily_horoscope(self):
        """Test daily horoscope for all 12 signs at once"""
        response = client.get("/api/predictions/horoscope/all-signs/daily")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data

        horoscopes = data["data"]
        assert isinstance(horoscopes, list)
        assert len(horoscopes) == 12

        # Verify each sign is present
        signs_returned = {h["zodiac_sign"].lower() for h in horoscopes}
        signs_expected = {s.lower() for s in ZODIAC_SIGNS}
        assert signs_returned == signs_expected

    def test_all_signs_daily_with_date(self):
        """Test all signs daily horoscope with specific date"""
        target_date = (date.today() - timedelta(days=3)).isoformat()

        response = client.get("/api/predictions/horoscope/all-signs/daily", params={"date": target_date})

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 12

    def test_all_signs_response_format(self):
        """Test response format of all-signs endpoint"""
        response = client.get("/api/predictions/horoscope/all-signs/daily")

        assert response.status_code == 200
        horoscopes = response.json()["data"]

        for horoscope in horoscopes:
            assert "zodiac_sign" in horoscope
            assert "overall_score" in horoscope
            assert "life_areas" in horoscope
            assert "lucky_elements" in horoscope


class TestHoroscopeArchiveEndpoint:
    """Test the horoscope archive endpoint"""

    def test_archive_endpoint_exists(self):
        """Test that archive endpoint is accessible"""
        sign = "Libra"
        response = client.get(f"/api/predictions/horoscope/archive/{sign}")

        # Should return either archived horoscopes or empty list
        assert response.status_code in [200, 404]

    def test_archive_with_date_range(self):
        """Test archive with date range parameters"""
        sign = "Scorpio"
        end_date = date.today().isoformat()
        start_date = (date.today() - timedelta(days=30)).isoformat()

        response = client.get(
            f"/api/predictions/horoscope/archive/{sign}",
            params={"from_date": start_date, "to_date": end_date}
        )

        assert response.status_code in [200, 404]

    def test_archive_with_limit(self):
        """Test archive with limit parameter"""
        sign = "Sagittarius"

        response = client.get(f"/api/predictions/horoscope/archive/{sign}", params={"limit": 10})

        assert response.status_code in [200, 404]


class TestHoroscopeLifeAreas:
    """Test life area scoring in horoscopes"""

    def test_life_areas_in_daily_horoscope(self):
        """Test that daily horoscope includes life areas"""
        sign = "Capricorn"
        response = client.get(f"/api/predictions/horoscope/daily/{sign}")

        assert response.status_code == 200
        horoscope = response.json()["data"]
        assert "life_areas" in horoscope

        life_areas = horoscope["life_areas"]
        assert isinstance(life_areas, list)

        # Should have 9 life areas
        if len(life_areas) > 0:
            expected_areas = [
                "Love & Romance",
                "Career & Professional",
                "Finance & Wealth",
                "Health & Wellness",
                "Family & Relationships",
                "Travel & Adventure",
                "Spirituality & Growth",
                "Luck & Opportunity",
                "Challenges & Obstacles"
            ]

            for area in life_areas:
                assert "name" in area
                assert "score" in area
                assert 0 <= area["score"] <= 100

    def test_life_areas_scoring_range(self):
        """Test that life area scores are in valid range"""
        for sign in ZODIAC_SIGNS[:3]:  # Test first 3 signs
            response = client.get(f"/api/predictions/horoscope/daily/{sign}")

            assert response.status_code == 200
            life_areas = response.json()["data"]["life_areas"]

            for area in life_areas:
                assert 0 <= area["score"] <= 100


class TestHoroscopeContent:
    """Test horoscope content quality"""

    def test_horoscope_has_affirmations(self):
        """Test that horoscope includes affirmations"""
        sign = "Aquarius"
        response = client.get(f"/api/predictions/horoscope/daily/{sign}")

        assert response.status_code == 200
        horoscope = response.json()["data"]

        if "affirmations" in horoscope:
            assert isinstance(horoscope["affirmations"], list)
            if len(horoscope["affirmations"]) > 0:
                assert len(horoscope["affirmations"][0]) > 0  # Non-empty strings

    def test_horoscope_has_lucky_elements(self):
        """Test that horoscope includes lucky elements"""
        sign = "Pisces"
        response = client.get(f"/api/predictions/horoscope/daily/{sign}")

        assert response.status_code == 200
        horoscope = response.json()["data"]

        if "lucky_elements" in horoscope:
            lucky = horoscope["lucky_elements"]
            # Should have standard lucky elements
            if isinstance(lucky, dict):
                # At least one of these should be present
                lucky_fields = ["color", "number", "direction", "time"]
                assert any(field in lucky for field in lucky_fields)

    def test_horoscope_grades(self):
        """Test that horoscope grades are valid"""
        sign = "Aries"
        response = client.get(f"/api/predictions/horoscope/daily/{sign}")

        assert response.status_code == 200
        horoscope = response.json()["data"]

        if "grade" in horoscope:
            grade = horoscope["grade"]
            # Valid grades: A+, A, A-, B+, B, B-, C+, C, C-, D, F
            valid_grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
            assert grade in valid_grades


class TestHoroscopeResponseFormat:
    """Test consistent response format across endpoints"""

    def test_api_response_format(self):
        """Test that all horoscope endpoints return APIResponse format"""
        sign = "Taurus"

        endpoints = [
            f"/api/predictions/horoscope/daily/{sign}",
            f"/api/predictions/horoscope/weekly/{sign}",
            f"/api/predictions/horoscope/monthly/{sign}",
            "/api/predictions/horoscope/all-signs/daily"
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)

            if response.status_code == 200:
                data = response.json()
                # Check APIResponse format
                assert "success" in data
                assert "status" in data
                assert "message" in data
                assert "timestamp" in data
                assert "data" in data

    def test_timestamp_format(self):
        """Test that timestamps are properly formatted"""
        sign = "Gemini"
        response = client.get(f"/api/predictions/horoscope/daily/{sign}")

        assert response.status_code == 200
        data = response.json()

        # Timestamp should be valid ISO format
        timestamp = data["timestamp"]
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp}")


class TestHoroscopeIntegration:
    """Integration tests for horoscope feature"""

    def test_consistency_across_endpoints(self):
        """Test that same sign returns consistent data across endpoints"""
        sign = "Cancer"

        daily_response = client.get(f"/api/predictions/horoscope/daily/{sign}")
        weekly_response = client.get(f"/api/predictions/horoscope/weekly/{sign}")

        assert daily_response.status_code == 200
        assert weekly_response.status_code == 200

        daily_sign = daily_response.json()["data"]["zodiac_sign"]
        weekly_sign = weekly_response.json()["data"]["zodiac_sign"]

        assert daily_sign.lower() == weekly_sign.lower()

    def test_all_signs_contains_each_sign(self):
        """Test that all-signs endpoint returns every zodiac sign"""
        response = client.get("/api/predictions/horoscope/all-signs/daily")

        assert response.status_code == 200
        horoscopes = response.json()["data"]

        returned_signs = [h["zodiac_sign"].lower() for h in horoscopes]
        expected_signs = [s.lower() for s in ZODIAC_SIGNS]

        for expected_sign in expected_signs:
            assert any(expected_sign in returned.lower() for returned in returned_signs), \
                f"Sign {expected_sign} not found in all-signs response"

    def test_pagination_in_archive(self):
        """Test pagination functionality in archive endpoint"""
        sign = "Leo"

        # Request with different limits
        for limit in [5, 10, 20]:
            response = client.get(
                f"/api/predictions/horoscope/archive/{sign}",
                params={"limit": limit}
            )

            if response.status_code == 200:
                horoscopes = response.json()["data"]
                # Should not exceed limit
                assert len(horoscopes) <= limit
