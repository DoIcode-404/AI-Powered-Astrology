# Kundali Astrology API - Complete Reference

**Version:** 1.0
**Last Updated:** 2025-11-08
**Status:** ✅ Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [API Endpoints](#api-endpoints)
3. [Response Format](#response-format)
4. [Error Handling](#error-handling)
5. [Implementation Details](#implementation-details)
6. [Code Examples](#code-examples)
7. [Best Practices](#best-practices)

---

## Overview

The Kundali Astrology API provides endpoints for generating personalized birth charts (Kundali) and making AI-powered predictions about 8 life dimensions using machine learning. The API combines Vedic astrology calculations with XGBoost ML models to deliver predictions based on 53 astrological features.

**API Base URL:** `http://localhost:8001`
**API Version:** 1.0

### Key Features
- ✅ Standardized response format across all endpoints
- ✅ Comprehensive error handling and validation
- ✅ Request tracking with unique IDs
- ✅ Performance metrics tracking
- ✅ CORS support for mobile apps
- ✅ Health checks and monitoring
- ✅ Detailed logging throughout

---

## API Endpoints

### Health Check

#### GET /health
Check if the API is running and healthy.

**Request:**
```bash
curl http://localhost:8001/health
```

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2025-11-08T06:40:20.123456",
    "ephemeris": "initialized",
    "database": "connected"
  },
  "error": null,
  "message": "Service is running normally"
}
```

---

### Authentication Endpoints

#### POST /auth/signup
Register a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | User's full name |
| email | string | Yes | Valid email address |
| password | string | Yes | Password (min 8 chars) |

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "user_id": "123",
    "email": "john@example.com",
    "name": "John Doe",
    "token": "eyJhbGc..."
  },
  "message": "User registered successfully"
}
```

---

#### POST /auth/login
User login.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "user_id": "123",
    "email": "john@example.com",
    "token": "eyJhbGc..."
  },
  "message": "Login successful"
}
```

---

#### GET /auth/profile
Get current user profile.

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "user_id": "123",
    "email": "john@example.com",
    "name": "John Doe"
  },
  "message": "Profile retrieved successfully"
}
```

---

#### POST /auth/logout
Logout user.

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": null,
  "message": "Logout successful"
}
```

---

### Kundali Endpoints

#### POST /kundali/generate_kundali
Generate a complete birth chart (Kundali) with astrological calculations and ML-extracted features.

**Request Body:**
```json
{
  "birthDate": "1990-05-15",
  "birthTime": "14:30",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": "Asia/Kolkata"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| birthDate | string | Yes | Birth date in YYYY-MM-DD format |
| birthTime | string | Yes | Birth time in HH:MM format (24-hour) |
| latitude | float | Yes | Birth location latitude (-90 to 90) |
| longitude | float | Yes | Birth location longitude (-180 to 180) |
| timezone | string | Yes | IANA timezone (e.g., "Asia/Kolkata", "America/New_York") |

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "ascendant": {
      "index": 6,
      "longitude": 151.90787719222817,
      "sign": "Virgo",
      "nakshatra": "Uttara Phalguni",
      "pada": 2
    },
    "planets": {
      "Sun": {
        "longitude": 30.553032342827663,
        "sign": "Taurus",
        "nakshatra": "Krittika",
        "pada": 2,
        "house": 9
      }
    },
    "houses": {
      "1": {
        "sign": 6,
        "planets": []
      }
    },
    "zodiac_sign": "Capricorn",
    "ruling_planet": "Saturn",
    "dasha": {
      "moon_nakshatra": "Uttara Ashadha",
      "current_maha_dasha": "Jupiter",
      "maha_dasha_start_date": "1980-08-23",
      "maha_dasha_end_date": "1996-08-23",
      "maha_dasha_duration_years": 16,
      "remaining_maha_dasha_years": 9.72
    },
    "shad_bala": {
      "planetary_strengths": {},
      "house_lord_strengths": {},
      "yogas": {
        "total_yoga_count": 1,
        "benefic_yoga_count": 0,
        "malefic_yoga_count": 1
      },
      "aspect_strengths": {}
    },
    "divisional_charts": {
      "D1_Rasi": {},
      "D2_Hora": {},
      "D7_Saptamsha": {},
      "D9_Navamsha": {}
    },
    "ml_features": {},
    "training_data": {},
    "generated_at": "2025-11-08T06:40:20.123456"
  },
  "message": "Kundali generated successfully"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8001/kundali/generate_kundali \
  -H "Content-Type: application/json" \
  -d '{
    "birthDate": "1990-05-15",
    "birthTime": "14:30",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
  }'
