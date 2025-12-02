# Riverpod Auth - Quick Reference Guide

## Import Authentication Providers

```dart
import 'package:client/presentation/providers/auth_provider.dart';
import 'package:client/presentation/providers/auth_state.dart';
```

## Watch Entire Auth State

```dart
final authState = ref.watch(authProvider);

switch (authState) {
  AuthStateInitial() => SplashScreen(),
  AuthStateLoading() => LoadingScreen(),
  AuthStateUnauthenticated(:final errorMessage) => LoginScreen(),
  AuthStateAuthenticated(:final user) => HomeScreen(),
  AuthStateSessionExpiring() => WarningDialog(),
}
```

## Watch Individual Values (Recommended)

```dart
// Boolean flags
final isAuthenticated = ref.watch(isAuthenticatedProvider);
final isLoading = ref.watch(isAuthLoadingProvider);
final isSessionExpiring = ref.watch(isSessionExpiringProvider);

// Data
final user = ref.watch(currentUserProvider);
final token = ref.watch(accessTokenProvider);
final error = ref.watch(authErrorProvider);

// Detailed info
final tokenInfo = ref.watch(tokenExpiryProvider);
final warning = ref.watch(sessionWarningProvider);
```

## Call Auth Methods

```dart
final authNotifier = ref.read(authProvider.notifier);

// Login
await authNotifier.login(
  email: 'user@example.com',
  password: 'password',
);

// Signup
await authNotifier.signup(
  email: 'user@example.com',
  password: 'password',
  name: 'John Doe',
  phone: '+1234567890', // optional
);

// Logout
await authNotifier.logout();

// Refresh token (automatic, but can call manually)
await authNotifier.refreshAccessToken();

// Clear error
authNotifier.clearError();
```

## Error Handling

```dart
// Automatic - Watch error provider
final error = ref.watch(authErrorProvider);
if (error != null) {
  showError(error);
}

// Manual - Try-catch
try {
  await authNotifier.login(email, password);
} on AuthException catch (e) {
  showError(e.message);
}
```

## Conditional UI

```dart
// Show loading spinner
if (ref.watch(isAuthLoadingProvider)) {
  return CircularProgressIndicator();
}

// Show user info only if authenticated
final user = ref.watch(currentUserProvider);
if (user != null) {
  return Text('Welcome ${user.name}');
}

// Show session warning
final warning = ref.watch(sessionWarningProvider);
if (warning != null) {
  return SessionWarningDialog(
    minutesRemaining: warning.minutesRemaining,
  );
}
```

## Screen Conversion (StatefulWidget → ConsumerWidget)

**Before:**
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
    // ... api call ...
  }

  @override
  Widget build(BuildContext context) {
    return // ...
  }
}
```

**After:**
```dart
class LoginScreen extends ConsumerWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isLoading = ref.watch(isAuthLoadingProvider);
    final error = ref.watch(authErrorProvider);

    void _login() async {
      await ref.read(authProvider.notifier).login(
        email: email,
        password: password,
      );
    }

    return // ...
  }
}
```

## Root Navigation (Auth-Aware)

```dart
class AppShell extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);

    return switch (authState) {
      AuthStateInitial() => SplashScreen(),
      AuthStateLoading() => LoadingScreen(),
      AuthStateUnauthenticated() => LoginScreen(),
      AuthStateAuthenticated(:final user) => HomeScreen(user: user),
      AuthStateSessionExpiring() => SessionWarningOverlay(),
    };
  }
}
```

## State Transitions Quick Map

```
Initial → (checkAuthStatus) → Authenticated (if valid token)
                            → Unauthenticated (if no token)

Unauthenticated → (login) → Loading → Authenticated ✓
                                    → Unauthenticated ✗

Unauthenticated → (signup) → Loading → Authenticated ✓
                                     → Unauthenticated ✗

Authenticated → (logout) → Loading → Unauthenticated

Authenticated → (auto refresh @ 5 min before expiry) → Authenticated (token updated)

Authenticated → (warning @ 2 min before expiry) → SessionExpiring
                                                   ├→ (extend) → refreshAccessToken()
                                                   └→ (wait) → logout
