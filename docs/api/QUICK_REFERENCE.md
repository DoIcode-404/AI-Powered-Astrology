# Kundali API - Quick Reference Guide

## API Base URL
```
Development: http://localhost:8000
Production: https://api.example.com
```

---

## Quick Start

### 1. Health Check
```bash
curl -X GET http://localhost:8000/health
```

### 2. Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "user123",
    "password": "Pass1234!",
    "full_name": "John Doe"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Pass1234!"
  }'
```

### 4. Generate Kundali
```bash
curl -X POST http://localhost:8000/kundali/generate_kundali \
  -H "Content-Type: application/json" \
  -d '{
    "birthDate": "2000-01-15",
    "birthTime": "10:30",
    "latitude": 28.7041,
    "longitude": 77.1025,
    "timezone": "Asia/Kolkata"
  }'
```

### 5. Save Kundali (Authenticated)
```bash
curl -X POST http://localhost:8000/kundali/save \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "My Birth Chart",
    "birth_date": "2000-01-15",
    "birth_time": "10:30:00",
    "latitude": 28.7041,
    "longitude": 77.1025,
    "timezone": "Asia/Kolkata",
    "kundali_data": {...},
    "ml_features": {...}
  }'
```

---

## Endpoint Cheat Sheet

### Authentication
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/auth/register` | No | Register new user |
| POST | `/auth/login` | No | Login user |
| POST | `/auth/refresh` | No | Refresh access token |
| GET | `/auth/me` | Yes | Get current user |

### Kundali
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/kundali/generate_kundali` | No | Generate kundali |
| POST | `/kundali/save` | Yes | Save kundali |
| GET | `/kundali/list` | Yes | List kundalis |
| GET | `/kundali/{id}` | Yes | Get kundali |
| PUT | `/kundali/{id}` | Yes | Update kundali |
| DELETE | `/kundali/{id}` | Yes | Delete kundali |

### Predictions
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/predictions/` | Yes | Create prediction |
| GET | `/predictions/list` | Yes | List predictions |
| GET | `/predictions/{id}` | Yes | Get prediction |
| PUT | `/predictions/{id}` | Yes | Update prediction |
| DELETE | `/predictions/{id}` | Yes | Delete prediction |

### ML Predictions
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/ml/predict` | No | Predict from features |
| POST | `/ml/predict-from-kundali` | No | Predict from birth details |
| POST | `/ml/predict-batch` | No | Batch predict |
| GET | `/ml/test-scenarios` | No | Test model |
| GET | `/ml/model-info` | No | Model info |
| GET | `/ml/health` | No | ML health |

### Transits
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/transits/calculate` | No | Calculate transits |
| POST | `/transits/upcoming` | No | Upcoming transits |
| POST | `/transits/dasha-transit-analysis` | No | Dasha-transit analysis |

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Auth required |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Invalid parameters |
| 500 | Server Error - Internal error |
| 503 | Service Unavailable - Maintenance/models not loaded |

---

## Response Format

### Success Response
```json
{
  "status": "success",
  "success": true,
  "data": {...},
  "message": "Operation successful",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### Error Response
```json
{
  "status": "error",
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  },
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

---

## Common Parameters

### Pagination
```
?limit=100&offset=0
```

### Authentication
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Common Request Bodies

### Birth Details
```json
{
  "birthDate": "2000-01-15",
  "birthTime": "10:30",
  "latitude": 28.7041,
  "longitude": 77.1025,
  "timezone": "Asia/Kolkata"
}
```

### Prediction Scores
```json
{
  "career_potential": 0.85,
  "wealth_potential": 0.72,
  "marriage_happiness": 0.88,
  "children_prospects": 0.92,
  "health_status": 0.78,
  "spiritual_inclination": 0.81,
  "chart_strength": 0.79,
  "life_ease_score": 0.82
}
```

---

## Token Management

