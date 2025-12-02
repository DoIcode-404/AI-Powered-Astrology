# Riverpod 2.x Authentication State Management Architecture

## Overview

This document describes the complete Riverpod state management architecture for authentication in the Flutter astrology app. The architecture follows Riverpod 2.x best practices with immutable state, proper scoping, reactive updates, and performance optimizations.

## Architecture Principles

1. **Immutability First**: All state classes are immutable using sealed classes
2. **Separation of Concerns**: Clear boundaries between state, notifier, service, and UI
3. **Single Source of Truth**: One authoritative provider for each piece of data
4. **Explicit Async States**: Loading and error states for all operations
5. **Performance Optimized**: Select patterns prevent unnecessary rebuilds
6. **Type Safe**: Full type safety with Dart's type system
7. **Testable**: Dependencies are injectable and mockable

## Directory Structure

```
lib/
├── presentation/
│   ├── providers/
│   │   ├── auth_provider.dart          # Main Riverpod providers (StateNotifier + derived)
│   │   ├── auth_state.dart             # Immutable auth state classes
│   │   └── index.dart                  # Barrel export
│   ├── notifiers/
│   │   └── auth_notifier.dart          # StateNotifier with business logic
│   └── screens/
│       └── auth/
│           ├── login_screen.dart       # UI layer (consumes auth providers)
│           └── signup_screen.dart      # UI layer (consumes auth providers)
└── data/
    ├── services/
    │   └── auth_service.dart           # Service layer (API calls, token storage)
    └── models/
        └── auth_models.dart            # Request/Response/Exception models
```

## State Design

### Auth State Hierarchy

```
AuthState (abstract base)
├── AuthStateInitial           # App startup, checking auth status
├── AuthStateLoading           # Operation in progress (login, signup, logout)
├── AuthStateUnauthenticated   # User not logged in (with optional error)
├── AuthStateAuthenticated     # User logged in with valid tokens
└── AuthStateSessionExpiring   # (extends Authenticated) Warning user about expiry
```

### State Structure

```dart
// Initial state - no operation yet
AuthStateInitial()

// Loading state
AuthStateLoading(message: 'Logging in...')

// Unauthenticated with optional error
AuthStateUnauthenticated(
  errorMessage: 'Invalid credentials',
  statusCode: 401
)

// Fully authenticated
AuthStateAuthenticated(
  user: UserData(...),
  accessToken: 'eyJhbGc...',
  refreshToken: 'eyJhbGc...',
  expiresIn: 3600,
  expiryTime: DateTime(...) // Absolute expiry time
)

// Session expiring warning
AuthStateSessionExpiring(
  user: UserData(...),
  // ... same as AuthStateAuthenticated ...
  timeRemaining: Duration(minutes: 1, seconds: 30)
)
```

## Provider Design

### 1. Core Providers

#### authServiceProvider
```dart
final authServiceProvider = Provider<AuthService>((ref) {
  return AuthService();
});
```
- **Purpose**: Provides singleton AuthService for dependency injection
- **Type**: Provider
- **Scope**: Application-wide
- **Usage**: Injected into AuthNotifier, used for API calls and token storage

#### authProvider (StateNotifierProvider)
```dart
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final authService = ref.watch(authServiceProvider);
  return AuthNotifier(authService);
});
```
- **Purpose**: Main state management provider
- **Type**: StateNotifierProvider
- **Scope**: Application-wide
- **State**: AuthState (sealed class)
- **Notifier**: AuthNotifier (handles business logic)
- **Methods Available**:
  - `login(email, password)` - Authenticate user
  - `signup(email, password, name, phone?)` - Create new account
  - `logout()` - Clear session
  - `refreshAccessToken()` - Get new token before expiry
  - `retryLogin/retrySignup()` - Retry after error
  - `clearError()` - Dismiss error message

### 2. Derived Providers (Computed State)

These providers compute derived values from the main auth state. They use implicit `.select()` pattern to prevent unnecessary rebuilds.

#### isAuthenticatedProvider
```dart
final isAuthenticatedProvider = Provider<bool>((ref) {
  return ref.watch(authProvider) is AuthStateAuthenticated;
});
```
- **Returns**: `bool` - true if user is logged in
- **Performance**: Rebuilds only when auth state changes
- **Use Case**: Navigation, permission checks

