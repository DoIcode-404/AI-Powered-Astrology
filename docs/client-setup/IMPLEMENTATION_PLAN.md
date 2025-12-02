# Riverpod Authentication Implementation Plan

## Executive Summary

This document provides a complete implementation plan for integrating Riverpod 2.x state management into the Flutter astrology app's authentication system. The architecture has been designed following Riverpod best practices with a focus on performance, testability, and maintainability.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      UI Layer (Flutter)                      │
│  ├─ LoginScreen (ConsumerWidget)                             │
│  ├─ SignupScreen (ConsumerWidget)                            │
│  ├─ ProfileScreen (ConsumerWidget)                           │
│  └─ AppShell (Root Navigation)                               │
└────────────────────┬────────────────────────────────────────┘
                     │ ref.watch() / ref.read()
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Riverpod Provider Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ StateNotifierProvider: authProvider                  │   │
│  │ - Main state: AuthState (sealed class)               │   │
│  │ - Notifier: AuthNotifier (business logic)            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Derived Providers (Computed Values):                        │
│  ├─ isAuthenticatedProvider      (bool)                      │
│  ├─ isAuthLoadingProvider         (bool)                     │
│  ├─ currentUserProvider           (UserData?)               │
│  ├─ accessTokenProvider           (String?)                 │
│  ├─ authErrorProvider             (String?)                 │
│  ├─ tokenExpiryProvider           (TokenExpiryInfo?)        │
│  ├─ isSessionExpiringProvider     (bool)                    │
│  └─ sessionWarningProvider        (SessionWarningInfo?)     │
└────────────────────┬────────────────────────────────────────┘
                     │ calls methods
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Business Logic Layer (Notifier)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ AuthNotifier extends StateNotifier<AuthState>        │   │
│  │ - login(email, password)                             │   │
│  │ - signup(email, password, name, phone?)              │   │
│  │ - logout()                                           │   │
│  │ - refreshAccessToken()                               │   │
│  │ - Token refresh scheduling (automatic)               │   │
│  │ - Session warning scheduling (automatic)             │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ calls methods
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Service Layer (API & Storage)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ AuthService                                          │   │
│  │ - Singleton pattern for consistency                  │   │
│  │ - login() -> API call via ApiClient                  │   │
│  │ - signup() -> API call via ApiClient                 │   │
│  │ - refreshAccessToken() -> API call via ApiClient     │   │
│  │ - logout() -> API call via ApiClient (optional)      │   │
│  │ - Token storage -> SharedPreferences                 │   │
│  │ - User data storage -> SharedPreferences             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ ApiClient (HTTP layer)                               │   │
│  │ - JWT token injection via interceptor                │   │
│  │ - Error handling and transformation                  │   │
│  │ - Token refresh retry logic                          │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ uses
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Layer (Models & Storage)                   │
│  ├─ auth_models.dart                                        │
│  │  ├─ LoginRequest / SignupRequest                        │
│  │  ├─ AuthResponse / TokenResponse                        │
│  │  ├─ UserData                                            │
│  │  └─ Exception classes (AuthException, etc.)             │
│  └─ SharedPreferences                                       │
└─────────────────────────────────────────────────────────────┘
```

## Files Created

### 1. Immutable State Classes
**File**: `client/lib/presentation/providers/auth_state.dart`

Defines all possible authentication states using sealed classes:
- `AuthStateInitial` - Initial state before auth check
- `AuthStateLoading` - Async operation in progress
- `AuthStateUnauthenticated` - Not logged in (with optional error)
- `AuthStateAuthenticated` - Logged in with valid tokens
- `AuthStateSessionExpiring` - Warning state for token expiry

**Key Features**:
- Immutable value objects
- Type-safe pattern matching with sealed classes
- Helper methods for token validation and time calculations
- `copyWith()` method for state updates

### 2. Riverpod Providers
**File**: `client/lib/presentation/providers/auth_provider.dart`

Defines all providers for authentication:
- `authServiceProvider` - Dependency injection for AuthService
- `authProvider` - Main StateNotifierProvider (auth state + notifier)
- Derived providers for computed values (see section below)

**Key Features**:
- Single source of truth (authProvider)
- Derived providers prevent unnecessary rebuilds
- Full type safety
- Well-documented with usage examples

### 3. Business Logic (StateNotifier)
**File**: `client/lib/presentation/notifiers/auth_notifier.dart`

Implements business logic for authentication:
- `login()` - Authenticate with email/password
- `signup()` - Create new account
- `logout()` - Clear session
- `refreshAccessToken()` - Get new token before expiry
- Token refresh scheduling (automatic, triggers at 5 min before expiry)
- Session warning scheduling (warns at 2 min before expiry)

**Key Features**:
- Automatic token refresh before expiry
- Session expiry warnings
- Proper error handling and state transitions
- Resource cleanup (timer cancellation)
- Rethrow pattern for error handling in UI

## State Architecture Details

### Auth State Hierarchy
```
AuthState (abstract)
├── AuthStateInitial
├── AuthStateLoading (loading with optional message)
├── AuthStateUnauthenticated (error optional)
├── AuthStateAuthenticated
│   └── AuthStateSessionExpiring (extends Authenticated)
```

### State Transition Diagram

```
┌─────────────┐
│  Initial    │
└──────┬──────┘
       │ _checkAuthStatus()
       │
       ├──→ Valid token → Authenticated
       │
       └──→ No/invalid token → Unauthenticated


