# State Management Data Models - Complete Specification

**Framework:** Riverpod with Dart/Flutter
**Status:** Architecture Complete
**Last Updated:** November 2025

---

## Overview

This document defines all data models (Dart classes) used throughout the Kundali application. These models represent the data structures exchanged between UI, state management, services, and backend API.

**Total Models:** 40+
**Data Points:** 500+ per Kundali

---

## Authentication Models

### AuthState (StateNotifier State)

Core state model for authentication system.

```dart
class AuthState {
  final bool isAuthenticated;
  final String? token;
  final User? user;
  final String? error;
  final DateTime? tokenExpiresAt;
  final bool isLoading;

  AuthState({
    required this.isAuthenticated,
    this.token,
    this.user,
    this.error,
    this.tokenExpiresAt,
    this.isLoading = false,
  });

  // Copy constructor for immutable updates
  AuthState copyWith({
    bool? isAuthenticated,
    String? token,
    User? user,
    String? error,
    DateTime? tokenExpiresAt,
    bool? isLoading,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      token: token ?? this.token,
      user: user ?? this.user,
      error: error ?? this.error,
      tokenExpiresAt: tokenExpiresAt ?? this.tokenExpiresAt,
      isLoading: isLoading ?? this.isLoading,
    );
  }
}
```

**Properties:**
- `isAuthenticated`: Whether user is logged in
- `token`: JWT token for API requests
- `user`: Current user profile
- `error`: Error message if login failed
- `tokenExpiresAt`: When JWT token expires (for auto-refresh)
- `isLoading`: Request in progress

**Usage:**
```dart
// In providers or widgets
final isAuth = ref.watch(authProvider.select((state) => state.isAuthenticated));
final user = ref.watch(authProvider.select((state) => state.user));
```

---

### User Model

Represents a user profile.

```dart
class User {
  final String id;                    // MongoDB ObjectId as String
  final String name;
  final String email;
  final String? birthDate;            // YYYY-MM-DD
  final String? birthTime;            // HH:MM
  final double? latitude;
  final double? longitude;
  final String? timezone;
  final DateTime createdAt;
  final DateTime? lastUpdatedAt;

  User({
    required this.id,
    required this.name,
    required this.email,
    this.birthDate,
    this.birthTime,
    this.latitude,
    this.longitude,
    this.timezone,
    required this.createdAt,
    this.lastUpdatedAt,
  });

  // Convenience getter - has complete birth data
  bool get hasCompleteBirthData =>
      birthDate != null &&
      birthTime != null &&
      latitude != null &&
      longitude != null &&
      timezone != null;

  User copyWith({
    String? id,
    String? name,
    String? email,
    String? birthDate,
    String? birthTime,
    double? latitude,
    double? longitude,
    String? timezone,
    DateTime? createdAt,
    DateTime? lastUpdatedAt,
  }) {
    return User(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      birthDate: birthDate ?? this.birthDate,
      birthTime: birthTime ?? this.birthTime,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      timezone: timezone ?? this.timezone,
      createdAt: createdAt ?? this.createdAt,
      lastUpdatedAt: lastUpdatedAt ?? this.lastUpdatedAt,
    );
  }
}
```

**Properties:**
- `id`: Unique user identifier from MongoDB
- `name`: Full name
- `email`: Email address (unique)
- `birthDate`: Birth date (YYYY-MM-DD)
- `birthTime`: Birth time (HH:MM)
- `latitude`, `longitude`: Birth location coordinates
- `timezone`: Birth timezone (IANA format)
- `createdAt`: Account creation timestamp
- `lastUpdatedAt`: Last profile update

---

## Kundali Models

### Kundali (Main Birth Chart)

Complete birth chart with all astrological data.