#### currentUserProvider
```dart
final currentUserProvider = Provider<UserData?>((ref) {
  final authState = ref.watch(authProvider);
  if (authState is AuthStateAuthenticated) {
    return authState.user;
  }
  return null;
});
```
- **Returns**: `UserData?` - current user or null
- **Performance**: Rebuilds only when user data changes
- **Use Case**: Displaying user info, user-specific features

#### accessTokenProvider
```dart
final accessTokenProvider = Provider<String?>((ref) {
  final authState = ref.watch(authProvider);
  if (authState is AuthStateAuthenticated) {
    return authState.accessToken;
  }
  return null;
});
```
- **Returns**: `String?` - current access token or null
- **Performance**: Only rebuilds when token changes
- **Use Case**: API requests, token validation

#### authErrorProvider
```dart
final authErrorProvider = Provider<String?>((ref) {
  final authState = ref.watch(authProvider);
  if (authState is AuthStateUnauthenticated) {
    return authState.errorMessage;
  }
  return null;
});
```
- **Returns**: `String?` - error message or null
- **Performance**: Only rebuilds on error changes
- **Use Case**: Error display, error handling

#### tokenExpiryProvider
```dart
final tokenExpiryProvider = Provider<TokenExpiryInfo?>((ref) {
  // Returns TokenExpiryInfo with:
  // - expiryTime: DateTime
  // - timeRemaining: Duration
  // - shouldRefresh: bool
  // - isExpired: bool
});
```
- **Returns**: `TokenExpiryInfo?` - token expiry details
- **Performance**: Rebuilds when token changes
- **Use Case**: Session management, token refresh scheduling

#### isSessionExpiringProvider
```dart
final isSessionExpiringProvider = Provider<bool>((ref) {
  // true if session warning shown or <= 2 minutes remain
});
```
- **Returns**: `bool` - true if session expiring warning should show
- **Performance**: Rebuilds on timeout changes
- **Use Case**: Session warning UI

#### sessionWarningProvider
```dart
final sessionWarningProvider = Provider<SessionWarningInfo?>((ref) {
  // Returns SessionWarningInfo with:
  // - minutesRemaining: int
  // - secondsRemaining: int
  // - expiryTime: DateTime
});
```
- **Returns**: `SessionWarningInfo?` - session warning details
- **Performance**: Rebuilds when session state changes
- **Use Case**: Detailed session expiry warnings

## State Transitions

### Login Flow
```
Initial
  ↓
checkAuthStatus() [automatic on app start]
  ├─→ Has valid token → Authenticated
  └─→ No valid token → Unauthenticated
  ↓
User taps "Login"
  ↓
login(email, password)
  ↓
Loading
  ├─→ Success → Authenticated (with user, tokens, expiry)
  └─→ Error → Unauthenticated (with errorMessage)
```

### Signup Flow
```
Unauthenticated
  ↓
signup(email, password, name, phone?)
  ↓
Loading
  ├─→ Success → Authenticated (with user, tokens, expiry)
  └─→ Error → Unauthenticated (with errorMessage)
```

### Token Refresh Flow
```
Authenticated (with 4:55 remaining)
  ↓
[Timer scheduled for 4:55 - 5:00 = automatic]
  ↓
refreshAccessToken()
  ↓
Loading [implicit, no UI change needed]
  ├─→ Success → Authenticated (tokens updated silently)
  └─→ Error → Unauthenticated (user logged out)
```

### Session Expiry Flow
```
Authenticated (with 2:30 remaining)
  ↓
[Timer scheduled for 2:30 - 2:00 = :30 seconds from now]
  ↓
SessionExpiring warning shown to user
  ├─→ User taps "Continue" → refreshAccessToken()
  │   ├─→ Success → Authenticated (session extended)
  │   └─→ Error → Unauthenticated
  └─→ User waits → auto-logout after expiry
```

### Logout Flow
```
Authenticated
  ↓
logout()
  ↓
Loading
  ↓
Unauthenticated (tokens cleared, timers cancelled)
```

## Using Providers in UI

### Basic Pattern
```dart
class LoginScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch providers for reactive updates
    final authState = ref.watch(authProvider);
    final isLoading = ref.watch(isAuthLoadingProvider);

    return Scaffold(
      // UI code
    );
  }
}
```

