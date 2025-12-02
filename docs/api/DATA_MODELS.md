# Kundali API - Data Models & Schemas

## Table of Contents
1. [Authentication Models](#authentication-models)
2. [Kundali Models](#kundali-models)
3. [Prediction Models](#prediction-models)
4. [Transit Models](#transit-models)
5. [Enum Types](#enum-types)
6. [Relationships](#relationships)

---

## Authentication Models

### UserRegisterRequest

Registration request for new users.

```json
{
  "email": "user@example.com",
  "username": "johnsmith",
  "password": "secure_password_123",
  "full_name": "John Smith"
}
```

**Fields:**
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| email | string | Yes | Valid email, unique | User's email address |
| username | string | Yes | 3-50 chars, unique | Username for login |
| password | string | Yes | Min 8 characters | Account password |
| full_name | string | No | Max 255 chars | User's full name |

---

### UserLoginRequest

Login request for authentication.

```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Registered email address |
| password | string | Yes | Account password |

---

### UserResponse

User profile data returned by API.

```json
{
  "id": "690f866a1a9023ffe1b1c096",
  "email": "user@example.com",
  "username": "johnsmith",
  "full_name": "John Smith",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-15T10:32:00Z"
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string | MongoDB ObjectId |
| email | string | User's email |
| username | string | Username |
| full_name | string | Full name |
| is_active | boolean | Account status |
| is_verified | boolean | Email verification status |
| created_at | datetime | Account creation timestamp |
| last_login | datetime | Last login timestamp |

---

### TokenResponse

Authentication tokens returned after login/register.

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| access_token | string | JWT for API requests (15 min expiry) |
| refresh_token | string | JWT for refreshing access token (7 day expiry) |
| token_type | string | Always "bearer" |
| expires_in | integer | Access token expiry in seconds (900 = 15 min) |

---

### TokenRefreshRequest

Request to refresh expired access token.

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| refresh_token | string | Yes | Valid refresh token |

---

## Kundali Models

### KundaliRequest

Birth details for kundali generation.

```json
{
  "birthDate": "2000-01-15",
  "birthTime": "10:30",
  "latitude": 28.7041,
  "longitude": 77.1025,
  "timezone": "Asia/Kolkata"
}
```

**Fields:**
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| birthDate | string | Yes | Format: YYYY-MM-DD | Birth date |
| birthTime | string | Yes | Format: HH:MM | Birth time (24-hour) |
| latitude | float | Yes | -90 to 90 | Birth location latitude |
| longitude | float | Yes | -180 to 180 | Birth location longitude |
| timezone | string | Yes | Valid IANA timezone | Birth timezone |

**Example Timezones:**
- "UTC"
- "Asia/Kolkata" (India)
- "America/New_York"
- "Europe/London"
- "Australia/Sydney"

---

### KundaliSaveRequest

Request to save a generated kundali.

```json
{
  "name": "My Birth Chart",
  "birth_date": "2000-01-15",
  "birth_time": "10:30:00",
  "latitude": 28.7041,
  "longitude": 77.1025,
  "timezone": "Asia/Kolkata",
  "kundali_data": {...},
  "ml_features": {...}
}
```

**Fields:**
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| name | string | Yes | 1-255 chars | User-friendly name |
| birth_date | string | Yes | Format: YYYY-MM-DD | Birth date |
| birth_time | string | Yes | Format: HH:MM:SS | Birth time |
| latitude | float | Yes | -90 to 90 | Birth latitude |
| longitude | float | Yes | -180 to 180 | Birth longitude |
| timezone | string | Yes | Valid timezone | Birth timezone |
| kundali_data | object | Yes | Full kundali object | Complete analysis data |
| ml_features | object | No | 53 features | Extracted ML features |

---

### KundaliUpdateRequest

Request to update an existing kundali.

```json
{
  "name": "My Updated Chart",
  "ml_features": {"career": 0.85, "wealth": 0.72}
}
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | No | New kundali name |
| ml_features | object | No | Updated ML features |

---

### Ascendant

Ascendant (Lagna) details.

```json
{
  "index": 1,
  "longitude": 25.5,
  "sign": "Aries",
  "nakshatra": "Ashwini",
  "pada": 1
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| index | integer | Rasi index (0-11) |
| longitude | float | Ecliptic longitude (0-360) |
| sign | string | Zodiac sign name |
| nakshatra | string | Lunar mansion name |
| pada | integer | Quarter within nakshatra (1-4) |

---

### PlanetDetails

Planetary position details.

```json
{
  "longitude": 281.23,
  "sign": "Capricorn",
  "nakshatra": "Uttarashada",
  "pada": 2,
  "house": 10
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| longitude | float | Ecliptic longitude (0-360) |
| sign | string | Zodiac sign |
| nakshatra | string | Lunar mansion |
| pada | integer | Pada within nakshatra (1-4) |
| house | integer | House placement (1-12) |

**Planet Names:**
- Sun
- Moon
- Mars
- Mercury
- Jupiter
- Venus
- Saturn
- Rahu (North Node)
- Ketu (South Node)

---

### HouseDetails

House information.

```json
{
  "sign": 0,
  "planets": ["Sun", "Mercury"]
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| sign | integer | Sign in the house (0-11) |
| planets | array | Planets in this house |

---

### DashaInfo

Dasha (life period) system information.

```json
{
  "moon_nakshatra": "Ashwini",
  "moon_nakshatra_number": 1,
  "current_maha_dasha": "Jupiter",
  "maha_dasha_start_date": "2020-01-15",
  "maha_dasha_end_date": "2036-01-15",
  "maha_dasha_duration_years": 16,
  "remaining_maha_dasha_years": 12.5,
  "remaining_maha_dasha_months": 6.0,
  "completed_maha_dasha_years": 3.5,
  "current_antar_dasha": "Mercury",
  "current_antar_dasha_duration_days": 45,
  "maha_dasha_timeline": [...],
  "antar_dasha_timeline": [...],
  "next_dasha_lord": "Saturn",
  "dasha_interpretations": [...],
  "dasha_predictions": [...],
  "dasha_remedies": [...]
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| moon_nakshatra | string | Natal moon's nakshatra |
| moon_nakshatra_number | integer | Nakshatra number (1-27) |
| current_maha_dasha | string | Current major period planet |
| maha_dasha_start_date | string | Period start date |
| maha_dasha_end_date | string | Period end date |
| maha_dasha_duration_years | integer | Total period duration |
| remaining_maha_dasha_years | float | Years remaining |
| remaining_maha_dasha_months | float | Months remaining |
| completed_maha_dasha_years | float | Years completed |
| current_antar_dasha | string | Current sub-period planet |
| current_antar_dasha_duration_days | integer | Sub-period duration |
| maha_dasha_timeline | array | All major periods |
| antar_dasha_timeline | array | Sub-periods |
| next_dasha_lord | string | Next period's planet |
| dasha_interpretations | array | Text interpretations |
| dasha_predictions | array | Future predictions |
| dasha_remedies | array | Recommended remedies |

**Dasha Duration (Years):**
- Sun: 6
- Moon: 10
- Mars: 7
- Mercury: 17
- Jupiter: 16
- Venus: 20
- Saturn: 19
- Rahu: 18
- Ketu: 7

---

### YogaInfo

Yogas (auspicious combinations) information.

```json
{
  "total_yoga_count": 5,
  "benefic_yoga_count": 3,
  "malefic_yoga_count": 2,
  "neutral_yoga_count": 0,
  "yogas": [
    {
      "yoga_name": "Gaja Kesari Yoga",
      "house": 1,
      "planets": ["Jupiter", "Moon"],
      "strength": 85.5,
      "benefic": true
    }
  ]
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| total_yoga_count | integer | Total yogas present |
| benefic_yoga_count | integer | Auspicious yogas |
| malefic_yoga_count | integer | Challenging yogas |
| neutral_yoga_count | integer | Neutral yogas |
| yogas | array | Detailed yoga list |

---

### YogaAnalysis

Individual yoga details.

```json
{
  "yoga_name": "Gaja Kesari Yoga",
  "house": 1,
  "planets": ["Jupiter", "Moon"],
  "strength": 85.5,
  "benefic": true
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| yoga_name | string | Yoga name |
| house | integer | House where yoga forms |
| planets | array | Involved planets |
| strength | float | Yoga strength (0-100) |
| benefic | boolean | Is yoga beneficial |

---

### PlanetaryStrength

Planetary strength assessment.

```json
{
  "planet": "Jupiter",
  "total_strength": 45.5,
  "strength_percentage": 75.8,
  "strength_status": "Strong",
  "breakdown": {
    "sthana_bala": 12.0,
    "dig_bala": 10.5,
    "kala_bala": 9.5,
    "chesta_bala": 8.0,
    "naisargika_bala": 4.0,
    "drishti_bala": 1.5
  },
  "is_strong": true,
  "capacity": "Can give excellent results"
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| planet | string | Planet name |
| total_strength | float | Total strength (0-60) |
| strength_percentage | float | As percentage (0-100) |
| strength_status | string | Status label |
| breakdown | object | Component strengths |
| is_strong | boolean | Is planet strong (>70%) |
| capacity | string | Result capacity description |

**Strength Components (Shad Bala):**
- **Sthana Bala:** Positional strength (0-15)
- **Dig Bala:** Directional strength (0-15)
- **Kala Bala:** Temporal strength (0-15)
- **Chesta Bala:** Motion strength (0-15)
- **Naisargika Bala:** Natural strength (0-15)
- **Drishti Bala:** Aspect strength (0-15)

---

### HouseLordStrength

House lord strength details.

```json
{
  "house": 1,
  "lord": "Mars",
  "strength_percentage": 78.5,
  "status": "Strong"
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| house | integer | House number (1-12) |
| lord | string | House ruling planet |
| strength_percentage | float | Lord's strength (0-100) |
| status | string | Strong/Moderate/Weak |

---

### KundaliResponse

Complete kundali data returned by API.

```json
{
  "id": "690f866a1a9023ffe1b1c096",
  "user_id": "690f866a1a9023ffe1b1c096",
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
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string | MongoDB ObjectId |
| user_id | string | Owner user ID |
| name | string | Kundali name |
| birth_date | string | Birth date |
| birth_time | string | Birth time |
| latitude | float | Birth latitude |
| longitude | float | Birth longitude |
| timezone | string | Birth timezone |
| kundali_data | object | Full analysis |
| ml_features | object | 53 ML features |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

---

### KundaliListResponse

Kundali summary for listing.

```json
{
  "id": "690f866a1a9023ffe1b1c096",
  "name": "My Birth Chart",
  "birth_date": "2000-01-15",
  "created_at": "2024-01-15T10:30:00"
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string | Kundali ID |
| name | string | Kundali name |
| birth_date | string | Birth date |
| created_at | datetime | Creation timestamp |

---

## Prediction Models

### PredictionCreateRequest

Request to create a prediction.

```json
{
  "kundali_id": "690f866a1a9023ffe1b1c096",
  "career_potential": 0.85,
  "wealth_potential": 0.72,
  "marriage_happiness": 0.88,
  "children_prospects": 0.92,
  "health_status": 0.78,
  "spiritual_inclination": 0.81,
  "chart_strength": 0.79,
  "life_ease_score": 0.82,
  "interpretation": "Strong chart with good prospects",
  "model_version": "1.0.0",
  "model_type": "xgboost",
  "raw_output": null
}
```

**Fields:**
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| kundali_id | string | Yes | Valid ObjectId | Associated kundali |
| career_potential | float | Yes | 0-100 | Career score |
| wealth_potential | float | Yes | 0-100 | Wealth score |
| marriage_happiness | float | Yes | 0-100 | Marriage score |
| children_prospects | float | Yes | 0-100 | Children score |
| health_status | float | Yes | 0-100 | Health score |
| spiritual_inclination | float | Yes | 0-100 | Spiritual score |
| chart_strength | float | Yes | 0-100 | Chart strength score |
| life_ease_score | float | Yes | 0-100 | Life ease score |
| interpretation | string | No | Max 1000 chars | Text interpretation |
| model_version | string | No | Default: "1.0.0" | ML model version |
| model_type | string | No | Default: "xgboost" | ML model type |
| raw_output | object | No | Any | Raw model data |

---

### PredictionUpdateRequest

Request to update a prediction.

```json
{
  "interpretation": "Updated interpretation",
  "model_version": "1.1.0",
  "model_type": "gradient_boosting"
}
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| interpretation | string | No | Updated interpretation |
| model_version | string | No | Updated model version |
| model_type | string | No | Updated model type |

---

### PredictionResponse

Complete prediction data from API.

```json
{
  "id": "690f866a1a9023ffe1b1c098",
  "kundali_id": "690f866a1a9023ffe1b1c096",
  "user_id": "690f866a1a9023ffe1b1c096",
  "career_potential": 0.85,
  "wealth_potential": 0.72,
  "marriage_happiness": 0.88,
  "children_prospects": 0.92,
  "health_status": 0.78,
  "spiritual_inclination": 0.81,
  "chart_strength": 0.79,
  "life_ease_score": 0.82,
  "average_score": 0.823,
  "interpretation": "Strong chart with good prospects",
  "model_version": "1.0.0",
  "model_type": "xgboost",
  "raw_output": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string | Prediction ID |
| kundali_id | string | Associated kundali |
| user_id | string | Owner user ID |
| career_potential | float | Career score (0-100) |
| wealth_potential | float | Wealth score (0-100) |
| marriage_happiness | float | Marriage score (0-100) |
| children_prospects | float | Children score (0-100) |
| health_status | float | Health score (0-100) |
| spiritual_inclination | float | Spiritual score (0-100) |
| chart_strength | float | Chart strength (0-100) |
| life_ease_score | float | Life ease score (0-100) |
| average_score | float | Average of all scores |
| interpretation | string | Text interpretation |
| model_version | string | ML model version |
| model_type | string | ML model type |
| raw_output | object | Raw model output |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

---

### PredictionListResponse

Prediction summary for listing.

```json
{
  "id": "690f866a1a9023ffe1b1c098",
  "kundali_id": "690f866a1a9023ffe1b1c096",
  "average_score": 0.823,
  "created_at": "2024-01-15T10:30:00"
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | string | Prediction ID |
| kundali_id | string | Associated kundali |
| average_score | float | Average of all scores |
| created_at | datetime | Creation timestamp |

---

## Transit Models

### TransitRequest

Request for transit calculation.

```json
{
  "birthDate": "2000-01-15",
  "birthTime": "10:30",
  "latitude": 28.7041,
  "longitude": 77.1025,
  "timezone": "Asia/Kolkata",
  "date": "2024-01-15"
}
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| birthDate | string | Yes | Birth date (YYYY-MM-DD) |
| birthTime | string | Yes | Birth time (HH:MM) |
| latitude | float | Yes | Birth latitude |
| longitude | float | Yes | Birth longitude |
| timezone | string | Yes | Birth timezone |
| date | string | No | Transit date (defaults to today) |

---

### TransitInfo

Transit information for a planet.

```json
{
  "current_sign": "Capricorn",
  "current_degree": 25.5,
  "house": 10,
  "interpretations": ["Sun in 10th brings career focus"],
  "remedies": ["Chant Aditya Hridayam daily"]
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| current_sign | string | Current zodiac sign |
| current_degree | float | Ecliptic longitude (0-360) |
| house | integer | House placement (1-12) |
| interpretations | array | Text interpretations |
| remedies | array | Suggested remedies |

---

## Enum Types

### Zodiac Signs

```
Aries, Taurus, Gemini, Cancer, Leo, Virgo,
Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces
```

---

### Nakshatras (27 Lunar Mansions)

```
Ashwini, Bharani, Krittika, Rohini, Mrigashira, Ardra,
Punarvasu, Pushya, Aslesha, Magha, Purva Phalguni, Uttara Phalguni,
Hasta, Chitra, Swati, Vishakha, Anuradha, Jyeshtha,
Mula, Purva Ashadha, Uttara Ashadha, Sravana, Dhanishtha, Shatabhisha,
Purva Bhadrapada, Uttara Bhadrapada, Revati
```

---

### Planets

```
Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
```

---

### Strength Status

```
Very Strong, Strong, Moderate, Weak, Very Weak
```

---

### House Lord Status

```
Strong, Moderate, Weak
```

---

## Relationships

### Entity Relationships

```
User
├── n: Kundali
│   ├── 1: User (owner)
│   └── n: Prediction
│       ├── 1: User (owner)
│       └── 1: Kundali
└── 1: UserSettings
    └── 1: User
```

### Data Flow Diagram

```
Birth Details
    ↓
[Kundali Generation]
    ↓
KundaliRequest → Kundali Data
    ↓
[Feature Extraction]
    ↓
ML Features (53)
    ↓
[ML Prediction]
    ↓
Prediction Scores (8 metrics)
    ↓
[Save Operations]
    ↓
MongoDB Storage
    ↓
[Retrieve Operations]
    ↓
API Response
```

---

### Sample Complete Flow

**1. User Registration**
```json
POST /auth/register
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "secure123",
  "full_name": "John Doe"
}
→ UserResponse + TokenResponse
```

**2. Kundali Generation**
```json
POST /kundali/generate_kundali
{
  "birthDate": "2000-01-15",
  "birthTime": "10:30",
  "latitude": 28.7041,
  "longitude": 77.1025,
  "timezone": "Asia/Kolkata"
}
→ KundaliResponse (with planets, houses, dasha, yogas, ml_features)
```

**3. Kundali Save**
```json
POST /kundali/save
{
  "name": "My Birth Chart",
  "birth_date": "2000-01-15",
  "birth_time": "10:30:00",
  "latitude": 28.7041,
  "longitude": 77.1025,
  "timezone": "Asia/Kolkata",
  "kundali_data": {...},
  "ml_features": {...}
}
→ KundaliResponse with id, user_id, timestamps
```

**4. Prediction Creation**
```json
POST /predictions/
{
  "kundali_id": "690f866a1a9023ffe1b1c096",
  "career_potential": 0.85,
  "wealth_potential": 0.72,
  ...
  "interpretation": "Strong chart"
}
→ PredictionResponse with id, all scores, timestamps
```

**5. Data Retrieval**
```
GET /kundali/list
→ Array of KundaliListResponse

GET /kundali/{id}
→ KundaliResponse

GET /predictions/list
→ Array of PredictionListResponse

GET /predictions/{id}
→ PredictionResponse
```

---

## Validation Rules

### Birth Date & Time
- Date: Must be valid past date (YYYY-MM-DD)
- Time: Valid 24-hour time (HH:MM)
- Together: Must be reasonable (not in future, recent death not possible)

### Coordinates
- Latitude: -90 to 90
- Longitude: -180 to 180
- Must correspond to real locations

### Scores
- Range: 0 to 100
- Type: Float with precision up to 2 decimals
- Consistency: Average = sum of scores / 8

### String Fields
- Trimmed of whitespace
- No SQL injection risk (Pydantic validated)
- Max lengths enforced

### Email
- Valid RFC 5322 format
- Unique across system
- Case-insensitive comparison

### Username
- 3-50 characters
- Alphanumeric + underscore
- Unique across system
- Case-insensitive comparison

---

## Database Constraints

### MongoDB Indexes

**Essential Indexes:**
```javascript
// Users
db.users.createIndex({"email": 1}, {unique: true})
db.users.createIndex({"username": 1}, {unique: true})

// Kundalis
db.kundalis.createIndex({"user_id": 1})
db.kundalis.createIndex({"created_at": -1})

// Predictions
db.predictions.createIndex({"user_id": 1})
db.predictions.createIndex({"kundali_id": 1})
db.predictions.createIndex({"created_at": -1})
```

### Unique Constraints
- User.email (globally unique)
- User.username (globally unique)

### Foreign Keys (Application Level)
- Kundali.user_id → User._id
- Prediction.user_id → User._id
- Prediction.kundali_id → Kundali._id