Unauthenticated
       │
       ├─ login() ──→ Loading ──→ Authenticated ✓
       │                       └──→ Unauthenticated (error)
       │
       └─ signup() ─→ Loading ──→ Authenticated ✓
                               └──→ Unauthenticated (error)


Authenticated
       │
       ├─ [Auto-refresh at 5 min before expiry] ──→ Token updated (silent)
       │
       ├─ [Warning at 2 min before expiry] ────────→ SessionExpiring
       │                                              │
       │                                              ├─ User extends → refreshAccessToken()
       │                                              │
       │                                              └─ Wait for expiry → logout()
       │
       └─ logout() ──→ Loading ──→ Unauthenticated
```

## Derived Providers (Performance Optimization)

The architecture includes several derived providers that compute values from the main auth state. This prevents unnecessary rebuilds.

```dart
// Instead of watching entire authState:
final authState = ref.watch(authProvider);  // Rebuilds on ANY auth state change
final isAuth = authState is AuthStateAuthenticated;

// Use derived provider:
final isAuth = ref.watch(isAuthenticatedProvider);  // Rebuilds only when auth status changes
```

### Complete List of Derived Providers

| Provider | Returns | Rebuilds When | Use Case |
|----------|---------|---------------|----------|
| `isAuthenticatedProvider` | `bool` | Auth status changes | Navigation guards, conditional UI |
| `isAuthLoadingProvider` | `bool` | Loading state changes | Loading spinners, button disabling |
| `currentUserProvider` | `UserData?` | User data changes | User profile, user info display |
| `authErrorProvider` | `String?` | Error changes | Error messages, error handling |
| `accessTokenProvider` | `String?` | Token changes | API calls, token validation |
| `tokenExpiryProvider` | `TokenExpiryInfo?` | Token expiry changes | Session info, expiry display |
| `isSessionExpiringProvider` | `bool` | Session warning state | Show/hide warning UI |
| `sessionWarningProvider` | `SessionWarningInfo?` | Session warning state | Detailed warning info |

## Integration Points

### For API Data Architect

The AuthService expects the following API client methods to be implemented:

```dart
// In AuthService
Future<AuthResponse> login({
  required String email,
  required String password,
}) async {
  // TODO: Implement
  // POST /auth/login with LoginRequest
  // Return: AuthResponse (with user, tokens, expires_in)
}

Future<AuthResponse> signup({
  required String email,
  required String password,
  required String name,
  String? phone,
}) async {
  // TODO: Implement
  // POST /auth/register with SignupRequest
  // Return: AuthResponse (with user, tokens, expires_in)
}

Future<TokenResponse> refreshAccessToken() async {
  // TODO: Implement
  // POST /auth/refresh with RefreshTokenRequest
  // Return: TokenResponse (with new tokens, expires_in)
}

Future<void> logout() async {
  // TODO: Implement (optional)
  // POST /auth/logout
  // Or simply clear local tokens if backend doesn't need it
}
```

**Important**: AuthService internally calls `_storeAuthData()` after successful login/signup. This method stores tokens and user data in SharedPreferences.

### For Flutter UI Developer

Replace all StatefulWidget authentication screens with ConsumerWidget implementations.

**Basic Pattern**:
```dart
class LoginScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch providers for reactive updates
    final authState = ref.watch(authProvider);
    final isLoading = ref.watch(isAuthLoadingProvider);
    final error = ref.watch(authErrorProvider);

    // Get notifier for user actions
    final authNotifier = ref.read(authProvider.notifier);

    // Build UI based on state
    return Scaffold(
      // ... UI code ...
    );
  }
}
```

**See**: `RIVERPOD_UI_EXAMPLES.md` for complete, production-ready screen implementations.

## Token Management Strategy

### Automatic Token Refresh
- **When**: Triggered automatically when 5 minutes or less remain on token expiry
- **How**: AuthNotifier schedules a Timer that calls `refreshAccessToken()`
- **Result**: Tokens updated silently, UI unaffected
- **Failure**: If refresh fails, user is automatically logged out

### Session Expiry Warning
- **When**: Shown when 2 minutes or less remain
- **How**: AuthNotifier transitions state to `AuthStateSessionExpiring`
- **UI**: Dialog/banner shown to user
- **Options**: User can refresh (extends session) or logout

### Storage
- **Location**: SharedPreferences (via AuthService)
- **Data Stored**:
  - `access_token` - JWT token for API calls
  - `refresh_token` - Token for refreshing access token
  - `token_expiry` - Absolute expiry time in seconds
  - `user_data` - Current user info (JSON encoded)

### Expiry Time Calculation
```
API Response: expires_in = 3600 (seconds)
Stored Expiry: DateTime.now() + Duration(seconds: 3600)