```

## Common Patterns

### Pattern 1: Conditional Navigation
```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  final isAuth = ref.watch(isAuthenticatedProvider);

  useEffect(() {
    if (isAuth) {
      Navigator.of(context).pushReplacementNamed('/home');
    }
  }, [isAuth]);

  return LoginScreen();
}
```

### Pattern 2: Protected Route
```dart
class ProtectedRoute extends ConsumerWidget {
  final Widget child;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isAuth = ref.watch(isAuthenticatedProvider);

    if (!isAuth) {
      return LoginScreen();
    }

    return child;
  }
}

// Usage:
ProtectedRoute(child: ProfileScreen())
```

### Pattern 3: Session Warning Dialog
```dart
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final warning = ref.watch(sessionWarningProvider);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (warning != null) {
        showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: Text('Session Expiring'),
            content: Text('${warning.minutesRemaining} minutes left'),
            actions: [
              TextButton(
                onPressed: () {
                  ref.read(authProvider.notifier).logout();
                },
                child: Text('Logout'),
              ),
              ElevatedButton(
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
    });

    return SizedBox.shrink();
  }
}
```

### Pattern 4: Display User Info
```dart
class UserCard extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(currentUserProvider);
    final token = ref.watch(tokenExpiryProvider);

    return user == null
      ? SizedBox.shrink()
      : Card(
          child: Column(
            children: [
              Text(user.name),
              Text(user.email),
              if (token != null)
                Text('Expires: ${token.expiryTime}'),
            ],
          ),
        );
  }
}
```

## Debugging

```dart
// Check current state
final state = ref.watch(authProvider);
print('Auth state: $state');

// Force refresh (use rarely)
ref.refresh(authProvider);

// Check specific value
final isAuth = ref.watch(isAuthenticatedProvider);
print('Is authenticated: $isAuth');
```

## Testing

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

test('Login works', () async {
  final container = ProviderContainer(
    overrides: [
      authServiceProvider.overrideWithValue(MockAuthService()),
    ],
  );

  final notifier = container.read(authProvider.notifier);
  await notifier.login(email: 'test@test.com', password: 'pass');

  expect(
    container.read(authProvider),
    isA<AuthStateAuthenticated>(),
  );
});
```

## Common Issues

### "Can't access ref outside of widget"
Solution: Use ConsumerWidget, not StatelessWidget

### "State not updating"
Solution: Make sure you're using ref.watch(), not ref.read()

### "Timer never fires"
Solution: Check token expiry calculation, ensure DateTime is correct

### "Error state not showing"
Solution: Check authErrorProvider is being watched

### "Excessive rebuilds"
Solution: Use specific derived providers instead of watching entire authState

## Checklist Before Deploy

- [ ] All screens converted to ConsumerWidget
- [ ] Error handling implemented
- [ ] Session warnings working
- [ ] Token refresh happens automatically
- [ ] No manual token management in UI
- [ ] No memory leaks (test with DevTools)
- [ ] All state transitions tested
- [ ] Error messages are user-friendly
- [ ] Loading states show spinners
- [ ] Logout clears all data
- [ ] Navigation switches on auth state

## Emergency Reset (for development only)

```dart
// Clear all auth data
await ref.read(authProvider.notifier).logout();

// Force to initial state
ref.read(authProvider);
```

## Performance Tips

1. Use derived providers instead of watching entire authState
2. Only watch what you need
3. Use ConsumerWidget, not Consumer widget
4. Avoid unnecessary state updates in notifier
5. Profile with DevTools to find issues

## Helpful Links

- Auth Provider: `lib/presentation/providers/auth_provider.dart`
- Auth State: `lib/presentation/providers/auth_state.dart`
- Auth Notifier: `lib/presentation/notifiers/auth_notifier.dart`
- Architecture Docs: `RIVERPOD_AUTH_ARCHITECTURE.md`
- UI Examples: `RIVERPOD_UI_EXAMPLES.md`
- Setup Guide: `RIVERPOD_SETUP.md`

---

**Last Updated**: November 24, 2025
**Version**: 1.0 - Production Ready
