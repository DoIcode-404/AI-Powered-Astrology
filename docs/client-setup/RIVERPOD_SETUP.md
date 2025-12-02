# Riverpod Setup & Configuration Guide

## Step 1: Update pubspec.yaml

### Current State
Your `pubspec.yaml` currently uses:
```yaml
dependencies:
  provider: ^6.1.1  # Old provider package
```

### Required Changes

Add Riverpod dependencies to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter

  # State Management - REPLACE provider with riverpod
  flutter_riverpod: ^2.5.0        # NEW: Riverpod state management
  riverpod: ^2.5.0                # NEW: Core Riverpod (required by flutter_riverpod)

  # ... rest of your dependencies remain the same ...
  cupertino_icons: ^1.0.8
  dio: ^5.4.0
  dio_cache_interceptor: ^3.4.4
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  shared_preferences: ^2.2.2
  # ... other dependencies ...

dev_dependencies:
  flutter_test:
    sdk: flutter

  # Code Generation
  build_runner: ^2.4.8            # Already present
  hive_generator: ^2.0.1          # Already present

  # Linting
  flutter_lints: ^5.0.0           # Already present
```

### Version Note
- **Latest stable**: `flutter_riverpod: ^2.5.0` and `riverpod: ^2.5.0`
- **Compatibility**: Requires Flutter 3.0+, Dart 3.0+
- **Your project**: Already meets requirements (SDK ^3.7.0)

## Step 2: Update Dependency

```bash
# Navigate to client directory
cd client

# Get new dependencies
flutter pub get

# Update dependencies (if needed)
flutter pub upgrade
```

## Step 3: Update Main.dart

Wrap your app with `ProviderScope` to enable Riverpod:

### Before (Current)
```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';  // Old provider

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Astrology App',
      home: const LoginScreen(),
    );
  }
}
```

### After (With Riverpod)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';  // NEW: Riverpod
import 'package:client/data/services/auth_service.dart';
import 'package:client/presentation/shell/app_shell.dart';

void main() async {
  // Initialize AuthService before running app
  final authService = AuthService();
  await authService.init();

  runApp(
    ProviderScope(  // NEW: Wrap with ProviderScope
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Astrology App',
      theme: ThemeData(
        primarySwatch: Colors.purple,
        useMaterial3: true,
      ),
      home: const AppShell(),  // Root navigation that switches based on auth
    );
  }
}
```

## Step 4: Update Imports Across Project

### Replace all old provider imports
```dart
// OLD
import 'package:provider/provider.dart';

// NEW
import 'package:flutter_riverpod/flutter_riverpod.dart';
```

### Replace StatefulWidget with ConsumerWidget for auth screens

```dart
// OLD
class LoginScreen extends StatefulWidget {
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  // ...
}

// NEW
class LoginScreen extends ConsumerWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // ...
  }
}
```

## Step 5: Test Setup

Create a simple test to verify Riverpod is working:

```dart
// test/riverpod_setup_test.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:client/presentation/providers/auth_provider.dart';

void main() {
  test('AuthService provider can be accessed', () {
    final container = ProviderContainer();

    // This should not throw
    final authService = container.read(authServiceProvider);
    expect(authService, isNotNull);
  });

  test('Auth provider initializes to AuthStateInitial', () {
    final container = ProviderContainer();

    final authState = container.read(authProvider);
    expect(authState, isA<AuthStateInitial>());
  });
}
```

Run the test:
```bash
cd client
flutter test test/riverpod_setup_test.dart
```

## File Structure After Setup

```
client/
├── lib/
│   ├── main.dart                          # UPDATED with ProviderScope
│   ├── data/
│   │   ├── models/
│   │   │   └── auth_models.dart           # (unchanged)
│   │   └── services/
│   │       ├── auth_service.dart          # (unchanged, needs API impl)
│   │       └── api_client.dart            # (unchanged)
│   ├── presentation/
│   │   ├── providers/
│   │   │   ├── auth_provider.dart         # NEW: Riverpod providers
│   │   │   ├── auth_state.dart            # NEW: State classes
│   │   │   └── index.dart                 # NEW: Barrel export
│   │   ├── notifiers/
│   │   │   ├── auth_notifier.dart         # NEW: Business logic
│   │   │   └── index.dart                 # NEW: Barrel export
│   │   ├── screens/
│   │   │   ├── auth/
│   │   │   │   ├── login_screen.dart      # UPDATED to ConsumerWidget
│   │   │   │   ├── signup_screen.dart     # UPDATED to ConsumerWidget
│   │   │   │   └── ...
│   │   └── shell/
│   │       └── app_shell.dart             # NEW: Root navigation
│   └── core/
│       └── ...
├── test/
│   └── riverpod_setup_test.dart           # NEW: Verify setup
├── pubspec.yaml                           # UPDATED dependencies
└── ...
```

## Migration Guide: Provider to Riverpod

### Watching State

**OLD (Provider)**
```dart
Consumer(
  builder: (context, watch, child) {
    final value = watch(myProvider);
    return Text('$value');
  },
)
```

**NEW (Riverpod)**
```dart
ConsumerWidget(
  build: (context, ref) {
    final value = ref.watch(myProvider);
    return Text('$value');
  },
)
```