Token is considered expired if: DateTime.now().isAfter(expiryTime)
Token should be refreshed if: timeRemaining.inMinutes < 5
```

## Error Handling Strategy

### Error Types
1. **AuthException** - Base auth exception with message and status code
2. **TokenExpiredException** - Token has expired (401)
3. **InvalidTokenException** - Token is malformed/invalid (401)
4. **UnauthorizedException** - Invalid credentials (401)
5. **NetworkException** - Network error occurred

### Error Flow
```
API Error
  ↓
ApiClient._ErrorInterceptor converts to AuthException
  ↓
AuthService.login/signup/refresh() catches and rethrows
  ↓
AuthNotifier.login/signup/refresh() catches
  ↓
AuthNotifier sets AuthStateUnauthenticated(errorMessage: ...)
  ↓
UI watches authErrorProvider and displays message
```

### Error Handling in UI
```dart
// Option 1: Automatic (Recommended)
final error = ref.watch(authErrorProvider);
if (error != null) {
  // Show error message
}

// Option 2: Manual with try-catch
try {
  await ref.read(authProvider.notifier).login(...);
} on AuthException catch (e) {
  // Handle specific error
}

// Option 3: Retry after error
await ref.read(authProvider.notifier).retryLogin(email: '...', password: '...');
```

## Performance Optimizations

### 1. Select Pattern (Implicit)
All derived providers use implicit select pattern to prevent unnecessary rebuilds.

```dart
// Before (inefficient - rebuilds on ANY auth change)
final authState = ref.watch(authProvider);
if (authState is AuthStateAuthenticated) {
  // Show user name
}

// After (efficient - rebuilds only on user change)
final user = ref.watch(currentUserProvider);
if (user != null) {
  // Show user name
}
```

### 2. Pattern Matching Efficiency
Dart's pattern matching is optimized at compile time, making switch expressions efficient.

```dart
return switch (authState) {
  AuthStateAuthenticated(:final user) => UserWidget(user),
  _ => LoginWidget(),
};
```

### 3. Sealed Classes
Sealed classes provide exhaustiveness checking at compile time, ensuring all cases are handled.

### 4. Timer Management
- Only one refresh timer active at a time
- Timers cancelled on state changes
- No memory leaks - proper cleanup on dispose

## Testing Strategy

### Unit Tests (AuthNotifier)
```dart
test('login transitions from Unauthenticated to Loading to Authenticated', () async {
  final container = ProviderContainer(
    overrides: [
      authServiceProvider.overrideWithValue(MockAuthService()),
    ],
  );

  final notifier = container.read(authProvider.notifier);

  // Initial state
  expect(container.read(authProvider), isA<AuthStateUnauthenticated>());

  // Trigger login
  await notifier.login(email: 'test@test.com', password: 'password');

  // Check authenticated state
  expect(container.read(authProvider), isA<AuthStateAuthenticated>());
});
```

### Widget Tests
```dart
testWidgets('LoginScreen shows error when login fails', (tester) async {
  final container = ProviderContainer(
    overrides: [
      authServiceProvider.overrideWithValue(MockAuthServiceWithError()),
    ],
  );

  await tester.pumpWidget(
    UncontrolledProviderScope(
      container: container,
      child: MaterialApp(home: LoginScreen()),
    ),
  );

  // Find and tap login button
  await tester.tap(find.byType(ElevatedButton));
  await tester.pumpAndSettle();

  // Verify error message displayed
  expect(find.text('Invalid credentials'), findsOneWidget);
});
```

### Integration Tests
Test full user journeys with real Riverpod container.

## Migration Checklist

For each auth-related screen:

- [ ] Change from `StatefulWidget` to `ConsumerWidget`
- [ ] Replace `setState()` with `ref.watch(provider)`
- [ ] Replace `_authService` calls with `ref.read(authProvider.notifier).method()`
- [ ] Remove manual loading/error state management
- [ ] Remove manual token refresh logic
- [ ] Update error handling to use `authErrorProvider`
- [ ] Test state transitions
- [ ] Test error scenarios
- [ ] Verify no unnecessary rebuilds (profile with DevTools)

## Phase Implementation Timeline

### Phase 1: Setup (Current)
- [x] Design state architecture (sealed classes)
- [x] Create Riverpod providers
- [x] Implement AuthNotifier
- [x] Create derived providers
- [ ] Update pubspec.yaml with Riverpod dependencies (if needed)

### Phase 2: API Integration (API Data Architect)
- [ ] Implement AuthService.login() - API call
- [ ] Implement AuthService.signup() - API call
- [ ] Implement AuthService.refreshAccessToken() - API call
- [ ] Implement AuthService.logout() - API call (optional)
- [ ] Test with backend
- [ ] Handle API-specific errors

### Phase 3: UI Implementation (Flutter UI Developer)
- [ ] Create LoginScreen (ConsumerWidget)
- [ ] Create SignupScreen (ConsumerWidget)
- [ ] Update existing screens to use providers
- [ ] Implement root navigation (AppShell) with auth switching
- [ ] Add session warning UI
- [ ] Test all state transitions
- [ ] Profile and optimize rebuilds

### Phase 4: Testing & Deployment
- [ ] Unit tests for AuthNotifier
- [ ] Widget tests for screens
- [ ] Integration tests for full flow
- [ ] Manual testing on devices
- [ ] Performance profiling
- [ ] Production deployment

## Dependency Management

### Required Dependencies (Add to pubspec.yaml)
```yaml
dependencies:
  flutter_riverpod: ^2.5.0  # State management
  riverpod: ^2.5.0          # Core Riverpod
