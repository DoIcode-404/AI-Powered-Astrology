"""
Pytest configuration and fixtures for Kundali API tests.
"""

import pytest
from fastapi.testclient import TestClient
from server.main import app


@pytest.fixture(scope="session")
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.fixture
def valid_birth_data():
    """Fixture with valid birth data for testing."""
    return {
        "birthDate": "1990-05-15",
        "birthTime": "14:30",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }


@pytest.fixture
def alternative_birth_data():
    """Fixture with alternative valid birth data."""
    return {
        "birthDate": "1985-12-25",
        "birthTime": "09:15",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timezone": "America/New_York"
    }


@pytest.fixture
def valid_53_features():
    """Fixture with 53 valid ML features for testing."""
    return [
        1990, 5, 15, 14, 30, 28.6139, 77.209, 2448026.875, 151.90787719222817, 6,
        20, 2, 0.5530323428276631, 0, 0, 30.553032342827663, 2, 9, 0.5530323428276631, 0,
        271.8969694575721, 10, 5, 1.8969694575720837, 0, 324.518463186251, 11, 6,
        24.518463186250983, 0, 14.30554416815847, 1, 8, 14.30554416815847, 0,
        75.79556153856383, 3, 10, 15.795561538563831, 0, 348.95320076532744, 12, 7,
        18.953200765327438, 1, 271.5289649008921, 10, 5, 1.528964900892106, 1,
        287.62321930477333, 10, 5
    ]


@pytest.fixture
def invalid_birth_data_missing_field():
    """Fixture with missing required field."""
    return {
        "birthDate": "1990-05-15",
        "birthTime": "14:30",
        "latitude": 28.6139
        # Missing longitude and timezone
    }


@pytest.fixture
def invalid_birth_data_bad_timezone():
    """Fixture with invalid timezone format."""
    return {
        "birthDate": "1990-05-15",
        "birthTime": "14:30",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "UTC+5:30"  # Invalid IANA timezone
    }


@pytest.fixture
def invalid_birth_data_bad_date():
    """Fixture with invalid date format."""
    return {
        "birthDate": "15-05-1990",  # Wrong format
        "birthTime": "14:30",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }


@pytest.fixture
def invalid_birth_data_out_of_range():
    """Fixture with out-of-range coordinates."""
    return {
        "birthDate": "1990-05-15",
        "birthTime": "14:30",
        "latitude": 95.0,  # Out of range (-90 to 90)
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }


@pytest.fixture
def expected_prediction_keys():
    """Fixture with expected keys in prediction response."""
    return [
        "career_potential",
        "wealth_potential",
        "marriage_happiness",
        "children_prospects",
        "health_status",
        "spiritual_inclination",
        "chart_strength",
        "life_ease_score",
        "average_score",
        "interpretation"
    ]


@pytest.fixture
def expected_kundali_keys():
    """Fixture with expected keys in Kundali response."""
    return [
        "ascendant",
        "planets",
        "houses",
        "zodiac_sign",
        "ruling_planet",
        "dasha",
        "shad_bala",
        "divisional_charts",
        "ml_features",
        "training_data",
        "generated_at"
    ]