### Reading State

**OLD (Provider)**
```dart
Provider.of<MyNotifier>(context, listen: false).doSomething();
```

**NEW (Riverpod)**
```dart
ref.read(myProvider.notifier).doSomething();
```

### StateNotifier

**OLD (Provider)**
```dart
class MyNotifier extends StateNotifier<MyState> {
  MyNotifier() : super(initialState);

  void doSomething() {
    state = newState;
  }
}

final myProvider = StateNotifierProvider<MyNotifier, MyState>((ref) {
  return MyNotifier();
});
```

**NEW (Riverpod 2.x) - Same pattern**
```dart
class MyNotifier extends StateNotifier<MyState> {
  MyNotifier() : super(initialState);

  void doSomething() {
    state = newState;
  }
}

final myProvider = StateNotifierProvider<MyNotifier, MyState>((ref) {
  return MyNotifier();
});
```

**Key Difference**: Riverpod 2.x requires explicit import of `StateNotifier` from `flutter_riverpod`

## Common Issues & Solutions

### Issue 1: "ProviderScope not found"
**Cause**: `ProviderScope` not imported or added to main.dart

**Solution**:
```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Wrap MaterialApp
runApp(
  ProviderScope(
    child: MyApp(),
  ),
);
```

### Issue 2: "ConsumerWidget requires WidgetRef"
**Cause**: Trying to use `ConsumerWidget` without `ref` parameter

**Solution**:
```dart
// WRONG
class MyScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context) { }  // Missing ref
}

// RIGHT
class MyScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) { }
}
```

### Issue 3: "StateNotifier.state is not found"
**Cause**: Not extending `StateNotifier` properly

**Solution**:
```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

class MyNotifier extends StateNotifier<MyState> {
  MyNotifier() : super(initialState);

  void update() {
    state = newState;  // This should work
  }
}
```

### Issue 4: "AuthService already initialized"
**Cause**: Calling `AuthService().init()` multiple times

**Solution**: Initialize once in main(), before ProviderScope:
```dart
void main() async {
  final authService = AuthService();
  await authService.init();

  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}
```

### Issue 5: "Hot reload not working with providers"
**Solution**: Full restart instead of hot reload
```bash
# Use full restart for Riverpod changes
flutter run --full-restart

# Or in IDE, press R (not r)
```

## Performance Considerations

### Memory Usage
- **Before**: Provider package - moderate memory footprint
- **After**: Riverpod 2.x - slightly lower footprint, better caching
- **Impact**: Negligible on modern devices

### Build Time
- **Adding Riverpod**: ~1-2 seconds additional compile time
- **No code generation**: Riverpod doesn't require build_runner

### Runtime Performance
- **Improved**: Better widget rebuild optimization
- **Derived providers**: No unnecessary rebuilds
- **State caching**: More efficient than previous provider package

## Debugging with Riverpod

### Enable Riverpod DevTools
```dart
// main.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(
    ProviderScope(
      observers: [
        // Add this observer to track all provider changes
        RiverpodObserver(),
      ],
      child: MyApp(),
    ),
  );
}

// Create custom observer for logging
class RiverpodObserver extends ProviderObserver {
  @override
  void didUpdateProvider(
    ProviderBase provider,
    Object? previousValue,
    Object? newValue,
    ProviderContainer container,
  ) {
    print('${provider.name}: $previousValue -> $newValue');
  }
}
```

### Console Logging
```dart
// In providers or notifiers
print('AuthState: $state');  // Prints state changes
```

## Rollback Plan

If you need to revert to the old Provider package:

```yaml
# Revert pubspec.yaml
dependencies:
  provider: ^6.1.1  # Old provider

# Remove Riverpod
- flutter_riverpod: ^2.5.0
- riverpod: ^2.5.0
```

```bash
flutter pub get
```

However, **not recommended** - Riverpod is superior and the migration is straightforward.

## Next Steps

1. **Update pubspec.yaml** with Riverpod dependencies
2. **Run flutter pub get**
3. **Update main.dart** with ProviderScope
4. **Update auth screens** to ConsumerWidget
5. **Test** with `flutter test`
6. **Verify** state transitions work correctly

## Support Resources

- **Riverpod Docs**: https://riverpod.dev
- **Migration Guide**: https://riverpod.dev/docs/migration/from_1_to_2
- **API Reference**: https://pub.dev/documentation/flutter_riverpod/latest/
- **Example Projects**: https://github.com/rrousselGit/riverpod/tree/master/examples

## Checklist

- [ ] Added `flutter_riverpod` to pubspec.yaml
- [ ] Added `riverpod` to pubspec.yaml
- [ ] Ran `flutter pub get`
- [ ] Updated main.dart with ProviderScope
- [ ] Created auth_provider.dart
- [ ] Created auth_state.dart
- [ ] Created auth_notifier.dart
- [ ] Updated import statements across project
- [ ] Converted auth screens to ConsumerWidget
- [ ] Tested with `flutter test`
- [ ] Verified hot reload works
- [ ] Profiled for performance issues
- [ ] All auth state transitions working

You're all set! Riverpod is now integrated into your project.