```dart
class Kundali {
  final String id;
  final String userId;
  final String birthDate;
  final String birthTime;
  final double latitude;
  final double longitude;
  final String timezone;
  final double julianDay;

  // Core astrological data
  final Ascendant ascendant;
  final Map<String, Planet> planets;        // "Sun", "Moon", "Mars", etc.
  final Map<int, House> houses;             // 1-12
  final String zodiacSign;                  // Sun sign (tropical)
  final String rulingPlanet;                // Moon sign lord

  // Advanced calculations
  final Dasha dasha;
  final ShadBala shadBala;
  final Map<String, DivisionalChart> divisionalCharts;  // D1, D2, D7, D9
  final List<Yoga> yogas;

  // ML extracted features
  final Map<String, dynamic> mlFeatures;    // 53+ features

  // Metadata
  final DateTime calculatedAt;
  final String ephemerisVersion;

  Kundali({
    required this.id,
    required this.userId,
    required this.birthDate,
    required this.birthTime,
    required this.latitude,
    required this.longitude,
    required this.timezone,
    required this.julianDay,
    required this.ascendant,
    required this.planets,
    required this.houses,
    required this.zodiacSign,
    required this.rulingPlanet,
    required this.dasha,
    required this.shadBala,
    required this.divisionalCharts,
    required this.yogas,
    required this.mlFeatures,
    required this.calculatedAt,
    required this.ephemerisVersion,
  });
}
```

**Key Properties:**
- `ascendant`: Lagna (rising sign) - critical for accuracy
- `planets`: 9 celestial bodies with positions
- `houses`: 12 houses with planets and lords
- `dasha`: Current life period (Vimshottari)
- `shadBala`: 6 planetary strength measures
- `divisionalCharts`: D1 (main), D2 (wealth), D7 (children), D9 (spouse)
- `mlFeatures`: 53+ features for ML predictions

---

### Ascendant

Rising sign / Lagna - defines house system.

```dart
class Ascendant {
  final int index;                    // 1-12 (Aries=1, Taurus=2, etc.)
  final String sign;                  // "Aries", "Taurus", etc.
  final double longitude;             // 0-360 degrees
  final double degree;                // Within sign (0-30)
  final String nakshatra;             // 27 lunar mansions
  final int pada;                     // 1-4 (quarter within nakshatra)
  final String lord;                  // Ruling planet

  Ascendant({
    required this.index,
    required this.sign,
    required this.longitude,
    required this.degree,
    required this.nakshatra,
    required this.pada,
    required this.lord,
  });
}
```

**Properties:**
- `index`: Sign number (Aries=1 to Pisces=12)
- `nakshatra`: Lunar mansion (27 total)
- `pada`: Quarter position within nakshatra (1-4)
- `lord`: Planet ruling this sign (e.g., Mars for Aries)

**Significance:** Defines entire chart structure, house placement, and life themes.

---

### Planet

Planetary position and characteristics.

```dart
class Planet {
  final String name;                  // "Sun", "Moon", "Mars", etc.
  final double longitude;             // 0-360 degrees (sidereal)
  final double tropicalLongitude;     // Tropical zodiac
  final String sign;                  // "Taurus", "Gemini", etc.
  final int signNumber;               // 1-12
  final double degreeInSign;          // 0-30
  final String nakshatra;             // 27 lunar mansions
  final int pada;                     // 1-4 within nakshatra
  final int house;                    // 1-12
  final bool isRetrograde;            // Moving backwards
  final bool isCombust;               // Too close to Sun
  final double speed;                 // Degrees per day
  final String dignity;               // "Exalted", "Own", "Neutral", "Debilitated"
  final bool isVargottama;            // Same sign in D9 chart

  // Aspect information
  final List<Aspect> aspects;         // Aspects from other planets

  Planet({
    required this.name,
    required this.longitude,
    required this.tropicalLongitude,
    required this.sign,
    required this.signNumber,
    required this.degreeInSign,
    required this.nakshatra,
    required this.pada,
    required this.house,
    required this.isRetrograde,
    required this.isCombust,
    required this.speed,
    required this.dignity,
    required this.isVargottama,
    required this.aspects,
  });
}
```

