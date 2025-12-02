# Kundali Astrology API - Complete Documentation Package

This directory contains comprehensive API documentation for the Kundali Astrology backend service.

## Documentation Files

### 1. **API_DOCUMENTATION.md** (Primary Reference)
**Size:** ~3500 lines | **Purpose:** Complete API specification

The authoritative source for all API endpoints with:
- Complete endpoint specifications with examples
- Request/response schemas
- Error codes and handling
- Authentication & security guidelines
- Performance recommendations
- Database considerations
- Deployment checklist

**Use this when:**
- You need complete details on a specific endpoint
- Implementing API clients (mobile, web, etc.)
- Setting up error handling
- Understanding authentication flow
- Configuring caching strategies

---

### 2. **QUICK_REFERENCE.md** (Developer Cheat Sheet)
**Size:** ~400 lines | **Purpose:** Quick lookup for common tasks

Quick reference guide with:
- API base URLs
- Quick start examples (cURL, JavaScript, Dart)
- HTTP status codes
- Common parameters and request bodies
- Token management quick tips
- Error codes quick lookup
- Common data types and ranges
- Timeout recommendations
- Rate limiting guidelines

**Use this when:**
- You need quick syntax for a cURL request
- Looking up HTTP status codes
- Finding example request formats
- Checking token management flow
- Need quick reference for data ranges/formats

---

### 3. **ENDPOINTS_SUMMARY.md** (Overview & Inventory)
**Size:** ~600 lines | **Purpose:** Complete endpoint inventory

Summary of all API endpoints organized by module:
- 28 total endpoints (18 protected, 10 public)
- Health & system endpoints (3)
- Authentication endpoints (4)
- Kundali management (7)
- Predictions (6)
- ML predictions (6)
- Transit calculations (3)
- Export endpoints (4 - production disabled)

Also includes:
- Feature extraction details
- Response time benchmarks
- Error handling guide
- Integration order recommendations
- Development vs production differences
- Performance optimization tips
- Security considerations
- Troubleshooting guide

**Use this when:**
- Getting overview of all available endpoints
- Planning API integration
- Understanding feature availability
- Checking endpoint authentication requirements
- Planning data models

---

### 4. **DATA_MODELS.md** (Schema Specification)
**Size:** ~1200 lines | **Purpose:** Complete data model specification

Detailed schema for all request/response models:
- Authentication models (UserRegisterRequest, LoginRequest, TokenResponse)
- Kundali models (KundaliRequest, KundaliSaveRequest, Ascendant, PlanetDetails)
- Prediction models (PredictionCreateRequest, PredictionResponse)
- Transit models (TransitRequest, TransitInfo)
- Enum types (Zodiac signs, Nakshatras, Planets)
- Data relationships and flow diagrams
- Validation rules for all fields
- Database constraints and indexes
- Sample complete data flows

Also includes:
- Field descriptions and constraints
- Type specifications and ranges
- Required vs optional fields
- Example JSON for each model
- Relationships between entities
- Sample flow for entire lifecycle (register → generate → predict → save)

**Use this when:**
- Implementing data models in client code
- Creating database schemas
- Validating input data
- Understanding data relationships
- Setting up type-safe models (TypeScript, Dart, etc.)

---

## Module Organization

### By Use Case

**For User Authentication:**
1. Read QUICK_REFERENCE.md → "Quick Start" → "Register User" / "Login"
2. Check API_DOCUMENTATION.md → "Authentication Endpoints" for full spec
3. Reference DATA_MODELS.md → "Authentication Models" for request/response schemas

**For Kundali Generation:**
1. Check ENDPOINTS_SUMMARY.md → "Kundali Generation"
2. Reference QUICK_REFERENCE.md → "Kundali Zodiac Signs" for context
3. Read API_DOCUMENTATION.md → "/kundali/generate_kundali" for complete spec
4. Use DATA_MODELS.md → "Kundali Models" for data structure

**For ML Predictions:**
1. Review ENDPOINTS_SUMMARY.md → "Key Statistics" for metrics overview
2. Check API_DOCUMENTATION.md → "ML Prediction Endpoints" for endpoints
3. Use QUICK_REFERENCE.md → "ML Prediction Metrics" for reference
4. Reference DATA_MODELS.md → "Prediction Models" for schemas