### Login Implementation
```dart
void _handleLogin() async {
  final authNotifier = ref.read(authProvider.notifier);

  try {
    await authNotifier.login(email: _emailController.text, password: _passwordController.text);
    // Success - state automatically updated to Authenticated
    // Navigator handles routing based on isAuthenticatedProvider
  } on AuthException catch (e) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(text: e.message));
  }
}
```

### Conditional UI Based on Auth State
```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  final authState = ref.watch(authProvider);

  return switch (authState) {
    AuthStateInitial() => SplashScreen(),
    AuthStateLoading() => LoadingIndicator(),
    AuthStateUnauthenticated(:final errorMessage) => LoginScreen(
      errorMessage: errorMessage,
    ),
    AuthStateAuthenticated(:final user) => HomeScreen(user: user),
    AuthStateSessionExpiring(:final timeRemaining) =>
      DialogOverlay(
        child: HomeScreen(),
        dialog: SessionWarningDialog(timeRemaining: timeRemaining),
      ),
  };
}
```

### Display Error Message
```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  final errorMessage = ref.watch(authErrorProvider);

  return errorMessage != null
    ? ErrorBanner(message: errorMessage)
    : SizedBox.shrink();
}
```

### Show User Info
```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  final user = ref.watch(currentUserProvider);

  return user != null
    ? Text('Welcome ${user.name}!')
    : SizedBox.shrink();
}
```

### Session Warning
```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  final warning = ref.watch(sessionWarningProvider);

  if (warning != null) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text('Session Expiring'),
        content: Text('Your session expires in ${warning.minutesRemaining}m'),
        actions: [
          TextButton(
            onPressed: () {
              ref.read(authProvider.notifier).refreshAccessToken();
              Navigator.pop(context);
            },
            child: Text('Continue'),
          ),
        ],
      ),
    );
  }

  return SizedBox.shrink();
}
```

## Business Logic Details

### AuthNotifier Methods

#### _checkAuthStatus()
- Called automatically on app start
- Checks if stored token is still valid
- Transitions from Initial → Authenticated (if valid token) or Unauthenticated
- Schedules token refresh if needed

#### login() / signup()
- Transition: Unauthenticated → Loading → Authenticated (or Unauthenticated with error)
- Calls AuthService API methods
- Stores tokens and user data via AuthService._storeAuthData()
- Calculates expiry time from response
- Schedules automatic token refresh

#### logout()
- Transition: Authenticated → Loading → Unauthenticated
- Calls AuthService.logout() (backend invalidation attempt)
- Clears all stored tokens and user data
- Cancels all timers (refresh, warning)
- Clears auth state

#### refreshAccessToken()
- Called automatically when token needs refresh
- Only works if state is Authenticated
- Updates tokens without changing user
- Automatically schedules next refresh
- On failure: Logs out user and sets error state

#### _scheduleTokenRefresh()
- Calculates when token should be refreshed
- Refreshes when < 5 minutes remain
- Uses Timer to trigger _refreshTokenDelayed()
- Called after login, signup, and successful refresh

#### _scheduleSessionWarning()
- Shows warning when < 2 minutes remain
- Changes state to SessionExpiring
- Allows user to refresh or wait for logout

### Error Handling Strategy

1. **API Errors**: Caught in notifier, transformed to user-friendly messages
2. **Token Expired**: Detected by refresh, triggers automatic logout
3. **Network Errors**: Caught, logged, returned as AuthException
4. **Validation Errors**: Passed through from API

### Token Management Strategy

1. **Storage**: Tokens stored in SharedPreferences via AuthService
2. **Expiry Calculation**: Backend provides `expires_in` (seconds), converted to absolute DateTime
3. **Validation**: Token validity checked before use
4. **Refresh**: Automatic when < 5 minutes remain
5. **Cleanup**: All tokens cleared on logout

## Performance Optimizations

### 1. Select Pattern (Implicit)
All derived providers use implicit select pattern:
```dart
final isAuthenticatedProvider = Provider<bool>((ref) {
  final authState = ref.watch(authProvider);
  return authState is AuthStateAuthenticated;
});
```
This ensures widgets only rebuild when their specific value changes, not when unrelated auth state fields change.