**Key Properties:**
- `longitude`: Actual position (0-360°)
- `sign`: Zodiac sign (Aries-Pisces)
- `nakshatra`: Lunar mansion (27 total)
- `house`: House placement (1-12)
- `isRetrograde`: Appears to move backwards
- `dignity`: Strength based on sign position
- `aspects`: Other planets it aspects

**Natural Significances:**
```
Sun      → Soul, Father, Authority, Vitality
Moon     → Mind, Mother, Emotions, Public
Mars     → Energy, Courage, Siblings, Property
Mercury  → Communication, Intelligence, Business
Jupiter  → Wisdom, Children, Spirituality, Luck
Venus    → Love, Beauty, Arts, Luxury, Creativity
Saturn   → Discipline, Delays, Karma, Hardwork
Rahu     → Illusion, Foreign, Technology, Sudden
Ketu     → Spirituality, Detachment, Past Life
```

---

### House

Astrological house - life domains.

```dart
class House {
  final int number;                   // 1-12
  final String sign;                  // "Aries", "Taurus", etc.
  final int signNumber;               // 1-12
  final List<String> planetsInHouse;  // Planet names
  final int planetCount;              // How many planets
  final String lord;                  // Ruling planet
  final double cusp;                  // Exact degree of cusp
  final bool isEmpty;                 // No planets

  House({
    required this.number,
    required this.sign,
    required this.signNumber,
    required this.planetsInHouse,
    required this.planetCount,
    required this.lord,
    required this.cusp,
    required this.isEmpty,
  });
}
```

**House Significances:**
```
1  → Self, Personality, Health, Appearance
2  → Wealth, Family, Speech, Resources
3  → Siblings, Communication, Short travel
4  → Home, Mother, Property, Education
5  → Children, Creativity, Romance, Intellect
6  → Enemies, Diseases, Service, Debts
7  → Marriage, Partnership, Contracts, Others
8  → Transformation, Inheritance, Death, Occult
9  → Luck, Dharma, Father, Higher learning
10 → Career, Reputation, Authority, Achievement
11 → Gains, Friends, Income, Wishes
12 → Losses, Spirituality, Moksha, Seclusion
```

---

### Dasha (Time Periods)

Life cycle progression system (Vimshottari).

```dart
class Dasha {
  final String moonNakshatra;         // Birth lunar mansion

  // Current major period
  final String currentMahaDasha;      // Planet ruling major period
  final DateTime mahaDashaStartDate;
  final DateTime mahaDashaEndDate;
  final int mahaDashaDurationYears;
  final double remainingMahaDashaYears;
  final double progressionPercentage;  // 0-100

  // Current sub-period
  final String currentAntarDasha;     // Planet ruling sub-period
  final DateTime antarDashaStartDate;
  final DateTime antarDashaEndDate;

  // Dasha interpretation
  final String interpretation;        // AI-generated text
  final List<PredictionPeriod> periodPredictions;

  Dasha({
    required this.moonNakshatra,
    required this.currentMahaDasha,
    required this.mahaDashaStartDate,
    required this.mahaDashaEndDate,
    required this.mahaDashaDurationYears,
    required this.remainingMahaDashaYears,
    required this.progressionPercentage,
    required this.currentAntarDasha,
    required this.antarDashaStartDate,
    required this.antarDashaEndDate,
    required this.interpretation,
    required this.periodPredictions,
  });
}
```

**Dasha Periods (9 planets, 120-year cycle):**
```
Ketu   → 7 years     Detachment, Past-life karma
Venus  → 20 years    Relationships, Creative growth
Sun    → 6 years     Authority, Father, Leadership
Moon   → 10 years    Emotions, Mother, Nurturing
Mars   → 7 years     Energy, Courage, Conflict
Rahu   → 18 years    Foreign, Technology, Illusion
Jupiter→ 16 years    Expansion, Wisdom, Children
Saturn → 19 years    Restriction, Lessons, Delays
Mercury→ 17 years    Communication, Intellect, Business
```

---

### ShadBala (Planetary Strengths)

Six measures of planetary strength.

