# State Management Patterns - Riverpod

**Framework:** Riverpod (Functional Reactive State Management)
**Status:** Architecture Complete
**Last Updated:** November 2025

---

## Overview

This document defines the state management patterns and best practices for the Kundali Astrology Flutter application using Riverpod.

**Why Riverpod?**
- Functional and composable (vs imperative)
- Type-safe state management
- Built-in caching and invalidation
- Testable without complex mocking
- Excellent code generation support
- No BuildContext required

---

## Provider Types & Patterns

### 1. StateNotifier Providers (for mutable state)

Used for states that change over time and need explicit mutations.

```dart
// Define the state class
class AuthState {
  final bool isAuthenticated;
  final String? token;
  final User? user;
  final String? error;

  AuthState({
    required this.isAuthenticated,
    this.token,
    this.user,
    this.error,
  });

  AuthState copyWith({
    bool? isAuthenticated,
    String? token,
    User? user,
    String? error,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      token: token ?? this.token,
      user: user ?? this.user,
      error: error ?? this.error,
    );
  }
}

// Define the StateNotifier
class AuthNotifier extends StateNotifier<AuthState> {
  final AuthService _authService;

  AuthNotifier(this._authService)
      : super(AuthState(isAuthenticated: false));

  Future<void> login(String email, String password) async {
    try {
      final response = await _authService.login(email, password);
      state = state.copyWith(
        isAuthenticated: true,
        token: response.token,
        user: response.user,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  Future<void> logout() async {
    try {
      await _authService.logout();
      state = AuthState(isAuthenticated: false);
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }
}

// Create the provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final authService = ref.watch(authServiceProvider);
  return AuthNotifier(authService);
});
```

**Usage:**
```dart
// In Widget
final authState = ref.watch(authProvider);

// Call notifier methods
ref.read(authProvider.notifier).login(email, password);
```

---

### 2. Future Providers (for async data)

Used for one-time async operations that fetch data.

```dart
// Get Kundali data
final kundaliProvider = FutureProvider.family<Kundali, String>((ref, birthDate) async {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.generateKundali(birthDate);
});

// In Widget
final kundaliAsync = ref.watch(kundaliProvider('1990-05-15'));

kundaliAsync.when(
  data: (kundali) => KundaliChart(kundali: kundali),
  loading: () => LoadingIndicator(),
  error: (error, stack) => ErrorWidget(error: error),
);
```

---

### 3. Stream Providers (for real-time data)

Used for continuous data streams (WebSocket, Firebase, etc.).

```dart
// Watch user predictions stream
final predictionsStreamProvider = StreamProvider<List<Prediction>>((ref) {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.watchPredictions();
});

// In Widget
final predictions = ref.watch(predictionsStreamProvider);

predictions.when(
  data: (list) => PredictionsList(predictions: list),
  loading: () => LoadingIndicator(),
  error: (error, stack) => ErrorWidget(error: error),
);
```

---

### 4. Computed Providers (derived state)

Used for derived or computed state based on other providers.

```dart
// Derive user zodiac sign from birth date
final userZodiacProvider = FutureProvider<String>((ref) async {
  final authState = ref.watch(authProvider);
  if (authState.user?.birthDate == null) return '';

  final service = ref.watch(astroServiceProvider);
  return service.getZodiacSign(authState.user!.birthDate);
});

// Derive chart strength (computed from kundali)
final chartStrengthProvider = FutureProvider<double>((ref) async {
  final kundaliAsync = ref.watch(kundaliProvider(ref.watch(userBirthDateProvider)));

  return kundaliAsync.when(
    data: (kundali) => kundali.chartStrength,
    loading: () => 0.0,
    error: (_, __) => 0.0,
  );
});
```

---

### 5. Select (Performance Optimization)

Use `.select()` to watch only specific parts of state.

```dart
// Only listen to isAuthenticated (not entire authState)
final isAuthenticatedProvider = Provider<bool>((ref) {
  return ref.watch(authProvider.select((state) => state.isAuthenticated));
});

// In Widget - rebuilds only when isAuthenticated changes
final isAuthenticated = ref.watch(isAuthenticatedProvider);
```

---

## Provider Architecture

### Core Providers (Foundation)

```dart
// lib/data/providers/core_providers.dart

// Service providers
final authServiceProvider = Provider((ref) => AuthService());
final apiServiceProvider = Provider((ref) => ApiClient());
final astroServiceProvider = Provider((ref) => AstroService());

// Base state providers
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(authServiceProvider));
});
```

### Feature Providers (Business Logic)

```dart
// lib/data/providers/kundali_providers.dart

// Kundali data
final kundaliProvider = FutureProvider.family<Kundali, String>((ref, birthDate) async {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.generateKundali(birthDate);
});

// User Kundali (from auth user)
final userKundaliProvider = FutureProvider<Kundali>((ref) async {
  final authState = ref.watch(authProvider);
  if (authState.user?.birthDate == null) throw Exception('No birth date');

  return ref.watch(kundaliProvider(authState.user!.birthDate)).value!;
});

// Predictions based on kundali
final predictionsProvider = FutureProvider<List<Prediction>>((ref) async {
  final kundali = await ref.watch(userKundaliProvider.future);
  final apiService = ref.watch(apiServiceProvider);
  return apiService.getPredictions(kundali);
});
```

