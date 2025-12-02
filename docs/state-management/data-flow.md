# State Management Data Flow - Riverpod

**Framework:** Riverpod (Functional Reactive State Management)
**Status:** Architecture Complete
**Last Updated:** November 2025

---

## Overview

This document describes how data flows through the Kundali application using Riverpod's reactive provider system.

**Key Principle:** Data flows downward from services → providers → UI, while mutations flow upward from UI → notifiers → services.

---

## High-Level Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Widget/Screen (UI Layer)                    │
│              ref.watch(provider) / ref.read(notifier)            │
└────────────────────────┬──────────────────────────────────────┘
                         │ Subscribes
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Providers (State Layer)                        │
│  • StateNotifier (auth, app state)                              │
│  • FutureProvider (async data)                                  │
│  • StreamProvider (real-time data)                              │
│  • Provider (derived/computed state)                            │
└────────────────────────┬──────────────────────────────────────┘
                         │ Watches/Reads
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Services (Business Logic)                       │
│  • AuthService (JWT, login/logout)                              │
│  • ApiClient (HTTP requests)                                    │
│  • AstroService (calculations)                                  │
│  • KundaliRepository (Kundali data)                             │
└────────────────────────┬──────────────────────────────────────┘
                         │ Calls
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            External Resources (Backend/Database)                 │
│  • FastAPI REST endpoints                                       │
│  • MongoDB database                                             │
│  • JWT token management                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow

### 1. User Initiates Login

```dart
// Widget calls notifier method
ref.read(authProvider.notifier).login(email, password);
```

### 2. AuthNotifier Processes Login

```
UI Layer
  └─→ AuthNotifier.login()
      └─→ AuthService.login()
          └─→ ApiClient.POST /auth/login
              └─→ Backend (FastAPI)
                  └─→ MongoDB validation
                      └─→ JWT token generation
                          └─→ Response: {token, user}
```

### 3. State Updates Cascade

```dart
// AuthNotifier updates state (line 69-74 of state-patterns.md example)
state = state.copyWith(
  isAuthenticated: true,
  token: response.token,
  user: response.user,
  error: null,
);

// All widgets watching authProvider are notified
// ▼
// authProvider listeners rebuild
// ▼
// isAuthenticatedProvider listeners rebuild (select optimization)
// ▼
// UI recomputes and displays authenticated content
```

### 4. Token Storage & Persistence

```
AuthService.login()
  ├─→ Save token to SecureStorage
  ├─→ Update AuthState in provider
  └─→ Notify all listeners

// Automatic persistence flow:
// Token stored → On app restart → Load token from storage
// → Restore AuthState → UI shows authenticated state
```

### 5. Logout Flow

```dart
ref.read(authProvider.notifier).logout();

// Flow:
AuthNotifier.logout()
  ├─→ ApiClient.POST /auth/logout
  ├─→ Clear SecureStorage
  ├─→ AuthService.logout()
  ├─→ state = AuthState(isAuthenticated: false)
  └─→ Invalidate dependent providers
      ├─→ invalidate(userKundaliProvider)
      ├─→ invalidate(predictionsProvider)
      └─→ UI redirects to login
```

---

## Kundali Generation Flow

### 1. User Submits Birth Details

```dart
// KundaliScreen collects birth data
final birthData = {
  'birthDate': '1990-05-15',
  'birthTime': '14:30',
  'latitude': 28.7041,
  'longitude': 77.1025,
  'timezone': 'Asia/Kolkata'
};

// Call generation
ref.read(kundaliProvider(birthData).notifier).generate();
```

### 2. Data Flow Through Providers

```
KundaliScreen (UI)
  │
  └─→ kundaliProvider.family<Kundali, String>
      │ (param: birthDate)
      │
      ├─→ Checks cache (has it been calculated?)
      │   ├─→ YES: Return cached Kundali
      │   └─→ NO: Continue
      │
      └─→ ApiClient.POST /kundali/generate_kundali
          │
          ├─→ Backend calculations:
          │   ├─→ Julian Day calculation
          │   ├─→ Planetary positions (SwissEphemeris)
          │   ├─→ House calculations
          │   ├─→ Dasha system
          │   ├─→ Shad Bala (planetary strengths)
          │   ├─→ ML features extraction (53 features)
          │   └─→ Divisional charts (D1, D2, D7, D9)
          │
          └─→ Response: Complete Kundali object
              │
              └─→ FutureProvider caches result
                  │
                  └─→ All listeners notified
                      ├─→ KundaliScreen (displays chart)
                      ├─→ userKundaliProvider (depends on this)
                      ├─→ predictionsProvider (depends on Kundali)
                      └─→ Other derived providers
```