### Get Tokens from Login
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "expires_in": 900
}
```

### Refresh Expired Token
```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
```

### Token Format
```
Authorization: Bearer {access_token}
```

---

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| INVALID_CREDENTIALS | Wrong email/password | Check credentials |
| EMAIL_ALREADY_EXISTS | Email registered | Use different email |
| USERNAME_ALREADY_EXISTS | Username taken | Choose different username |
| KUNDALI_NOT_FOUND | Kundali doesn't exist | Check ID |
| PREDICTION_NOT_FOUND | Prediction doesn't exist | Check ID |
| UNAUTHORIZED | Token invalid/expired | Refresh token |
| VALIDATION_ERROR | Invalid input | Check parameters |
| MODELS_NOT_LOADED | ML models unavailable | Wait and retry |

---

## Common Data Types

### Coordinates
```
Latitude: -90 to 90
Longitude: -180 to 180
```

### Scores
```
Range: 0 to 100
Type: Float (e.g., 0.85 = 85%)
```

### Dates/Times
```
Date: YYYY-MM-DD (e.g., 2000-01-15)
Time: HH:MM (24-hour, e.g., 10:30)
Datetime: ISO 8601 (e.g., 2024-01-15T10:30:00Z)
```

### Timezones
```
UTC, Asia/Kolkata, America/New_York, Europe/London, etc.
```

---

## Kundali Zodiac Signs

```
Aries (0°-30°)
Taurus (30°-60°)
Gemini (60°-90°)
Cancer (90°-120°)
Leo (120°-150°)
Virgo (150°-180°)
Libra (180°-210°)
Scorpio (210°-240°)
Sagittarius (240°-270°)
Capricorn (270°-300°)
Aquarius (300°-330°)
Pisces (330°-360°)
```

---

## ML Prediction Metrics

1. **Career Potential** - Professional success likelihood
2. **Wealth Potential** - Financial success likelihood
3. **Marriage Happiness** - Relationship satisfaction
4. **Children Prospects** - Family expansion potential
5. **Health Status** - Overall health quality
6. **Spiritual Inclination** - Spiritual development capacity
7. **Chart Strength** - Overall birth chart strength
8. **Life Ease Score** - Overall life ease and comfort

---

## Dasha Planets & Duration

| Planet | Years |
|--------|-------|
| Sun | 6 |
| Moon | 10 |
| Mars | 7 |
| Mercury | 17 |
| Jupiter | 16 |
| Venus | 20 |
| Saturn | 19 |
| Rahu | 18 |
| Ketu | 7 |

**Total Cycle:** 120 years

---

## 27 Nakshatras

1. Ashwini
2. Bharani
3. Krittika
4. Rohini
5. Mrigashira
6. Ardra
7. Punarvasu
8. Pushya
9. Aslesha
10. Magha
11. Purva Phalguni
12. Uttara Phalguni
13. Hasta
14. Chitra
15. Swati
16. Vishakha
17. Anuradha
18. Jyeshtha
19. Mula
20. Purva Ashadha
21. Uttara Ashadha
22. Sravana
23. Dhanishtha
24. Shatabhisha
25. Purva Bhadrapada
26. Uttara Bhadrapada
27. Revati

---

## 12 Houses & Their Significations

| House | Signification |
|-------|----------------|
| 1 | Self, personality, appearance |
| 2 | Wealth, family, speech |
| 3 | Siblings, communication, short trips |
| 4 | Home, mother, property, comfort |
| 5 | Children, creativity, love affairs |
| 6 | Enemies, health, debts, servants |
| 7 | Marriage, partner, contracts |
| 8 | Death, longevity, inheritance, occult |
| 9 | Father, luck, higher learning, travel |
| 10 | Career, reputation, authority |
| 11 | Gains, friendship, aspirations |
| 12 | Loss, expenditure, spirituality, foreign lands |

---

## Recommended Pagination Sizes

```
User lists: 20-50 items per page
Kundali lists: 10-20 items per page
Prediction lists: 10-15 items per page
Batch operations: 50-100 items per batch
```

---

## Timeout Recommendations

```
Kundali generation: 30 seconds
ML predictions: 20 seconds
Transit calculations: 25 seconds
Login/Register: 10 seconds
Database operations: 5 seconds
```

---

## Caching Strategy

```
Kundali generation: 6 hours
Predictions: 24 hours
Transits: 1 hour
User profile: 30 minutes
Model info: 1 week
```

---

## Rate Limiting (Recommended)

```
Public endpoints: 60 req/min
Authenticated: 300 req/min
ML predictions: 100 req/min
Batch operations: 10 req/min
```

---

## Environment Variables

```
MONGODB_URI=mongodb+srv://...
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## Useful cURL Examples