### 2. Sealed Classes for Pattern Matching
```dart
final authState = ref.watch(authProvider);
return switch (authState) {
  AuthStateAuthenticated(:final user) => UserWidget(user),
  _ => LoginWidget(),
};
```
Leverages Dart 3's exhaustiveness checking and pattern matching for clean, efficient UI logic.

### 3. Minimal Rebuilds
- Token updates don't trigger UI rebuilds unless watched
- User info doesn't rebuild when token refreshes
- Error dismissal doesn't rebuild success states

### 4. Timer Management
- Timers are cancelled and rescheduled as needed
- No memory leaks - timers disposed with notifier
- Only one refresh timer active at a time

## Testing Strategy

### Unit Tests
```dart
test('login transitions from Unauthenticated to Loading to Authenticated', () async {
  final authService = MockAuthService();
  final notifier = AuthNotifier(authService);

  expect(notifier.state, isA<AuthStateUnauthenticated>());

  final future = notifier.login(email: 'test@example.com', password: 'pass');
  expect(notifier.state, isA<AuthStateLoading>());

  await future;
  expect(notifier.state, isA<AuthStateAuthenticated>());
});
```

### Widget Tests
```dart
testWidgets('LoginScreen shows error when login fails', (tester) async {
  final container = ProviderContainer();

  await tester.pumpWidget(
    UncontrolledProviderScope(
      container: container,
      child: MaterialApp(home: LoginScreen()),
    ),
  );

  // Trigger error state
  // Verify error message displayed
});
```

### Integration Tests
```dart
test('Full authentication flow: signup → authenticated → logout → unauthenticated', () async {
  // Test full user journey
});
```

## Migration Guide from StatefulWidget

### Before (StatefulWidget)
```dart
class LoginScreen extends StatefulWidget {
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool _isLoading = false;
  String? _error;

  void _login() async {
    setState(() => _isLoading = true);
    try {
      // API call
      setState(() {
        _isLoading = false;
        _error = null;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _error = e.toString();
      });
    }
  }
}
```

### After (Riverpod)
```dart
class LoginScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isLoading = ref.watch(isAuthLoadingProvider);
    final error = ref.watch(authErrorProvider);

    void _login() async {
      await ref.read(authProvider.notifier).login(
        email: _emailController.text,
        password: _passwordController.text,
      );
    }

    return // UI
  }
}
```

## Architecture Validation Checklist

- [x] State is immutable (sealed classes with copyWith for Authenticated)
- [x] No UI logic in notifier (business logic only)
- [x] All async operations have loading and error states
- [x] Select pattern used for derived providers
- [x] Single source of truth (authProvider)
- [x] Error states are standardized (AuthException subclasses)
- [x] Resource cleanup (timers disposed)
- [x] Proper scoping (application-wide for auth)
- [x] Dependencies injected via ref.watch (AuthService)
- [x] State transitions well-defined
- [x] Edge cases handled (expired tokens, network errors)
- [x] Performance optimized (no excessive rebuilds)
- [x] Testable (services mockable)
- [x] Documentation complete with examples

## Next Steps

1. **Implement AuthService API calls** (API Data Architect)
   - Complete login() implementation
   - Complete signup() implementation
   - Complete refreshAccessToken() implementation
   - Implement logout() backend call

2. **Update UI Screens** (Flutter UI Developer)
   - Replace StatefulWidget with ConsumerWidget
   - Use ref.watch(authProvider) for state
   - Use ref.read(authProvider.notifier) for actions
   - Add error handling and loading indicators

3. **Add Navigation Integration**
   - Create root router that switches based on isAuthenticatedProvider
   - Navigate to login if unauthenticated
   - Navigate to home if authenticated

4. **Add Session Management UI**
   - Implement session warning dialog
   - Show token refresh countdown
   - Allow manual session extend

5. **Testing**
   - Unit test AuthNotifier transitions
   - Widget test screens with different auth states
   - Integration test full authentication flow

## References

- Riverpod Documentation: https://riverpod.dev
- Riverpod 2.x Migration: https://riverpod.dev/docs/migration/from_1_to_2
- StateNotifier Pattern: https://riverpod.dev/docs/providers/state_notifier_provider
- Derived Providers: https://riverpod.dev/docs/providers/combining_providers
