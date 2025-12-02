# Kundali API - Quick Endpoints Summary

## Complete API Endpoint Inventory

**Total Endpoints: 28**
**Protected Endpoints: 18 (require JWT token)**
**Public Endpoints: 10 (no authentication)**

---

## Endpoints by Module

### Health & System (3 endpoints)

| Method | Path | Auth | Status | Purpose |
|--------|------|------|--------|---------|
| GET | `/` | No | 200 | API welcome & info |
| GET | `/health` | No | 200 | Health check |
| GET | `/error-stats` | No | 200 | Error tracking stats |

---

### Authentication (4 endpoints)

| Method | Path | Auth | Status | Purpose |
|--------|------|------|--------|---------|
| POST | `/auth/register` | No | 201 | Register new user |
| POST | `/auth/login` | No | 200 | Login & get tokens |
| POST | `/auth/refresh` | No | 200 | Refresh access token |
| GET | `/auth/me` | **Yes** | 200 | Get current user profile |

---

### Kundali Management (7 endpoints)

| Method | Path | Auth | Status | Purpose |
|--------|------|------|--------|---------|
| POST | `/kundali/generate_kundali` | No | 200 | Generate kundali |
| POST | `/kundali/save` | **Yes** | 201 | Save kundali to profile |
| GET | `/kundali/list` | **Yes** | 200 | List user's kundalis |
| GET | `/kundali/{kundali_id}` | **Yes** | 200 | Get specific kundali |
| PUT | `/kundali/{kundali_id}` | **Yes** | 200 | Update kundali |
| DELETE | `/kundali/{kundali_id}` | **Yes** | 200 | Delete kundali |
| GET | `/kundali/history` | **Yes** | 200 | [DEPRECATED] Use /list |

---

### Predictions (6 endpoints)

| Method | Path | Auth | Status | Purpose |
|--------|------|------|--------|---------|
| POST | `/predictions/` | **Yes** | 201 | Create prediction |
| GET | `/predictions/list` | **Yes** | 200 | List predictions |
| GET | `/predictions/{prediction_id}` | **Yes** | 200 | Get specific prediction |
| GET | `/predictions/kundali/{kundali_id}` | **Yes** | 200 | Get predictions for kundali |
| PUT | `/predictions/{prediction_id}` | **Yes** | 200 | Update prediction |
| DELETE | `/predictions/{prediction_id}` | **Yes** | 200 | Delete prediction |

---

### ML Predictions (5 endpoints)

| Method | Path | Auth | Status | Purpose |
|--------|------|------|--------|---------|
| POST | `/ml/predict` | No | 200 | Predict from 53 features |
| POST | `/ml/predict-from-kundali` | No | 200 | Predict from birth details |
| POST | `/ml/predict-batch` | No | 200 | Batch predictions |
| GET | `/ml/test-scenarios` | No | 200 | Test on 3 scenarios |
| GET | `/ml/model-info` | No | 200 | Model information |
| GET | `/ml/health` | No | 200 | ML models health check |

---

### Transit Calculations (3 endpoints)

| Method | Path | Auth | Status | Purpose |
|--------|------|------|--------|---------|
| POST | `/transits/calculate` | No | 200 | Calculate current transits |
| POST | `/transits/upcoming` | No | 200 | Get upcoming transits |
| POST | `/transits/dasha-transit-analysis` | No | 200 | Analyze dasha-transit interaction |

---

### Export (4 endpoints - Production Disabled)

| Method | Path | Auth | Status | Purpose |
|--------|------|------|--------|---------|
| POST | `/export/kundali-csv` | No | 503 | [DEV ONLY] Export as CSV |
| POST | `/export/kundali-json` | No | 503 | [DEV ONLY] Export as JSON |
| POST | `/export/batch-kundali-csv` | No | 503 | [DEV ONLY] Batch CSV export |
| POST | `/export/batch-kundali-json` | No | 503 | [DEV ONLY] Batch JSON export |