**For Transit Analysis:**
1. See ENDPOINTS_SUMMARY.md → "Transit Analysis"
2. Read API_DOCUMENTATION.md → "Transit Endpoints" for full spec
3. Check DATA_MODELS.md → "Transit Models" for request/response structure

---

## By File Size & Detail Level

### Quick Lookups (< 10 minutes)
- QUICK_REFERENCE.md - Fast syntax and parameter lookup
- ENDPOINTS_SUMMARY.md - Feature overview and organization

### Moderate Details (30-45 minutes)
- DATA_MODELS.md - Understand all data structures
- ENDPOINTS_SUMMARY.md - Detailed feature breakdown

### Complete Details (1-2 hours)
- API_DOCUMENTATION.md - Complete specification reading

---

## Development Workflow Recommendation

### Phase 1: Understand Available Features (30 min)
1. Read ENDPOINTS_SUMMARY.md introduction
2. Review ENDPOINTS_SUMMARY.md module organization
3. Check which endpoints match your requirements

### Phase 2: Design Data Models (45 min)
1. Read relevant sections in DATA_MODELS.md
2. Review sample complete flows
3. Understand relationships and constraints
4. Plan your client-side models

### Phase 3: Implement Features (ongoing)
1. Reference QUICK_REFERENCE.md for syntax examples
2. Use API_DOCUMENTATION.md for complete endpoint specs
3. Check DATA_MODELS.md for request/response structure
4. Reference error codes and handling recommendations

### Phase 4: Test & Debug (ongoing)
1. Use HTTP status code reference in QUICK_REFERENCE.md
2. Check error codes in ENDPOINTS_SUMMARY.md
3. Read error handling section in API_DOCUMENTATION.md
4. Troubleshooting guide in ENDPOINTS_SUMMARY.md

---

## API Summary Statistics

### Endpoints: 28 Total
- Public endpoints: 10
- Protected endpoints: 18

### By Category
- Health & Status: 3
- Authentication: 4
- Kundali Management: 7
- Predictions: 6
- ML Predictions: 6
- Transits: 3
- Export: 4 (production disabled)

### Authentication
- Type: JWT Bearer Token
- Access token expiry: 15 minutes
- Refresh token expiry: 7 days
- Algorithm: HS256

### ML Features
- Input features: 53 astrological metrics
- Output metrics: 8 life outcome predictions
- Models: XGBoost (primary), Neural Network (optional)

### Database
- Type: MongoDB
- Collections: users, kundalis, predictions, user_settings
- Unique indexes: email, username
- Foreign keys: user_id, kundali_id

### Performance
- Kundali generation: 1-2 seconds
- ML predictions: 200-500ms
- Transit calculations: 500ms-2 seconds
- Database operations: 100-300ms

---

## Key Features by Endpoint Type

### Kundali Generation
- Complete astrological analysis
- Planetary positions & houses
- Dasha system (life periods)
- Yogas (auspicious combinations)
- Planetary strengths
- ML feature extraction

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
- Save/retrieve kundalis
- Create/update/delete predictions
- User profile management
- List operations with pagination

---

## Authentication Flow

```
1. Register: POST /auth/register
   → Returns: access_token + refresh_token

2. Login: POST /auth/login
   → Returns: access_token + refresh_token

3. Protected Requests: Add "Authorization: Bearer {token}"

4. Token Expiration (15 min): POST /auth/refresh
   → Returns: new access_token + refresh_token
```

---

## Common Integration Patterns

### Pattern 1: Generate & Predict
```
1. POST /kundali/generate_kundali (public)
   → Get complete kundali + ml_features

2. POST /ml/predict (public, option A)
   OR
   POST /ml/predict-from-kundali (public, option B)
   → Get 8 prediction scores

3. POST /predictions/ (authenticated, optional)
   → Save prediction to user's profile
```

### Pattern 2: Authenticated Workflow
```
1. POST /auth/register
   → Get access_token

2. POST /kundali/save
   → Save kundali to profile

3. GET /kundali/list
   → List all user's kundalis

4. POST /predictions/
   → Create prediction for kundali

5. GET /predictions/list
   → List all user's predictions
```