```dart
class ShadBala {
  // 1. Sthana Bala - Positional strength
  final Map<String, double> sthanaBala;    // Per planet

  // 2. Dig Bala - Directional strength
  final Map<String, double> digBala;

  // 3. Kala Bala - Temporal strength
  final Map<String, double> kalaBala;

  // 4. Chesta Bala - Motion strength
  final Map<String, double> chestaBala;

  // 5. Naisargika Bala - Natural strength
  final Map<String, double> naisargikaBala;

  // 6. Drishti Bala - Aspect strength
  final Map<String, double> drishtiBalA;

  // Overall strength
  final Map<String, double> totalPlanetaryStrength;  // 0-100
  final Map<String, double> houseLordStrengths;

  ShadBala({
    required this.sthanaBala,
    required this.digBala,
    required this.kalaBala,
    required this.chestaBala,
    required this.naisargikaBala,
    required this.drishtiBalA,
    required this.totalPlanetaryStrength,
    required this.houseLordStrengths,
  });
}
```

**Strength Measurement:** Each measure produces 0-100 strength score

---

### Aspect

Inter-planetary relationship.

```dart
class Aspect {
  final String planet1;               // "Sun", "Moon", etc.
  final String planet2;
  final String type;                  // "Conjunction", "Sextile", etc.
  final double orb;                   // Degrees of difference
  final double strength;              // 0-100% effectiveness
  final bool isApplying;              // Getting closer or separating
  final String interpretation;        // Meaning of aspect

  Aspect({
    required this.planet1,
    required this.planet2,
    required this.type,
    required this.orb,
    required this.strength,
    required this.isApplying,
    required this.interpretation,
  });
}
```

**Aspect Types:**
```
Conjunction (0°)  → Combined energy, fusion
Sextile (60°)     → Easy flow, supportive
Square (90°)      → Tension, challenge, growth
Trine (120°)      → Harmonious, natural gift
Opposition (180°) → Polarity, balance needed
```

---

### Yoga (Auspicious Combination)

Special planetary combinations.

```dart
class Yoga {
  final String name;                  // "Raj Yoga", "Dhana Yoga", etc.
  final String type;                  // "Benefic", "Malefic"
  final List<String> planets;         // Planets involved
  final int house;                    // House location
  final double strength;              // 0-100
  final String interpretation;        // Meaning

  Yoga({
    required this.name,
    required this.type,
    required this.planets,
    required this.house,
    required this.strength,
    required this.interpretation,
  });
}
```

**Common Yogas:**
```
Raj Yoga           → Kendra + Trikona lord together → Power, authority
Parivartana Yoga   → Planets exchange signs → Mutual support
Neecha Bhanga      → Debilitated planet gets relief → Overcoming obstacles
Gaja Kesari Yoga   → Jupiter-Moon conjunction → Intelligence, wisdom
```

---

### DivisionalChart (Varga)

Subdivisions of main chart for specific life areas.

```dart
class DivisionalChart {
  final String type;                  // "D1", "D2", "D7", "D9"
  final String name;                  // "Rasi", "Hora", "Saptamsha", "Navamsha"
  final Map<String, Planet> planets;  // Planet positions in this chart
  final Map<int, House> houses;       // House divisions
  final Ascendant ascendant;          // Lagna in this chart
  final List<Yoga> yogas;             // Yogas in this chart
  final Map<String, dynamic> interpretation;

  DivisionalChart({
    required this.type,
    required this.name,
    required this.planets,
    required this.houses,
    required this.ascendant,
    required this.yogas,
    required this.interpretation,
  });
}
```

**Chart Types:**
```
D1 (Rasi)       → Main birth chart (all life areas)
D2 (Hora)       → Wealth and finances (1 sign ÷ 2)
D7 (Saptamsha)  → Children and fertility (1 sign ÷ 7)
D9 (Navamsha)   → Spouse and destiny (1 sign ÷ 9)
```

---

## Prediction Models

### Prediction

Single life dimension prediction.