### 3. Dependent Providers Cascade

```dart
// userKundaliProvider depends on kundaliProvider
final userKundaliProvider = FutureProvider<Kundali>((ref) async {
  final authState = ref.watch(authProvider);
  final kundali = await ref.watch(
    kundaliProvider(authState.user!.birthDate).future
  );
  return kundali;
});

// When userKundaliProvider resolves:
// ▼
// predictionsProvider watches userKundaliProvider
// ▼
// API calls /ml/predict with 53 features
// ▼
// ML model generates predictions
// ▼
// predictionsProvider updates with results
// ▼
// PredictionsScreen rebuilds with new data
```

### 4. Cache Invalidation Pattern

```dart
// After user updates birth data:
ref.read(kundaliProvider(oldBirthDate).notifier).invalidate();

// This invalidates:
// ├─→ kundaliProvider(oldBirthDate) - clear cache
// ├─→ userKundaliProvider - depends on kundali
// ├─→ predictionsProvider - depends on userKundali
// └─→ UI refetches all data

// Manual invalidation:
ref.invalidate(kundaliProvider);  // All family variations
ref.invalidate(predictionsProvider);
ref.invalidate(userKundaliProvider);
```

---

## ML Predictions Flow

### 1. Trigger Prediction Generation

```dart
// Automatic trigger when userKundaliProvider resolves:
final predictionsProvider = FutureProvider<List<Prediction>>((ref) async {
  final kundali = await ref.watch(userKundaliProvider.future);
  final apiService = ref.watch(apiServiceProvider);

  // Extract 53 ML features from kundali
  final features = _extractMLFeatures(kundali);

  // Send to backend for prediction
  return apiService.getPredictions(kundali);
});
```

### 2. Backend Prediction Flow

```
Backend (/ml/predict endpoint)
  │
  ├─→ Receive 53 astrological features
  │   ├─→ Birth details (9 features)
  │   ├─→ Ascendant (6 features)
  │   ├─→ Planets (72 features)
  │   ├─→ Houses (48 features)
  │   ├─→ Aspects (10-15 features)
  │   ├─→ Yogas (3 features)
  │   └─→ Special (7 features)
  │
  ├─→ Load XGBoost models (8 models for 8 life dimensions)
  │   ├─→ Career predictions
  │   ├─→ Relationships predictions
  │   ├─→ Health predictions
  │   ├─→ Finance predictions
  │   ├─→ Education predictions
  │   ├─→ Family predictions
  │   ├─→ Travel predictions
  │   └─→ Spirituality predictions
  │
  ├─→ Generate predictions with confidence scores
  │   └─→ Each dimension: prediction + confidence (0-1)
  │
  └─→ Return: List[Prediction]
      └─→ With timestamps and interpretation
```

### 3. UI Consumes Predictions

```dart
// PredictionsScreen watches predictionsProvider
final predictions = ref.watch(predictionsProvider);

predictions.when(
  data: (list) {
    // Display all 8 dimension predictions
    // Each prediction shows:
    // ├─→ Title (e.g., "Career Outlook")
    // ├─→ Prediction text
    // ├─→ Confidence score (visual indicator)
    // └─→ Time period
  },
  loading: () => PredictionSkeleton(),
  error: (error, stack) => PredictionError(error),
);
```

---

## Chart Selection & Display Flow

### 1. User Selects Divisional Chart

```dart
// UI Providers track selection
final selectedChartProvider = StateProvider<ChartType>((ref) => ChartType.d1);

// User taps chart option
ref.read(selectedChartProvider.notifier).state = ChartType.d9;
```

### 2. Chart Data Fetched

```dart
// chartProvider depends on userKundaliProvider + selected chart
final chartProvider = FutureProvider<Chart>((ref) async {
  final chart = ref.watch(selectedChartProvider);
  final kundali = await ref.watch(userKundaliProvider.future);

  return kundali.getChart(chart);
});

// Available charts:
// ├─→ D1 (Rasi) - Main birth chart
// ├─→ D2 (Hora) - Wealth/Finances
// ├─→ D7 (Saptamsha) - Children/Fertility
// └─→ D9 (Navamsha) - Spouse/Destiny
```

### 3. Chart Renders