### UI Providers (Presentation State)

```dart
// lib/presentation/providers/ui_providers.dart

// Loading states
final loadingProvider = StateProvider<bool>((ref) => false);

// Selected chart (D1, D2, D7, D9)
final selectedChartProvider = StateProvider<ChartType>((ref) => ChartType.d1);

// Filter/sort preferences
final predictionsFilterProvider = StateProvider<PredictionFilter>((ref) => PredictionFilter.all);
```

---

## State Management Flow

```
┌─────────────────────────────────────────────────┐
│            Widget (UI Layer)                    │
│         ref.watch(provider)                     │
└────────────────────┬────────────────────────────┘
                     │
┌─────────────────────▼────────────────────────────┐
│         Providers (State Layer)                  │
│  • StateNotifier (Auth, App State)              │
│  • FutureProvider (Async Data)                  │
│  • StreamProvider (Real-time Data)              │
└────────────────────┬────────────────────────────┘
                     │
┌─────────────────────▼────────────────────────────┐
│        Services (Business Logic)                │
│  • AuthService (JWT, login/logout)              │
│  • ApiService (HTTP requests)                   │
│  • AstroService (Calculations)                  │
└────────────────────┬────────────────────────────┘
                     │
┌─────────────────────▼────────────────────────────┐
│      External (Backend, Database)               │
│  • REST API (FastAPI)                           │
│  • MongoDB (User data)                          │
└─────────────────────────────────────────────────┘
```

---

## Key Patterns

### 1. Dependency Injection via Providers

```dart
// Services depend on other services through providers
final databaseProvider = Provider((ref) => Database());

final userRepositoryProvider = Provider((ref) {
  final db = ref.watch(databaseProvider);
  return UserRepository(db);
});

final authServiceProvider = Provider((ref) {
  final userRepo = ref.watch(userRepositoryProvider);
  return AuthService(userRepo);
});
```

### 2. Invalidation & Refresh

```dart
// Refresh a provider
ref.refresh(userKundaliProvider);

// Invalidate a provider (clears cache, fetches again)
ref.invalidate(userKundaliProvider);

// Invalidate multiple related providers
void logout(WidgetRef ref) {
  ref.invalidate(authProvider);
  ref.invalidate(userKundaliProvider);
  ref.invalidate(predictionsProvider);
}
```

### 3. Error Handling

```dart
final dataProvider = FutureProvider<Data>((ref) async {
  try {
    return await fetchData();
  } catch (e) {
    // Log error
    logError(e);
    // Re-throw for UI to handle
    rethrow;
  }
});

// In Widget
final asyncData = ref.watch(dataProvider);

asyncData.when(
  data: (data) => DisplayData(data),
  loading: () => LoadingWidget(),
  error: (error, stack) {
    // Handle different error types
    if (error is NetworkException) {
      return ErrorWidget('No internet connection');
    }
    return ErrorWidget('An error occurred');
  },
);
```

### 4. Family Modifiers (Parameters)

```dart
// Provider with parameters
final chartProvider = FutureProvider.family<Chart, String>((ref, chartType) async {
  final kundali = await ref.watch(userKundaliProvider.future);
  return kundali.getChart(chartType);
});

// Usage with different parameters
final d1Chart = ref.watch(chartProvider('D1'));
final d9Chart = ref.watch(chartProvider('D9'));
```

---

## Testing State

```dart
test('Auth provider login updates state', () async {
  final container = ProviderContainer();

  await container.read(authProvider.notifier).login('test@test.com', 'password');

  final authState = container.read(authProvider);
  expect(authState.isAuthenticated, true);
  expect(authState.user, isNotNull);
});
```

---

## Anti-Patterns to Avoid

❌ **DO NOT** - Watch providers in provider initializationUnless using `ref.watch()`

❌ **DO NOT** - Modify state directly (use StateNotifier)
```dart
// WRONG
state.user = newUser;

// RIGHT
state = state.copyWith(user: newUser);
```

❌ **DO NOT** - Create providers inside widgets
```dart
// WRONG
final myProvider = Provider((ref) => ...); // Don't do this in widgets!

// RIGHT
// Define at module level
final myProvider = Provider((ref) => ...);
```

❌ **DO NOT** - Forget to invalidate cached data after mutations
```dart
// WRONG
await updateUser(user); // Cache stale!

// RIGHT
await updateUser(user);
ref.invalidate(userProvider);
```

---

## Best Practices

✅ **DO** - Keep providers focused on single responsibility
✅ **DO** - Use `.family` for parameterized providers
✅ **DO** - Use `.select()` to optimize rebuilds
✅ **DO** - Invalidate related caches after mutations
✅ **DO** - Handle loading and error states in UI
✅ **DO** - Test providers independently

---

## Provider Organization

```
lib/
├── data/
│   └── providers/
│       ├── core_providers.dart        # Services
│       ├── auth_providers.dart        # Auth state
│       ├── kundali_providers.dart     # Kundali data
│       └── predictions_providers.dart # Predictions
│
└── presentation/
    └── providers/
        ├── ui_providers.dart          # UI state
        └── filter_providers.dart      # Filter state
```

---

**Next:** See [data-flow.md](data-flow.md) for state flow diagrams
**Related:** See [data-models.md](data-models.md) for data structures