```dart
class Prediction {
  final String id;
  final String userId;
  final String kundaliId;

  // Prediction content
  final String dimension;             // "Career", "Relationships", etc.
  final String title;
  final String prediction;            // AI-generated text
  final double confidence;            // 0-1 (0-100%)
  final String confidenceLevel;       // "High", "Medium", "Low"

  // Timing
  final DateTime periodStart;
  final DateTime periodEnd;
  final int periodDays;

  // ML details
  final List<double> mlFeatures;      // 53 features used
  final String modelVersion;
  final double modelScore;            // Raw model output

  // Metadata
  final DateTime generatedAt;

  Prediction({
    required this.id,
    required this.userId,
    required this.kundaliId,
    required this.dimension,
    required this.title,
    required this.prediction,
    required this.confidence,
    required this.confidenceLevel,
    required this.periodStart,
    required this.periodEnd,
    required this.periodDays,
    required this.mlFeatures,
    required this.modelVersion,
    required this.modelScore,
    required this.generatedAt,
  });
}
```

**Prediction Dimensions:**
```
1. Career         → Professional path, success timeline
2. Relationships  → Love, marriage, partnerships
3. Health         → Physical and mental wellness
4. Finance        → Wealth, income, investments
5. Education      → Learning, academic success
6. Family         → Parents, siblings, household
7. Travel         → Journeys, relocation, exploration
8. Spirituality   → Inner growth, enlightenment
```

---

### MLFeatures (Astrological Data for ML)

Extracted features for machine learning.

```dart
class MLFeatures {
  // Birth details (9 features)
  final int birthYear;
  final int birthMonth;
  final int birthDay;
  final int birthHour;
  final int birthMinute;
  final double latitude;
  final double longitude;
  final double timezone;
  final double julianDay;

  // Ascendant (6 features)
  final double ascendantDegree;
  final int ascendantSign;
  final int ascendantNakshatra;
  final int ascendantPada;
  final int ascendantHouse;
  final String ascendantLord;

  // Planets (72 features = 9 planets × 8 features)
  // For each planet: longitude, sign, sign_number, house, nakshatra, pada, degree_in_sign, dignity
  final List<PlanetFeature> planetFeatures;

  // Houses (48 features = 12 houses × 4 features)
  final List<HouseFeature> houseFeatures;

  // Aspects & Yogas
  final int totalAspectCount;
  final int beneficYogaCount;
  final int maleficYogaCount;

  // Special features
  final String moonSign;
  final String sunSign;
  final String rulingPlanet;
  final String chartPattern;        // "Stellium", "Scattered", "Balanced"
  final String dominantElement;     // "Fire", "Earth", "Air", "Water"
  final String dominantQuality;     // "Cardinal", "Fixed", "Mutable"

  MLFeatures({
    required this.birthYear,
    required this.birthMonth,
    required this.birthDay,
    required this.birthHour,
    required this.birthMinute,
    required this.latitude,
    required this.longitude,
    required this.timezone,
    required this.julianDay,
    required this.ascendantDegree,
    required this.ascendantSign,
    required this.ascendantNakshatra,
    required this.ascendantPada,
    required this.ascendantHouse,
    required this.ascendantLord,
    required this.planetFeatures,
    required this.houseFeatures,
    required this.totalAspectCount,
    required this.beneficYogaCount,
    required this.maleficYogaCount,
    required this.moonSign,
    required this.sunSign,
    required this.rulingPlanet,
    required this.chartPattern,
    required this.dominantElement,
    required this.dominantQuality,
  });
}
```

**Total Features:** 53+ used in XGBoost models

---

## Request/Response Models

### KundaliGenerationRequest

Request to generate a Kundali.