```

### Already Available
- `shared_preferences: ^2.2.2` - Token storage
- `dio: ^5.4.0` - HTTP client
- `flutter` - UI framework

## Common Pitfalls & Solutions

### Pitfall 1: Over-watching auth state
```dart
// WRONG - Rebuilds on any auth change
final authState = ref.watch(authProvider);
final user = authState is AuthStateAuthenticated ? authState.user : null;

// RIGHT - Rebuilds only on user change
final user = ref.watch(currentUserProvider);
```

### Pitfall 2: Forgetting to handle Authenticated state in switch
```dart
// WRONG - Missing AuthStateSessionExpiring
return switch (authState) {
  AuthStateInitial() => Splash(),
  AuthStateAuthenticated() => Home(),  // Missing SessionExpiring case!
  _ => Login(),
};

// RIGHT - All cases covered
return switch (authState) {
  AuthStateInitial() => Splash(),
  AuthStateAuthenticated() => Home(),
  AuthStateSessionExpiring() => SessionWarning(),
  _ => Login(),
};
```

### Pitfall 3: Manual token refresh in UI
```dart
// WRONG - UI manages token refresh
if (token.shouldRefresh) {
  await refreshToken();
}

// RIGHT - AuthNotifier handles it automatically
// UI just watches token state
final token = ref.watch(tokenExpiryProvider);
```

### Pitfall 4: Not cleaning up timers
```dart
// WRONG - Timers leak memory
Timer.periodic(Duration(minutes: 1), (_) => refreshToken());

// RIGHT - TimerNotifier properly cancels
_tokenRefreshTimer?.cancel();
_tokenRefreshTimer = null;
```

## Monitoring & Debugging

### Using Riverpod DevTools
```dart
// Add to main.dart
void main() {
  runApp(
    ProviderScope(
      observers: [
        RiverpodObserver(), // Logs all provider changes
      ],
      child: MyApp(),
    ),
  );
}
```

### Checking State
```dart
// In debug console
ref.refresh(authProvider);  // Force refresh
container.read(authProvider);  // Read current state
```

### Performance Profiling
Use Flutter DevTools Profiler to:
- Monitor widget rebuild frequency
- Check for unnecessary rebuilds
- Identify expensive operations
- Measure frame times

## Summary

This Riverpod architecture provides:
- **Type Safety**: Sealed classes with pattern matching
- **Performance**: Derived providers prevent unnecessary rebuilds
- **Maintainability**: Clear separation of concerns
- **Testability**: Services are mockable, state is isolated
- **Scalability**: Easy to add new features (additional derived providers)
- **User Experience**: Automatic token refresh, session warnings

The implementation follows Riverpod 2.x best practices and Flutter architecture guidelines.

## Next Steps

1. **API Architect**: Implement AuthService API methods
2. **UI Developer**: Implement ConsumerWidget screens using provided examples
3. **QA**: Test all state transitions and error scenarios
4. **Deploy**: Gradual rollout with monitoring