### Get with Auth
```bash
curl -X GET http://localhost:8000/kundali/list \
  -H "Authorization: Bearer $TOKEN"
```

### POST with Data
```bash
curl -X POST http://localhost:8000/predictions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d @- << 'EOF'
{
  "kundali_id": "690f866a1a9023ffe1b1c096",
  "career_potential": 0.85,
  "wealth_potential": 0.72,
  "marriage_happiness": 0.88,
  "children_prospects": 0.92,
  "health_status": 0.78,
  "spiritual_inclination": 0.81,
  "chart_strength": 0.79,
  "life_ease_score": 0.82
}
EOF
```

### PUT with Update
```bash
curl -X PUT http://localhost:8000/kundali/{kundali_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Updated Chart"}'
```

### DELETE
```bash
curl -X DELETE http://localhost:8000/kundali/{kundali_id} \
  -H "Authorization: Bearer $TOKEN"
```

---

## Useful JavaScript Fetch Examples

### Fetch with Auth
```javascript
const response = await fetch('http://localhost:8000/kundali/list', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
  }
});
const data = await response.json();
```

### POST Request
```javascript
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const data = await response.json();
```

---

## Useful Dart/Flutter Examples

### Kundali Generation
```dart
Future<Map> generateKundali(String birthDate, String birthTime,
    double latitude, double longitude, String timezone) async {
  final response = await http.post(
    Uri.parse('$baseUrl/kundali/generate_kundali'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'birthDate': birthDate,
      'birthTime': birthTime,
      'latitude': latitude,
      'longitude': longitude,
      'timezone': timezone,
    }),
  );
  return jsonDecode(response.body)['data'];
}
```

### Authenticated Request
```dart
Future<Map> getKundaliList(String token) async {
  final response = await http.get(
    Uri.parse('$baseUrl/kundali/list?limit=10&offset=0'),
    headers: {'Authorization': 'Bearer $token'},
  );
  return jsonDecode(response.body)['data'];
}
```

---

## Troubleshooting

### Common Issues

**401 Unauthorized**
- Token expired → Use refresh_token
- Token invalid → Re-login
- Wrong format → Use "Bearer {token}"

**422 Validation Error**
- Check all required fields present
- Verify field types and formats
- Check value constraints (ranges, lengths)

**503 Service Unavailable**
- ML models loading → Wait a few seconds
- Server maintenance → Try again later

**504 Gateway Timeout**
- Request taking too long → Increase timeout
- Server overloaded → Implement retry logic

---

## Best Practices

1. **Always validate input** before sending to API
2. **Store tokens securely** (secure storage in mobile apps)
3. **Implement retry logic** with exponential backoff
4. **Cache responses** appropriately based on data freshness
5. **Use pagination** for list endpoints
6. **Handle errors gracefully** with user-friendly messages
7. **Log important events** for debugging
8. **Monitor API usage** to avoid rate limits
9. **Update documentation** when API changes
10. **Test thoroughly** before deployment

---

## Support & Documentation

- Full API docs: `/docs/api/API_DOCUMENTATION.md`
- Data models: `/docs/api/DATA_MODELS.md`
- Endpoints summary: `/docs/api/ENDPOINTS_SUMMARY.md`
- This guide: `/docs/api/QUICK_REFERENCE.md`