```

---

### ML Prediction Endpoints

#### POST /ml/predict
Make predictions using 53 pre-extracted astrological features.

**Request Body:**
```json
{
  "features": [1990, 5, 15, 14, 30, 28.6139, 77.209, 2448026.875, 151.90787719222817, ...]
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| features | array[float] | Yes | Array of exactly 53 numeric features |

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "career_potential": 69.41,
    "wealth_potential": 66.55,
    "marriage_happiness": 66.34,
    "children_prospects": 74.14,
    "health_status": 93.90,
    "spiritual_inclination": 76.97,
    "chart_strength": 56.45,
    "life_ease_score": 44.66,
    "average_score": 68.55,
    "interpretation": "This chart indicates average potential with some strengths to leverage and some areas to work on."
  },
  "message": "Prediction completed successfully"
}
```

---

#### POST /ml/predict-from-kundali
Generate Kundali, extract features, and make predictions in one request.

**Request Body:**
```json
{
  "birthDate": "1990-05-15",
  "birthTime": "14:30",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": "Asia/Kolkata"
}
```

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "career_potential": 75.53,
    "wealth_potential": 75.35,
    "marriage_happiness": 78.02,
    "children_prospects": 79.07,
    "health_status": 86.58,
    "spiritual_inclination": 64.95,
    "chart_strength": 25.62,
    "life_ease_score": 55.57,
    "average_score": 67.59,
    "interpretation": "This chart indicates average potential with some strengths to leverage and some areas to work on."
  },
  "message": "Kundali generated and predictions completed successfully"
}
```

**Performance:** ~150-200ms average response time

---

#### GET /ml/test-scenarios
Test the ML model on 3 predefined scenarios.

**Request:**
```bash
curl http://localhost:8001/ml/test-scenarios
```

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "strong_chart": {
      "name": "Strong Chart (Well-Aspected, Multiple Yogas)",
      "predictions": {
        "career_potential": 92.83,
        "wealth_potential": 94.21,
        "marriage_happiness": 87.83,
        "children_prospects": 92.43,
        "health_status": 85.27,
        "spiritual_inclination": 91.36,
        "chart_strength": 70.38,
        "life_ease_score": 84.58
      }
    },
    "weak_chart": { },
    "average_chart": { }
  },
  "message": "Test scenarios completed successfully"
}
```

---

#### GET /ml/model-info
Get information about the trained ML model.

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "models_loaded": true,
    "available_models": ["neural_network", "xgboost"],
    "input_features": 53,
    "output_targets": 8,
    "target_names": [
      "career_potential",
      "wealth_potential",
      "marriage_happiness",
      "children_prospects",
      "health_status",
      "spiritual_inclination",
      "chart_strength",
      "life_ease_score"
    ],
    "model_metrics": {
      "xgboost": {
        "r2_score": 0.75,
        "mae": 12.3,
        "rmse": 15.7
      }
    }
  },
  "message": "Model information retrieved successfully"
}
```

---

### Export Endpoints

#### POST /export/kundali-csv
Export a single Kundali as CSV.

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "format": "csv",
    "filename": "kundali_1990_05_15.csv"
  },
  "message": "Kundali exported successfully"
}
```

---

#### POST /export/kundali-json
Export a single Kundali as JSON.

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "format": "json",
    "filename": "kundali_1990_05_15.json"
  },
  "message": "Kundali exported successfully"
}
```