```
ChartDisplayWidget
  │
  └─→ ref.watch(chartProvider)
      │
      ├─→ Render ascendant circle
      │   └─→ 12 zodiac signs arranged in circle
      │
      ├─→ Plot planetary positions
      │   ├─→ 9 planets with their icons
      │   ├─→ Color coding by planet
      │   └─→ Position labels (degree, sign, house)
      │
      ├─→ Highlight aspects
      │   ├─→ Conjunction (0°)
      │   ├─→ Sextile (60°)
      │   ├─→ Square (90°)
      │   ├─→ Trine (120°)
      │   └─→ Opposition (180°)
      │
      └─→ Show house cusp lines
          └─→ 12 house divisions
```

---

## Error Handling Flow

### 1. API Error Caught

```dart
final kundaliProvider = FutureProvider<Kundali>((ref, birthDate) async {
  try {
    return await apiService.generateKundali(birthDate);
  } catch (e) {
    // Error automatically captured by FutureProvider
    rethrow;
  }
});
```

### 2. Error Flows to UI

```
API Error (e.g., ValidationError)
  │
  ├─→ FutureProvider catches error
  │   └─→ AsyncValue.error state
  │
  ├─→ All listeners notified
  │   ├─→ dependent providers also error
  │   └─→ UI gets error state
  │
  └─→ UI displays error
      ├─→ Network error → "Check internet connection"
      ├─→ Invalid birth data → "Please verify birth details"
      ├─→ Server error → "Please try again later"
      └─→ Retry button available
```

### 3. Error Recovery

```dart
// User corrects birth data and retries
ref.refresh(kundaliProvider('1990-05-15'));

// OR invalidate to force refetch
ref.invalidate(kundaliProvider);

// This:
// ├─→ Clears cached error
// ├─→ Fetches fresh data
// ├─→ Updates UI if successful
// └─→ Shows new error if still failing
```

---

## Optimization: Select Pattern

### Problem Without Select

```dart
// Without select - rebuilds on ANY authState change
final isAuthenticated = ref.watch(authProvider).isAuthenticated;

// User logs in:
// ├─→ authState changes
// ├─→ ALL listeners rebuild (even if they only care about isAuthenticated)
// └─→ Performance impact for complex widgets
```

### Solution With Select

```dart
// With select - only rebuilds if isAuthenticated changes
final isAuthenticatedProvider = Provider<bool>((ref) {
  return ref.watch(authProvider.select((state) => state.isAuthenticated));
});

// User updates profile name:
// ├─→ authState.name changes
// ├─→ isAuthenticatedProvider.select() returns same value
// └─→ No rebuild! (Performance improvement)

// User logs in:
// ├─→ authState.isAuthenticated changes
// ├─→ select() returns different value
// └─→ Rebuild happens (correct behavior)
```

---

## Real-Time Updates Flow (Stream)

### Predictions Stream Example

```dart
// StreamProvider for real-time predictions
final predictionsStreamProvider = StreamProvider<List<Prediction>>((ref) {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.watchPredictions();  // WebSocket stream
});

// Data flow:
Backend WebSocket
  │
  └─→ Emits Prediction updates
      │
      ├─→ StreamProvider receives
      │   └─→ AsyncValue<List<Prediction>>
      │
      ├─→ All listeners notified
      │   ├─→ PredictionsScreen rebuilds
      │   └─→ Related widgets update
      │
      └─→ Old prediction replaced with new
          └─→ Smooth animation transition
```

---

## Caching Strategy

### FutureProvider Caching

```dart
// First call - executes API request
final kundali1 = ref.watch(kundaliProvider('1990-05-15'));

// Second call with same parameter - returns cached value
final kundali2 = ref.watch(kundaliProvider('1990-05-15'));

// Cache duration: Until invalidated or provider goes out of scope
ref.invalidate(kundaliProvider);  // Clear ALL cache entries

ref.invalidate(kundaliProvider('1990-05-15'));  // Clear specific
```

### Why Cache is Critical

```
Without Cache:
├─→ Switch screens → kundaliProvider fetches again
├─→ Navigate back → kundaliProvider fetches again
├─→ Performance: 3+ second delays
└─→ User experience: Flickering, loading spinners

With Cache:
├─→ Switch screens → kundaliProvider returns cached
├─→ Navigate back → kundaliProvider returns cached
├─→ Performance: Instant (< 50ms)
└─→ User experience: Smooth, responsive app
```

---

## State Mutation Patterns

