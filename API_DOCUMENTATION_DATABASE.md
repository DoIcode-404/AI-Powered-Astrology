# Kundali API - Database CRUD Endpoints Documentation

## Overview

This document covers the database CRUD endpoints for Kundali charts and Predictions. All endpoints require authentication via JWT tokens.

---

## Authentication Endpoints

### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johnsmith",
  "password": "secure_password_123",
  "full_name": "John Smith"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "johnsmith",
      "full_name": "John Smith",
      "is_active": true,
      "is_verified": false,
      "created_at": "2024-01-15T10:30:00",
      "last_login": null
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIs...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
      "token_type": "bearer",
      "expires_in": 900
    }
  },
  "message": "User registered successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### POST /auth/login
Authenticate user and get JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "user": {...},
    "tokens": {...}
  },
  "message": "Login successful",
  "timestamp": "2024-01-15T10:30:00"
}
```

### POST /auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 900
  },
  "message": "Token refreshed successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /auth/me
Get authenticated user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "username": "johnsmith",
    "full_name": "John Smith",
    "is_active": true,
    "is_verified": false,
    "created_at": "2024-01-15T10:30:00",
    "last_login": "2024-01-15T11:00:00"
  },
  "message": "Profile retrieved successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## Kundali CRUD Endpoints

### POST /kundali/save
Save a generated Kundali chart.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "My Birth Chart",
  "birth_date": "2000-01-15",
  "birth_time": "10:30:00",
  "latitude": 28.7041,
  "longitude": 77.1025,
  "timezone": "Asia/Kolkata",
  "kundali_data": {
    "ascendant": {"sign": "Aries", "degree": 25.5},
    "planets": {...},
    "houses": {...}
  },
  "ml_features": {
    "career": 0.85,
    "wealth": 0.72
  }
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "id": 1,
    "user_id": 1,
    "name": "My Birth Chart",
    "birth_date": "2000-01-15",
    "birth_time": "10:30:00",
    "latitude": 28.7041,
    "longitude": 77.1025,
    "timezone": "Asia/Kolkata",
    "kundali_data": {...},
    "ml_features": {...},
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  },
  "message": "Kundali saved successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /kundali/list
Get user's saved Kundalis with pagination.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `limit` (integer, optional, default=100): Maximum number of results
- `offset` (integer, optional, default=0): Number of results to skip

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "kundalis": [
      {
        "id": 1,
        "name": "My Birth Chart",
        "birth_date": "2000-01-15",
        "created_at": "2024-01-15T10:30:00"
      }
    ],
    "total": 5,
    "limit": 100,
    "offset": 0
  },
  "message": "Kundali list retrieved successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /kundali/{kundali_id}
Get details of a specific Kundali.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "id": 1,
    "user_id": 1,
    "name": "My Birth Chart",
    "birth_date": "2000-01-15",
    "birth_time": "10:30:00",
    "latitude": 28.7041,
    "longitude": 77.1025,
    "timezone": "Asia/Kolkata",
    "kundali_data": {...},
    "ml_features": {...},
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  },
  "message": "Kundali retrieved successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### PUT /kundali/{kundali_id}
Update a Kundali's name and/or ML features.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "My Updated Chart",
  "ml_features": {
    "career": 0.90,
    "wealth": 0.75
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {...},
  "message": "Kundali updated successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### DELETE /kundali/{kundali_id}
Delete a saved Kundali.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "success": true,
    "message": "Kundali deleted successfully",
    "kundali_id": 1
  },
  "message": "Kundali deleted successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /kundali/history
Get user's saved Kundalis (deprecated, use /kundali/list instead).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": [...],
  "message": "Kundali history retrieved successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## Prediction CRUD Endpoints

### POST /predictions/
Create a new prediction for a Kundali.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "kundali_id": 1,
  "career_potential": 0.85,
  "wealth_potential": 0.72,
  "marriage_happiness": 0.88,
  "children_prospects": 0.92,
  "health_status": 0.78,
  "spiritual_inclination": 0.81,
  "chart_strength": 0.79,
  "life_ease_score": 0.82,
  "interpretation": "Strong chart with good marriage and children prospects",
  "model_version": "1.0.0",
  "model_type": "xgboost"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "id": 1,
    "kundali_id": 1,
    "user_id": 1,
    "career_potential": 0.85,
    "wealth_potential": 0.72,
    "marriage_happiness": 0.88,
    "children_prospects": 0.92,
    "health_status": 0.78,
    "spiritual_inclination": 0.81,
    "chart_strength": 0.79,
    "life_ease_score": 0.82,
    "average_score": 0.823,
    "interpretation": "Strong chart with good marriage and children prospects",
    "model_version": "1.0.0",
    "model_type": "xgboost",
    "raw_output": null,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  },
  "message": "Prediction created successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /predictions/list
Get user's predictions with pagination.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `limit` (integer, optional, default=100): Maximum number of results
- `offset` (integer, optional, default=0): Number of results to skip

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "predictions": [
      {
        "id": 1,
        "kundali_id": 1,
        "average_score": 0.823,
        "created_at": "2024-01-15T10:30:00"
      }
    ],
    "total": 3,
    "limit": 100,
    "offset": 0
  },
  "message": "Predictions retrieved successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /predictions/{prediction_id}
Get details of a specific prediction.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "id": 1,
    "kundali_id": 1,
    "user_id": 1,
    "career_potential": 0.85,
    "wealth_potential": 0.72,
    "marriage_happiness": 0.88,
    "children_prospects": 0.92,
    "health_status": 0.78,
    "spiritual_inclination": 0.81,
    "chart_strength": 0.79,
    "life_ease_score": 0.82,
    "average_score": 0.823,
    "interpretation": "Strong chart with good marriage and children prospects",
    "model_version": "1.0.0",
    "model_type": "xgboost",
    "raw_output": null,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  },
  "message": "Prediction retrieved successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /predictions/kundali/{kundali_id}
Get all predictions for a specific Kundali.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": [
    {
      "id": 1,
      "kundali_id": 1,
      "average_score": 0.823,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "message": "Predictions retrieved successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### PUT /predictions/{prediction_id}
Update a prediction's metadata.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "interpretation": "Updated interpretation",
  "model_version": "1.1.0",
  "model_type": "gradient_boosting"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {...},
  "message": "Prediction updated successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

### DELETE /predictions/{prediction_id}
Delete a prediction.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "success": true,
    "message": "Prediction deleted successfully",
    "prediction_id": 1
  },
  "message": "Prediction deleted successfully",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## Error Responses

All error responses follow this format:

**Response (4xx/5xx):**
```json
{
  "success": false,
  "status": "ERROR",
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### Common Error Codes
- `VALIDATION_ERROR` (400): Invalid request data
- `UNAUTHORIZED` (401): Missing or invalid authentication
- `NOT_FOUND` (404): Resource not found
- `EMAIL_ALREADY_EXISTS` (400): Email already registered
- `USERNAME_ALREADY_EXISTS` (400): Username already taken
- `INVALID_CREDENTIALS` (401): Wrong email or password
- `KUNDALI_NOT_FOUND` (404): Kundali not found
- `PREDICTION_NOT_FOUND` (404): Prediction not found
- `INTERNAL_SERVER_ERROR` (500): Server error

---

## Best Practices

1. **Always include the `Authorization` header** with the Bearer token from login/register
2. **Access tokens expire in 15 minutes** - use refresh endpoint to get new one
3. **Use pagination** for list endpoints to avoid large responses
4. **Validate data** before sending requests
5. **Handle error responses** gracefully in your client application
6. **Never expose tokens** in logs or client-side code

---

## Database Schema

### Users Table
- `id` (int, PK)
- `email` (varchar, unique)
- `username` (varchar, unique)
- `hashed_password` (varchar)
- `full_name` (varchar)
- `is_active` (bool)
- `is_verified` (bool)
- `created_at` (datetime)
- `updated_at` (datetime)
- `last_login` (datetime)

### Kundalis Table
- `id` (int, PK)
- `user_id` (int, FK → users.id)
- `name` (varchar)
- `birth_date` (varchar)
- `birth_time` (varchar)
- `latitude` (varchar)
- `longitude` (varchar)
- `timezone` (varchar)
- `kundali_data` (json)
- `ml_features` (json)
- `created_at` (datetime)
- `updated_at` (datetime)

### Predictions Table
- `id` (int, PK)
- `kundali_id` (int, FK → kundalis.id)
- `user_id` (int, FK → users.id)
- `career_potential` (float)
- `wealth_potential` (float)
- `marriage_happiness` (float)
- `children_prospects` (float)
- `health_status` (float)
- `spiritual_inclination` (float)
- `chart_strength` (float)
- `life_ease_score` (float)
- `average_score` (float)
- `interpretation` (varchar)
- `model_version` (varchar)
- `model_type` (varchar)
- `raw_output` (json)
- `created_at` (datetime)
- `updated_at` (datetime)

### UserSettings Table
- `user_id` (int, PK/FK → users.id)
- `theme` (varchar)
- `language` (varchar)
- `notifications_enabled` (bool)
- `notification_preferences` (json)
- `default_timezone` (varchar)