### Pattern 3: Transit Analysis
```
1. POST /transits/calculate
   → Get current transits

2. POST /transits/upcoming
   → Get upcoming transits (365 days)

3. POST /transits/dasha-transit-analysis
   → Analyze dasha + transit interaction
```

---

## Response Format (All Endpoints)

### Success
```json
{
  "status": "success",
  "success": true,
  "data": {...},
  "message": "Success message",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### Error
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

## Recommended Reading Order

### For Backend Integration
1. QUICK_REFERENCE.md - Get familiar with syntax
2. API_DOCUMENTATION.md (selective) - Focus on endpoints you need
3. DATA_MODELS.md - Understand request/response structure
4. ENDPOINTS_SUMMARY.md - Error handling and best practices

### For Frontend Development
1. QUICK_REFERENCE.md - Understand available endpoints
2. ENDPOINTS_SUMMARY.md - Feature overview
3. DATA_MODELS.md - Data structures and validation
4. API_DOCUMENTATION.md - Complete endpoint details as needed

### For Mobile App (Dart/Flutter)
1. QUICK_REFERENCE.md - See Dart examples
2. DATA_MODELS.md - Create models that match API schemas
3. ENDPOINTS_SUMMARY.md - Error handling strategy
4. API_DOCUMENTATION.md - Authentication & caching guidelines

### For ML Integration
1. ENDPOINTS_SUMMARY.md - ML endpoints overview
2. API_DOCUMENTATION.md - ML endpoint specifications
3. QUICK_REFERENCE.md - Quick syntax reference

---

## Need Help?

### Finding Something Specific

**"How do I register a user?"**
→ QUICK_REFERENCE.md: "Quick Start"

**"What's the error code for invalid token?"**
→ QUICK_REFERENCE.md: "Error Codes"

**"What fields does Kundali have?"**
→ DATA_MODELS.md: "Kundali Models"

**"How do I authenticate requests?"**
→ API_DOCUMENTATION.md: "Authentication"

**"What's the timeout for predictions?"**
→ QUICK_REFERENCE.md: "Timeout Recommendations"

**"How should I handle pagination?"**
→ ENDPOINTS_SUMMARY.md: "Pagination"

**"What's the complete spec for /kundali/generate_kundali?"**
→ API_DOCUMENTATION.md: "Kundali Endpoints"

---

## Document Statistics

| Document | Lines | Size | Purpose |
|----------|-------|------|---------|
| API_DOCUMENTATION.md | 3500+ | ~120KB | Complete specification |
| DATA_MODELS.md | 1200+ | ~45KB | Data schema details |
| ENDPOINTS_SUMMARY.md | 600+ | ~25KB | Overview & inventory |
| QUICK_REFERENCE.md | 400+ | ~18KB | Quick lookup |
| Total | 5700+ | ~210KB | Complete documentation |

---

## Version & Updates

- **API Version:** 1.0.0
- **Database Schema:** 1.0
- **ML Model Version:** 1.0.0
- **Documentation Date:** January 2024

Breaking changes will increment major version (2.0.0).
Non-breaking additions increment minor version (1.1.0).
Bug fixes increment patch version (1.0.1).

---

## File Locations

All files are located in: `C:\Users\ACER\Desktop\FInalProject\docs\api\`

- `API_DOCUMENTATION.md` - Primary reference
- `QUICK_REFERENCE.md` - Quick lookup guide
- `ENDPOINTS_SUMMARY.md` - Feature overview
- `DATA_MODELS.md` - Schema specifications
- `README.md` - This file (documentation guide)

---

## Contributing

When updating documentation:
1. Keep format consistent with existing files
2. Update version number if changing specs
3. Update statistics in this README
4. Cross-reference between documents
5. Include examples for new endpoints
6. Test examples before documenting

---

## Related Documentation

- Frontend specifications: `/docs/design/design-system.md`
- State management: `/docs/state-management/`
- Deployment guide: `/docs/deployment/railway-deployment-guide.md`
- Development status: `/docs/progress/development-status.md`