```dart
class KundaliGenerationRequest {
  final String birthDate;            // YYYY-MM-DD
  final String birthTime;            // HH:MM (24-hour)
  final double latitude;             // -90 to 90
  final double longitude;            // -180 to 180
  final String timezone;             // IANA timezone

  KundaliGenerationRequest({
    required this.birthDate,
    required this.birthTime,
    required this.latitude,
    required this.longitude,
    required this.timezone,
  });

  Map<String, dynamic> toJson() => {
    'birthDate': birthDate,
    'birthTime': birthTime,
    'latitude': latitude,
    'longitude': longitude,
    'timezone': timezone,
  };
}
```

---

### APIResponse<T> (Generic Response Wrapper)

Standard API response format.

```dart
class APIResponse<T> {
  final String status;                // "success" or "error"
  final bool success;
  final T? data;
  final String? error;
  final String message;
  final String? requestId;

  APIResponse({
    required this.status,
    required this.success,
    this.data,
    this.error,
    required this.message,
    this.requestId,
  });

  factory APIResponse.fromJson(
    Map<String, dynamic> json,
    T Function(dynamic) fromJsonT,
  ) {
    return APIResponse(
      status: json['status'] as String,
      success: json['success'] as bool,
      data: json['data'] != null ? fromJsonT(json['data']) : null,
      error: json['error'] as String?,
      message: json['message'] as String? ?? '',
      requestId: json['request_id'] as String?,
    );
  }
}
```

**All API endpoints return this format:**
```json
{
  "status": "success",
  "success": true,
  "data": { /* specific data */ },
  "error": null,
  "message": "Success message",
  "request_id": "req_12345"
}
```

---

### LoginRequest/Response

```dart
class LoginRequest {
  final String email;
  final String password;

  LoginRequest({
    required this.email,
    required this.password,
  });
}

class LoginResponse {
  final String userId;
  final String email;
  final String name;
  final String token;
  final DateTime expiresAt;

  LoginResponse({
    required this.userId,
    required this.email,
    required this.name,
    required this.token,
    required this.expiresAt,
  });
}
```

---

## Error Models

### AppException (Base Exception)

```dart
abstract class AppException implements Exception {
  final String message;
  final String? code;
  final dynamic originalException;

  AppException({
    required this.message,
    this.code,
    this.originalException,
  });

  @override
  String toString() => message;
}

class NetworkException extends AppException {
  NetworkException({
    required String message,
    dynamic originalException,
  }) : super(
    message: message,
    code: 'NETWORK_ERROR',
    originalException: originalException,
  );
}

class ValidationException extends AppException {
  final Map<String, String> errors;

  ValidationException({
    required String message,
    required this.errors,
  }) : super(
    message: message,
    code: 'VALIDATION_ERROR',
  );
}

class AuthenticationException extends AppException {
  AuthenticationException({
    required String message,
  }) : super(
    message: message,
    code: 'AUTH_ERROR',
  );
}

class ServerException extends AppException {
  ServerException({
    required String message,
    String? code,
  }) : super(
    message: message,
    code: code ?? 'SERVER_ERROR',
  );
}
```

**Exception Handling Pattern:**
```dart
try {
  final kundali = await apiService.generateKundali(birthDate);
} on ValidationException catch (e) {
  // Handle validation errors
  print('Validation failed: ${e.errors}');
} on NetworkException catch (e) {
  // Handle network errors
  print('Network error: ${e.message}');
} on AuthenticationException catch (e) {
  // Handle auth errors - logout user
  ref.invalidate(authProvider);
} catch (e) {
  // Handle unexpected errors
  print('Unexpected error: $e');
}
```

---

## UI State Models

### LoadingState

```dart
class LoadingState {
  final bool isLoading;
  final String? message;
  final double? progress;             // 0-1 for progress bars

  LoadingState({
    this.isLoading = false,
    this.message,
    this.progress,
  });
}
```

---

### FilterState

```dart
class FilterState {
  final String? dimensionFilter;      // Filter predictions by dimension
  final String? sortBy;               // "date", "confidence", "dimension"
  final bool sortAscending;
  final DateRange? dateRange;

  FilterState({
    this.dimensionFilter,
    this.sortBy = 'date',
    this.sortAscending = false,
    this.dateRange,
  });
}

class DateRange {
  final DateTime start;
  final DateTime end;

  DateRange({
    required this.start,
    required this.end,
  });
}
```