---

#### POST /export/batch-kundali-csv
Batch CSV export.

**Response:**
```json
{
  "status": "success",
  "success": true,
  "data": {
    "format": "csv",
    "filename": "batch_kundali_5_records.csv",
    "total_requested": 5,
    "successful": 5,
    "failed": 0,
    "time_ms": 2543.12
  },
  "message": "Batch export completed: 5/5 Kundalis exported"
}
```

---

## Response Format

### Standard Response Structure

All API responses follow a standardized format:

```json
{
  "status": "success|error|validation_error",
  "success": true|false,
  "data": {},
  "error": null,
  "timestamp": "2025-11-08T06:40:20.123456",
  "request_id": "unique-id",
  "message": "Response message"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| status | string | Response status: "success", "error", or "validation_error" |
| success | boolean | Whether the request was successful |
| data | object | Response payload (varies by endpoint) |
| error | object | Error details if request failed |
| timestamp | string | ISO 8601 timestamp of response |
| request_id | string | Unique request identifier for tracking |
| message | string | Human-readable response message |

---

## Error Handling

### Error Response Format

```json
{
  "status": "error",
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "error": "Technical error details"
    }
  },
  "timestamp": "2025-11-08T06:40:20.123456",
  "message": "Error message"
}
```

### Validation Error Response

```json
{
  "status": "validation_error",
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more validation errors occurred",
    "details": {
      "errors": [
        {"field": "birthDate", "message": "Invalid date format"},
        {"field": "latitude", "message": "Value must be between -90 and 90"}
      ]
    }
  },
  "timestamp": "2025-11-08T06:40:20.123456"
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| VALIDATION_ERROR | 422 | Invalid input parameters |
| INVALID_FEATURE_COUNT | 422 | Feature array is not exactly 53 elements |
| MODELS_NOT_LOADED | 503 | ML models failed to load |
| KUNDALI_PREDICTION_ERROR | 500 | Error generating Kundali |
| PREDICTION_ERROR | 500 | Error making ML prediction |
| TIMEZONE_ERROR | 400 | Invalid IANA timezone string |
| DATE_FORMAT_ERROR | 400 | Invalid date/time format |
| INVALID_EMAIL | 422 | Invalid email format |
| UNAUTHORIZED | 401 | Authentication failed |

---

## Implementation Details

### Middleware Stack

The API uses the following middleware stack (execution order, bottom to top):

1. **RequestIdMiddleware** - Add unique request ID to each request
2. **ErrorHandlingMiddleware** - Catch and handle all exceptions
3. **LoggingMiddleware** - Log all API activity
4. **CORSMiddleware** - Handle CORS headers

### CORS Configuration

```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    # Add your Flutter app URL here
]
```

### Request Tracking

Each request is assigned a unique UUID for tracking and debugging:
- Included in response headers
- Included in response body
- Used for error correlation
- Logged with all activity

### Performance Metrics

All endpoints include performance tracking:
- Request timestamp
- Response timestamp
- Calculation time (milliseconds)
- Request ID for correlation
- Batch operation metrics

Example:
```json
{
  "calculation_time_ms": 145.32,
  "timestamp": "2025-11-07T10:30:00Z",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Security Features

✅ **Request Validation**
- Pydantic schema validation
- Email validation (EmailStr)
- Coordinate range checking
- Type checking throughout

✅ **Error Messages**
- User-friendly messages
- No sensitive data in errors
- Detailed logging (not exposed to client)

✅ **CORS Configuration**
- Whitelist specific origins
- Allow credentials
- Wildcard headers/methods

---

## Code Examples

### Python Example

```python
import requests
import json

API_BASE_URL = "http://localhost:8001"

# Example 1: Health Check
response = requests.get(f"{API_BASE_URL}/health")
print(response.json())

# Example 2: Generate Kundali
kundali_request = {
    "birthDate": "1990-05-15",
    "birthTime": "14:30",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
}