### Pattern 1: Immutable Updates (StateNotifier)

```dart
// WRONG - Direct mutation
state.user?.name = newName;

// RIGHT - Create new state with copyWith
state = state.copyWith(user: state.user!.copyWith(name: newName));

// Why: Riverpod only detects state changes if reference changes
// ├─→ Direct mutation = same reference = no notification
// ├─→ copyWith = new object = reference change = notification
// └─→ All listeners properly notified of change
```

### Pattern 2: Batch Mutations

```dart
// If multiple updates needed:
void updateProfile(String name, String email) {
  state = state.copyWith(
    user: state.user?.copyWith(
      name: name,
      email: email,
    ),
  );

  // Result: Single rebuild, not two
  // ├─→ More efficient
  // └─→ Consistent state
}
```

---

## Complete End-to-End Flow Example: Generate Kundali

```
1. User opens app
   └─→ authProvider checks SecureStorage
       └─→ If token exists → restore AuthState (authenticated)

2. User navigates to Kundali generation
   └─→ KundaliGenerationScreen loads

3. User enters birth details and submits
   └─→ ref.read(kundaliProvider(birthDate).notifier).generate()
       │
       ├─→ UI shows loading spinner
       │   └─→ kundaliProvider state: AsyncValue.loading
       │
       └─→ ApiClient sends request to /kundali/generate_kundali
           │
           └─→ Backend processes (3-5 seconds)
               │
               ├─→ SwissEphemeris calculates planetary positions
               ├─→ House system creates divisions
               ├─→ Dasha system calculates periods
               ├─→ Shad Bala computes strengths
               ├─→ ML models extract 53 features
               └─→ Response: Complete Kundali object

4. kundaliProvider receives response
   └─→ Cache Kundali data
       └─→ Notify all listeners

5. Dependent providers cascade
   ├─→ userKundaliProvider resolves
   │   └─→ predictionsProvider starts fetching
   │
   └─→ ChartDisplayWidget renders
       ├─→ Shows D1 Rasi chart
       ├─→ Displays planetary positions
       └─→ Shows house divisions

6. predictionsProvider resolves
   ├─→ XGBoost models predict 8 dimensions
   │
   └─→ PredictionsScreen renders
       ├─→ Career predictions
       ├─→ Relationship predictions
       ├─→ Health predictions
       ├─→ Finance predictions
       ├─→ Education predictions
       ├─→ Family predictions
       ├─→ Travel predictions
       └─→ Spirituality predictions

7. User navigates to different chart (D9)
   ├─→ selectedChartProvider changes
   │
   └─→ chartProvider re-fetches with new param
       ├─→ Data already in kundali
       ├─→ Extract D9 divisional chart
       └─→ Render Navamsha chart

8. User logs out
   ├─→ ref.read(authProvider.notifier).logout()
   │
   ├─→ Clear token from SecureStorage
   │
   ├─→ Invalidate all user-specific providers
   │   ├─→ kundaliProvider cleared
   │   ├─→ predictionsProvider cleared
   │   └─→ userKundaliProvider cleared
   │
   └─→ AuthState updated
       └─→ UI redirects to login
```

---

## Performance Optimization Tips

✅ **DO:**
- Use `.select()` to listen to specific parts of state
- Cache expensive computations with FutureProvider
- Invalidate only what changed, not everything
- Use `.family` for parameterized data
- Group related mutations in StateNotifier methods

❌ **AVOID:**
- Watching entire objects when only 1 field needed
- Recreating providers on every widget build
- Invalidating too aggressively (clears beneficial cache)
- Deep nesting of dependent providers (hard to debug)
- Synchronous operations in async providers

---

## Debugging Data Flow

### Check Provider State

```dart
// In DevTools or debug prints
final state = ref.watch(authProvider);
print('Auth state: $state');  // See current state

final isLoading = ref.watch(kundaliProvider('1990-05-15'));
print('Kundali loading: ${isLoading.isLoading}');  // Check async state
```

### Track Listener Notifications

```dart
// Listen to provider changes
ref.listen(authProvider, (previous, next) {
  print('Auth changed from $previous to $next');
  // Useful for logging, analytics, side effects
});
```

### Use DevTools

- Riverpod extension shows all providers
- See provider dependencies
- Watch state changes in real-time
- Trace which listeners rebuild when

---

**Next:** See [data-models.md](data-models.md) for complete data structure definitions
**Related:** See [state-patterns.md](state-patterns.md) for implementation patterns