---

## Data Model Organization

### In Providers

```dart
// lib/data/models/

// Core models
├── auth/
│   ├── auth_state.dart
│   ├── user.dart
│   └── user_request.dart
│
├── kundali/
│   ├── kundali.dart
│   ├── ascendant.dart
│   ├── planet.dart
│   ├── house.dart
│   ├── dasha.dart
│   ├── shad_bala.dart
│   ├── yoga.dart
│   ├── divisional_chart.dart
│   └── aspect.dart
│
├── prediction/
│   ├── prediction.dart
│   ├── ml_features.dart
│   └── prediction_request.dart
│
├── common/
│   ├── api_response.dart
│   └── exceptions.dart
│
└── ui/
    ├── loading_state.dart
    └── filter_state.dart
```

---

## Model Relationships

```
┌─────────────┐
│   AuthState │
│   ├─ token  │
│   └─ user ──────────┐
└─────────────┘       │
                      ▼
              ┌─────────────────┐
              │      User       │
              │  ├─ birthDate   │
              │  ├─ latitude    │
              │  └─ longitude   │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │    Kundali      │
              │  ├─ ascendant   │
              │  ├─ planets     │
              │  ├─ houses      │
              │  ├─ dasha       │
              │  ├─ shad_bala   │
              │  ├─ yogas       │
              │  ├─ div_charts  │
              │  └─ ml_features │
              └─────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐
   │Planet    │ │House     │ │Prediction│
   │├─ aspects│ │├─ lord   │ │├─ dimension
   │└─ dignity│ │└─ empty  │ │├─ confidence
   └──────────┘ └──────────┘ │└─ ml_score
                              └──────────┘
```

---

## Common Model Conversions

### From API JSON to Dart Models

```dart
// API returns JSON
final jsonResponse = {
  'ascendant': {
    'index': 6,
    'sign': 'Virgo',
    'longitude': 151.90,
    // ...
  },
  'planets': {
    'Sun': {
      'longitude': 30.55,
      'sign': 'Taurus',
      // ...
    }
  }
};

// Convert to Dart models
final kundali = Kundali.fromJson(jsonResponse);
```

### From Dart Models to API Request

```dart
final request = KundaliGenerationRequest(
  birthDate: '1990-05-15',
  birthTime: '14:30',
  latitude: 28.7041,
  longitude: 77.1025,
  timezone: 'Asia/Kolkata',
);

// Convert to JSON
final json = request.toJson();
```

---

## Serialization Considerations

✅ **DO:**
- Use `@JsonSerializable` annotation for automatic JSON serialization
- Define `fromJson()` factory constructors
- Implement `toJson()` methods
- Handle nullable fields properly (`String?`)

❌ **AVOID:**
- Manual JSON parsing (error-prone)
- Inconsistent naming (use camelCase in Dart, snake_case in JSON)
- Forgetting to implement copyWith() for immutable updates

---

## Performance Optimization

**Large Models (Kundali with 500+ properties):**
```dart
// Split into smaller models
class KundaliPreview {
  final String id;
  final Ascendant ascendant;
  final String zodiacSign;
  // Only essential fields
}

// Load detailed data on demand
class KundaliDetail extends KundaliPreview {
  final Map<String, Planet> planets;
  final Map<int, House> houses;
  // Full data
}
```

---

## Model Testing

```dart
test('Kundali model copyWith works correctly', () {
  final kundali1 = Kundali(
    id: '1',
    birthDate: '1990-05-15',
    // ...
  );

  final kundali2 = kundali1.copyWith(
    birthDate: '1990-05-16',
  );

  expect(kundali2.id, kundali1.id);
  expect(kundali2.birthDate, '1990-05-16');
});
```

---

**Related:** See [state-patterns.md](state-patterns.md) for how these models are used
**Related:** See [data-flow.md](data-flow.md) for how data moves between models