response = requests.post(
    f"{API_BASE_URL}/kundali/generate_kundali",
    json=kundali_request
)

kundali_data = response.json()
print(f"Kundali generated: {kundali_data['data']['zodiac_sign']}")

# Example 3: Make Prediction from Kundali
response = requests.post(
    f"{API_BASE_URL}/ml/predict-from-kundali",
    json=kundali_request
)

predictions = response.json()['data']
print(f"Career Potential: {predictions['career_potential']:.2f}%")
print(f"Average Score: {predictions['average_score']:.2f}%")
```

### Dart/Flutter Example

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

const String API_BASE_URL = "http://localhost:8001";

Future<void> generateKundali() async {
  final kundaliRequest = {
    "birthDate": "1990-05-15",
    "birthTime": "14:30",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
  };

  try {
    final response = await http.post(
      Uri.parse("$API_BASE_URL/kundali/generate_kundali"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(kundaliRequest),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      if (data['success']) {
        print("Zodiac Sign: ${data['data']['zodiac_sign']}");
      }
    }
  } catch (e) {
    print("Error: $e");
  }
}
```

### JavaScript Example

```javascript
const API_BASE_URL = "http://localhost:8001";

// Health check
fetch(`${API_BASE_URL}/health`)
  .then(res => res.json())
  .then(data => console.log("API Status:", data.data.status));

// Generate Kundali and predict
const kundaliRequest = {
  birthDate: "1990-05-15",
  birthTime: "14:30",
  latitude: 28.6139,
  longitude: 77.2090,
  timezone: "Asia/Kolkata"
};

fetch(`${API_BASE_URL}/ml/predict-from-kundali`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(kundaliRequest)
})
  .then(res => res.json())
  .then(data => {
    console.log("Predictions:", data.data);
    console.log("Interpretation:", data.data.interpretation);
  });
```

### BASH Example

```bash
#!/bin/bash

API_BASE_URL="http://localhost:8001"

# Health check
echo "Checking API health..."
curl -s $API_BASE_URL/health | jq .

# Generate Kundali with prediction
echo "Generating Kundali and predictions..."
curl -X POST $API_BASE_URL/ml/predict-from-kundali \
  -H "Content-Type: application/json" \
  -d '{
    "birthDate": "1990-05-15",
    "birthTime": "14:30",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata"
  }' | jq .data
```

---

## Best Practices

### 1. Error Handling
Always check the `success` field in response:

```python
response = requests.post(url, json=data)
if response.json()['success']:
    # Process data
else:
    # Handle error
    print(response.json()['error']['message'])
```

### 2. Timezone Validation
Use IANA timezone database format:
- ✅ Correct: "Asia/Kolkata", "America/New_York", "Europe/London"
- ❌ Incorrect: "UTC+5:30", "IST", "EST"

### 3. Date/Time Format
Always use ISO 8601 format:
- Date: YYYY-MM-DD (e.g., "1990-05-15")
- Time: HH:MM in 24-hour format (e.g., "14:30")

### 4. Coordinate Validation
- Latitude: -90 to 90 degrees
- Longitude: -180 to 180 degrees

### 5. Feature Array Length
When using `/ml/predict`, ensure feature array is exactly 53 elements:
```python
if len(features) != 53:
    raise ValueError(f"Expected 53 features, got {len(features)}")
```

### 6. Request Tracking
Use the `request_id` from responses for debugging and correlation:
```python
response = requests.post(url, json=data)
data = response.json()
request_id = data['request_id']
# Use request_id for logging/debugging
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. Future versions will include:
- Rate limiting: 1000 requests/hour per IP
- Burst allowance: 50 requests/minute
- Rate limit headers in response

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-08 | Initial release with Kundali, ML prediction, and export endpoints |

---

## Support

For issues, feature requests, or feedback:
- GitHub Issues: [Project Repository]
- Email: support@kundaliapi.com

---

**Last Updated:** 2025-11-08
**Status:** ✅ Production Ready