---

## Authentication Flow

```
1. User Registration (POST /auth/register)
   └─> Returns: access_token + refresh_token

2. User Login (POST /auth/login)
   └─> Returns: access_token + refresh_token

3. Access Protected Resources (with Authorization header)
   Headers: Authorization: Bearer <access_token>

4. Token Expiration (after 15 minutes)
   └─> Refresh Token (POST /auth/refresh)
       └─> Returns: new access_token + refresh_token
```

---

## Request/Response Format

### Standard Success Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "success": true,
  "data": {...},
  "error": null,
  "timestamp": "2024-01-15T10:30:00.123456",
  "message": "Operation successful"
}
```

### Standard Error Response
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "field": null,
    "details": null
  },
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

---

## Core Features by Endpoint Type

### Kundali Generation
- Complete astrological analysis
- Planetary positions & houses
- Dasha system (life periods)
- Yogas (auspicious combinations)
- Planetary strengths
- ML features extraction

### ML Predictions (8 metrics)
1. Career Potential
2. Wealth Potential
3. Marriage Happiness
4. Children Prospects
5. Health Status
6. Spiritual Inclination
7. Chart Strength
8. Life Ease Score

### Transit Analysis
- Current planetary transits
- Upcoming important transits (up to 10 years)
- Dasha-transit conjunction analysis
- Interpretations & remedies

### Data Management
- Save kundalis to user profile
- List saved kundalis with pagination
- Retrieve specific kundali details
- Update kundali metadata
- Delete kundalis
- Create predictions
- Update prediction metadata
- Delete predictions

---

## Key Statistics

### Feature Extraction (ML)
- **Input Features:** 53 astrological features
- **Output Targets:** 8 life outcome predictions
- **Models Available:** XGBoost (primary), Neural Network (optional)

### Dasha Timeline
- **Maha Dasha:** Major periods (2.4 to 20 years each)
- **Antar Dasha:** Sub-periods within Maha Dasha
- **Timeline:** Complete multi-year outlook

### Yogas Detected
- **Benefic Yogas:** Auspicious combinations
- **Malefic Yogas:** Challenging combinations
- **Neutral Yogas:** Balanced combinations

### Response Times (Benchmarks)
- Kundali Generation: 1-2 seconds
- ML Predictions: 200-500ms
- Transit Calculations: 500ms-2 seconds
- Database Operations: 100-300ms

---

## Error Handling

### Common HTTP Status Codes

| Code | Scenario | Examples |
|------|----------|----------|
| 200 | Success (GET, POST, PUT) | Data retrieved/created |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid input, validation error |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Account disabled |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Invalid parameters |
| 500 | Server Error | Internal error |
| 503 | Service Unavailable | Models not loaded, maintenance |

### Retry Strategy
- **Transient Errors (5xx):** Implement exponential backoff
- **Rate Limiting (429):** Wait and retry
- **Client Errors (4xx):** Don't retry (except validation)
- **Auth Failures:** Refresh token and retry once

---

## Authentication Details

### Token Types
- **Access Token:** Valid for 15 minutes, used for API requests
- **Refresh Token:** Valid for 7 days, used to get new access token

### Token Format
- Type: JWT (JSON Web Token)
- Algorithm: HS256
- Claims: user_id, email, username

### Authorization Header Format
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Database Schema Overview

### Collections (MongoDB)

**users**
- _id: ObjectId
- email: string (unique)
- username: string (unique)
- hashed_password: string
- full_name: string
- is_active: boolean
- is_verified: boolean
- created_at: datetime
- updated_at: datetime
- last_login: datetime

**kundalis**
- _id: ObjectId
- user_id: string
- name: string
- birth_date: string
- birth_time: string
- latitude: float
- longitude: float
- timezone: string
- kundali_data: object
- ml_features: object
- created_at: datetime
- updated_at: datetime

**predictions**
- _id: ObjectId
- user_id: string
- kundali_id: string
- career_potential: float (0-100)
- wealth_potential: float (0-100)
- marriage_happiness: float (0-100)
- children_prospects: float (0-100)
- health_status: float (0-100)
- spiritual_inclination: float (0-100)
- chart_strength: float (0-100)
- life_ease_score: float (0-100)
- average_score: float
- interpretation: string
- model_version: string
- model_type: string
- raw_output: object
- created_at: datetime
- updated_at: datetime

**user_settings**
- _id: ObjectId
- user_id: string
- theme: string
- language: string
- notifications_enabled: boolean
- notification_preferences: object
- default_timezone: string
- preferences: object
- updated_at: datetime

---

## Pagination

### Query Parameters
- **limit:** Max items per page (default: 100, max: 1000)
- **offset:** Number of items to skip (default: 0)

### Response Structure
```json
{
  "data": {
    "kundalis": [...],
    "total": 25,
    "limit": 10,
    "offset": 0
  }
}
```

---

## Recommended Integration Order

1. **Health Check** → `/health` (verify API is running)
2. **User Auth** → `/auth/register` or `/auth/login`
3. **Kundali Generation** → `/kundali/generate_kundali`
4. **Save Kundali** → `/kundali/save`
5. **Get Predictions** → `/ml/predict-from-kundali`
6. **Save Prediction** → `/predictions/`
7. **Retrieve Data** → `/kundali/list`, `/predictions/list`
8. **Calculate Transits** → `/transits/calculate`

---

## Development vs Production

### ML Features
- **Development:** All ML endpoints available with model testing
- **Production:** ML endpoints available, export disabled

### Export Features
- **Development:** CSV/JSON export available
- **Production:** Export returns 503 (use API data directly)

### Database
- **Development:** Local MongoDB or dev instance
- **Production:** Production MongoDB cluster with backups

---

## Performance Optimization Tips

### Caching
- Cache kundali results for 6 hours (same birth details)
- Cache predictions for 24 hours
- Cache transit data for 1 hour
- Clear cache when user data changes

### Pagination
- Use pagination for list endpoints (limit user data transfer)
- Implement local caching of list pages
- Consider infinite scroll with offset-based pagination

### Batch Operations
- Use `/ml/predict-batch` for multiple predictions
- Reduces API calls and improves throughput
- Max batch size recommended: 100 records

### Timeout Handling
- Set 30s timeout for kundali generation
- Set 20s timeout for ML predictions
- Set 25s timeout for transit calculations
- Implement retry with exponential backoff

---

## Security Considerations

### Token Management
- Store refresh token securely (httpOnly cookie or secure storage)
- Never log or expose tokens
- Rotate tokens regularly
- Validate token expiration client-side

### Input Validation
- Validate birth date/time before API call
- Validate latitude/longitude range (-90 to 90, -180 to 180)
- Sanitize string inputs
- Use HTTPS for all requests

### Data Protection
- Don't expose password hashes
- Validate user ownership before returning data
- Implement rate limiting
- Log sensitive operations

---

## Troubleshooting

### Common Issues

**Models not loaded (503)**
- Wait for server to start up
- Check if ML dependencies installed
- Check server logs for initialization errors

**Invalid token (401)**
- Token may have expired (refresh using refresh_token)
- Token may be malformed (verify format)
- Token may be from different environment

**Validation error (422)**
- Check request body format
- Verify all required fields present
- Validate field types and constraints

**Rate limiting (429)**
- Wait before retrying
- Implement exponential backoff
- Consider batch operations

---

## API Versioning

- **Current Version:** 1.0.0
- **Database Schema:** 1.0
- **ML Model:** 1.0.0

Breaking changes will increment major version.
Non-breaking additions increment minor version.
Bug fixes increment patch version.

---

## Contact & Support

For issues, feature requests, or clarifications:
- Check API documentation first
- Review error codes and messages
- Check server logs for detailed errors
- Implement proper error handling and retries
