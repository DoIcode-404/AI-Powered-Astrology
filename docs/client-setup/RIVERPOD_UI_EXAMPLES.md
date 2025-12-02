# Riverpod Auth Providers - UI Implementation Examples

This document provides complete, ready-to-use examples for the Flutter UI Developer on how to integrate the Riverpod authentication system into screens.

## Quick Reference: Most Common Provider Usage

```dart
// Watch entire auth state for pattern matching
final authState = ref.watch(authProvider);

// Watch just the authenticated flag
final isAuth = ref.watch(isAuthenticatedProvider);

// Watch just the user
final user = ref.watch(currentUserProvider);

// Watch error messages
final error = ref.watch(authErrorProvider);

// Get the notifier to call actions
final authNotifier = ref.read(authProvider.notifier);
```

---

## Example 1: Login Screen with Full Error Handling

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:client/presentation/providers/auth_provider.dart';
import 'package:client/data/models/auth_models.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  late TextEditingController _emailController;
  late TextEditingController _passwordController;
  bool _obscurePassword = true;

  @override
  void initState() {
    super.initState();
    _emailController = TextEditingController();
    _passwordController = TextEditingController();
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() async {
    final authNotifier = ref.read(authProvider.notifier);

    try {
      await authNotifier.login(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );
      // Success - navigation handled by root route based on isAuthenticatedProvider
      // The state will automatically transition to Authenticated
    } on AuthException catch (e) {
      // Error state is automatically set by the notifier
      // This catch is optional - UI will show error from authErrorProvider
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.message), backgroundColor: Colors.red),
        );
      }
    }
  }

  void _clearError() {
    ref.read(authProvider.notifier).clearError();
  }

  @override
  Widget build(BuildContext context) {
    // Watch auth state for reactive updates
    final authState = ref.watch(authProvider);
    final isLoading = authState is AuthStateLoading;
    final error = ref.watch(authErrorProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: 40),

            // Error Message Banner
            if (error != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: Container(
                  decoration: BoxDecoration(
                    color: Colors.red.shade100,
                    border: Border.all(color: Colors.red.shade400),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  padding: const EdgeInsets.all(12),
                  child: Row(
                    children: [
                      Icon(Icons.error_outline, color: Colors.red.shade700),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Login Failed',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.red.shade700,
                              ),
                            ),
                            Text(
                              error,
                              style: TextStyle(color: Colors.red.shade700),
                            ),
                          ],
                        ),
                      ),
                      IconButton(
                        icon: Icon(Icons.close, color: Colors.red.shade700),
                        onPressed: _clearError,
                      ),
                    ],
                  ),
                ),
              ),

            // Email Field
            TextFormField(
              controller: _emailController,
              enabled: !isLoading,
              keyboardType: TextInputType.emailAddress,
              decoration: InputDecoration(
                labelText: 'Email',
                hintText: 'your.email@example.com',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                prefixIcon: const Icon(Icons.email_outlined),
              ),
            ),
            const SizedBox(height: 16),

            // Password Field
            TextFormField(
              controller: _passwordController,
              enabled: !isLoading,
              obscureText: _obscurePassword,
              decoration: InputDecoration(
                labelText: 'Password',
                hintText: 'Enter your password',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                prefixIcon: const Icon(Icons.lock_outlined),
                suffixIcon: IconButton(
                  icon: Icon(
                    _obscurePassword
                        ? Icons.visibility_off_outlined
                        : Icons.visibility_outlined,
                  ),
                  onPressed: () =>
                      setState(() => _obscurePassword = !_obscurePassword),
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Login Button
            ElevatedButton(
              onPressed: isLoading ? null : _handleLogin,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: Colors.blue,
                disabledBackgroundColor: Colors.grey.shade300,
              ),
              child: isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor:
                            AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    )
                  : const Text(
                      'Login',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
            ),
            const SizedBox(height: 16),

            // Sign Up Link
            TextButton(
              onPressed: isLoading
                  ? null
                  : () {
                      // Navigate to signup
                      Navigator.of(context).pushNamed('/signup');
                    },
              child: const Text("Don't have an account? Sign up"),
            ),

            const SizedBox(height: 16),

            // Forgot Password Link
            TextButton(
              onPressed: isLoading
                  ? null
                  : () {
                      // Navigate to forgot password
                      Navigator.of(context).pushNamed('/forgot-password');
                    },
              child: const Text('Forgot Password?'),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Example 2: Signup Screen with Validation

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:client/presentation/providers/auth_provider.dart';
import 'package:client/data/models/auth_models.dart';

class SignupScreen extends ConsumerStatefulWidget {
  const SignupScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends ConsumerState<SignupScreen> {
  late TextEditingController _nameController;
  late TextEditingController _emailController;
  late TextEditingController _phoneController;
  late TextEditingController _passwordController;
  late TextEditingController _confirmPasswordController;

  bool _obscurePassword = true;
  bool _obscureConfirm = true;
  bool _agreedToTerms = false;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController();
    _emailController = TextEditingController();
    _phoneController = TextEditingController();
    _passwordController = TextEditingController();
    _confirmPasswordController = TextEditingController();
  }

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _phoneController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  String? _validateEmail(String? value) {
    if (value == null || value.isEmpty) {
      return 'Email is required';
    }
    if (!RegExp(r'^[^@]+@[^@]+\.[^@]+').hasMatch(value)) {
      return 'Please enter a valid email';
    }
    return null;
  }

  String? _validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Password is required';
    }
    if (value.length < 8) {
      return 'Password must be at least 8 characters';
    }
    return null;
  }

  void _handleSignup() async {
    // Validate form
    if (_passwordController.text != _confirmPasswordController.text) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Passwords do not match')),
      );
      return;
    }

    if (!_agreedToTerms) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please agree to terms and conditions')),
      );
      return;
    }

    final authNotifier = ref.read(authProvider.notifier);

    try {
      await authNotifier.signup(
        email: _emailController.text.trim(),
        password: _passwordController.text,
        name: _nameController.text.trim(),
        phone: _phoneController.text.isNotEmpty
            ? _phoneController.text.trim()
            : null,
      );
      // Success - navigation handled by root route
    } on AuthException catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.message), backgroundColor: Colors.red),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);
    final isLoading = authState is AuthStateLoading;
    final error = ref.watch(authErrorProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Create Account'),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (error != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: Container(
                  decoration: BoxDecoration(
                    color: Colors.red.shade100,
                    border: Border.all(color: Colors.red.shade400),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  padding: const EdgeInsets.all(12),
                  child: Row(
                    children: [
                      Icon(Icons.error_outline, color: Colors.red.shade700),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          error,
                          style: TextStyle(color: Colors.red.shade700),
                        ),
                      ),
                    ],
                  ),
                ),
              ),

            // Name Field
            TextFormField(
              controller: _nameController,
              enabled: !isLoading,
              decoration: InputDecoration(
                labelText: 'Full Name',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                prefixIcon: const Icon(Icons.person_outlined),
              ),
            ),
            const SizedBox(height: 16),

            // Email Field
            TextFormField(
              controller: _emailController,
              enabled: !isLoading,
              keyboardType: TextInputType.emailAddress,
              validator: _validateEmail,
              decoration: InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                prefixIcon: const Icon(Icons.email_outlined),
              ),
            ),
            const SizedBox(height: 16),

            // Phone Field (Optional)
            TextFormField(
              controller: _phoneController,
              enabled: !isLoading,
              keyboardType: TextInputType.phone,
              decoration: InputDecoration(
                labelText: 'Phone (Optional)',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                prefixIcon: const Icon(Icons.phone_outlined),
              ),
            ),
            const SizedBox(height: 16),

            // Password Field
            TextFormField(
              controller: _passwordController,
              enabled: !isLoading,
              obscureText: _obscurePassword,
              validator: _validatePassword,
              decoration: InputDecoration(
                labelText: 'Password',
                helperText: 'At least 8 characters',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                prefixIcon: const Icon(Icons.lock_outlined),
                suffixIcon: IconButton(
                  icon: Icon(
                    _obscurePassword
                        ? Icons.visibility_off_outlined
                        : Icons.visibility_outlined,
                  ),
                  onPressed: () =>
                      setState(() => _obscurePassword = !_obscurePassword),
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Confirm Password Field
            TextFormField(
              controller: _confirmPasswordController,
              enabled: !isLoading,
              obscureText: _obscureConfirm,
              decoration: InputDecoration(
                labelText: 'Confirm Password',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                prefixIcon: const Icon(Icons.lock_outlined),
                suffixIcon: IconButton(
                  icon: Icon(
                    _obscureConfirm
                        ? Icons.visibility_off_outlined
                        : Icons.visibility_outlined,
                  ),
                  onPressed: () =>
                      setState(() => _obscureConfirm = !_obscureConfirm),
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Terms Checkbox
            Row(
              children: [
                Checkbox(
                  value: _agreedToTerms,
                  onChanged: isLoading
                      ? null
                      : (value) => setState(() => _agreedToTerms = value ?? false),
                ),
                Expanded(
                  child: GestureDetector(
                    onTap: isLoading
                        ? null
                        : () => setState(() => _agreedToTerms = !_agreedToTerms),
                    child: const Text(
                      'I agree to the Terms & Conditions and Privacy Policy',
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Signup Button
            ElevatedButton(
              onPressed: isLoading ? null : _handleSignup,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: Colors.blue,
              ),
              child: isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor:
                            AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    )
                  : const Text(
                      'Create Account',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
            ),
            const SizedBox(height: 16),

            // Login Link
            TextButton(
              onPressed: isLoading
                  ? null
                  : () {
                      Navigator.of(context).pop();
                    },
              child: const Text('Already have an account? Login'),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Example 3: Root Navigation/App Shell - Auth-Aware Routing

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:client/presentation/providers/auth_provider.dart';
import 'package:client/presentation/providers/auth_state.dart';

class AppShell extends ConsumerWidget {
  const AppShell({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);

    // Pattern match on auth state to determine what to show
    return switch (authState) {
      AuthStateInitial() =>
        const Scaffold(body: Center(child: CircularProgressIndicator())),
      AuthStateLoading(:final message) =>
        Scaffold(
          body: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const CircularProgressIndicator(),
                const SizedBox(height: 16),
                if (message != null) Text(message),
              ],
            ),
          ),
        ),
      AuthStateUnauthenticated() =>
        MaterialApp(
          home: const LoginScreen(),
          routes: {
            '/login': (_) => const LoginScreen(),
            '/signup': (_) => const SignupScreen(),
            '/forgot-password': (_) => const ForgotPasswordScreen(),
          },
        ),
      AuthStateAuthenticated(:final user) =>
        MaterialApp(
          home: HomeScreen(user: user),
          routes: {
            '/home': (_) => HomeScreen(user: user),
            '/profile': (_) => ProfileScreen(user: user),
          },
        ),
      AuthStateSessionExpiring(:final user, :final timeRemaining) =>
        MaterialApp(
          home: SessionExpiringOverlay(
            user: user,
            timeRemaining: timeRemaining,
            child: HomeScreen(user: user),
          ),
          routes: {
            '/home': (_) => HomeScreen(user: user),
          },
        ),
    };
  }
}
```

---

## Example 4: Session Expiring Warning Dialog

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:client/presentation/providers/auth_provider.dart';

class SessionExpiringOverlay extends ConsumerWidget {
  final Widget child;
  final UserData user;
  final Duration timeRemaining;

  const SessionExpiringOverlay({
    required this.child,
    required this.user,
    required this.timeRemaining,
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final warning = ref.watch(sessionWarningProvider);

    // Show warning dialog when session is expiring
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (warning != null && !_isDialogShowing(context)) {
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (context) => SessionWarningDialog(
            minutesRemaining: warning.minutesRemaining,
            secondsRemaining: warning.secondsRemaining,
          ),
        );
      }
    });

    return child;
  }

  bool _isDialogShowing(BuildContext context) {
    return ModalRoute.of(context) != null &&
        ModalRoute.of(context)! is PopupRoute;
  }
}

class SessionWarningDialog extends ConsumerWidget {
  final int minutesRemaining;
  final int secondsRemaining;

  const SessionWarningDialog({
    required this.minutesRemaining,
    required this.secondsRemaining,
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return AlertDialog(
      title: const Text('Session Expiring'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            Icons.schedule,
            size: 48,
            color: Colors.orange.shade600,
          ),
          const SizedBox(height: 16),
          Text(
            'Your session expires in $minutesRemaining minute(s)',
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 16),
          ),
          const SizedBox(height: 8),
          Text(
            'Would you like to extend your session?',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey.shade600),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () {
            Navigator.of(context).pop();
            // User chooses to logout
          },
          child: const Text('Logout'),
        ),
        ElevatedButton(
          onPressed: () {
            // User chooses to extend session
            ref
                .read(authProvider.notifier)
                .refreshAccessToken()
                .then((_) {
              if (context.mounted) Navigator.of(context).pop();
            });
          },
          child: const Text('Continue'),
        ),
      ],
    );
  }
}
```

---

## Example 5: Profile Screen - Accessing Current User

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:client/presentation/providers/auth_provider.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch specific user data - efficient, rebuilds only if user changes
    final user = ref.watch(currentUserProvider);

    // Watch token expiry info
    final tokenExpiry = ref.watch(tokenExpiryProvider);

    // Get notifier for logout action
    final authNotifier = ref.read(authProvider.notifier);

    if (user == null) {
      return const Scaffold(
        body: Center(child: Text('Not authenticated')),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await authNotifier.logout();
              if (context.mounted) {
                Navigator.of(context).pushReplacementNamed('/login');
              }
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Avatar
            Center(
              child: user.avatar != null
                  ? CircleAvatar(
                      radius: 50,
                      backgroundImage: NetworkImage(user.avatar!),
                    )
                  : const CircleAvatar(
                      radius: 50,
                      child: Icon(Icons.person, size: 50),
                    ),
            ),
            const SizedBox(height: 24),

            // User Info Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'User Information',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    _InfoRow(label: 'Name', value: user.name),
                    _InfoRow(label: 'Email', value: user.email),
                    if (user.phone != null)
                      _InfoRow(label: 'Phone', value: user.phone!),
                    if (user.createdAt != null)
                      _InfoRow(
                        label: 'Member Since',
                        value: _formatDate(user.createdAt!),
                      ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Token Info Card
            if (tokenExpiry != null)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Session Information',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 16),
                      _InfoRow(
                        label: 'Session Expires At',
                        value: _formatDateTime(tokenExpiry.expiryTime),
                      ),
                      _InfoRow(
                        label: 'Time Remaining',
                        value:
                            '${tokenExpiry.timeRemaining.inHours}h ${tokenExpiry.timeRemaining.inMinutes % 60}m',
                      ),
                      if (tokenExpiry.shouldRefresh)
                        Padding(
                          padding: const EdgeInsets.only(top: 8.0),
                          child: Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: Colors.orange.shade100,
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: const Text(
                              'Token will be refreshed automatically',
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.orange,
                              ),
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
              ),
            const SizedBox(height: 24),

            // Logout Button
            ElevatedButton.icon(
              onPressed: () async {
                await authNotifier.logout();
                if (context.mounted) {
                  Navigator.of(context).pushReplacementNamed('/login');
                }
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
              icon: const Icon(Icons.logout),
              label: const Text('Logout'),
            ),
          ],
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.month}/${date.day}/${date.year}';
  }

  String _formatDateTime(DateTime dateTime) {
    return '${dateTime.month}/${dateTime.day}/${dateTime.year} at ${dateTime.hour}:${dateTime.minute.toString().padLeft(2, '0')}';
  }
}

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;

  const _InfoRow({
    required this.label,
    required this.value,
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          SizedBox(
            width: 100,
            child: Text(
              label,
              style: TextStyle(
                color: Colors.grey.shade600,
                fontSize: 13,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

---

## Example 6: Protected Route/Middleware

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:client/presentation/providers/auth_provider.dart';

/// Widget that only displays content if user is authenticated
/// Automatically navigates to login if not authenticated
class ProtectedRoute extends ConsumerWidget {
  final Widget child;
  final String? redirectTo;

  const ProtectedRoute({
    required this.child,
    this.redirectTo = '/login',
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isAuthenticated = ref.watch(isAuthenticatedProvider);

    if (!isAuthenticated) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        Navigator.of(context).pushReplacementNamed(redirectTo ?? '/login');
      });

      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return child;
  }
}

// Usage:
// ProtectedRoute(
//   child: ProfileScreen(),
//   redirectTo: '/login',
// )
```

---

## Provider Watch Patterns Summary

### Pattern 1: Watch Entire Auth State (Pattern Matching)
```dart
final authState = ref.watch(authProvider);

return switch (authState) {
  AuthStateLoading() => LoadingWidget(),
  AuthStateUnauthenticated(:final errorMessage) =>
    LoginWidget(error: errorMessage),
  AuthStateAuthenticated(:final user) =>
    HomeWidget(user: user),
  _ => SplashWidget(),
};
```

### Pattern 2: Watch Single Boolean
```dart
final isLoading = ref.watch(isAuthLoadingProvider);

return isLoading ? CircularProgressIndicator() : MyButton();
```

### Pattern 3: Watch Computed Value
```dart
final user = ref.watch(currentUserProvider);

return user != null ? UserCard(user) : SizedBox.shrink();
```

### Pattern 4: Watch with Selection (Rare - Implicit in Derived Providers)
```dart
// For custom selections not covered by derived providers
final user = ref.watch(
  authProvider.select((state) =>
    state is AuthStateAuthenticated ? state.user : null
  ),
);
```

### Pattern 5: Read for One-Time Actions
```dart
void onPressed() {
  final authNotifier = ref.read(authProvider.notifier);
  authNotifier.login(email: 'test@example.com', password: 'pass');
}
```

---

## Error Handling Best Practices

### 1. Automatic Error Display (Recommended)
```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  final error = ref.watch(authErrorProvider);

  return error != null
    ? ErrorBanner(message: error)
    : SizedBox.shrink();
}
```

### 2. Manual Error Handling with Try-Catch
```dart
void handleLogin() async {
  final authNotifier = ref.read(authProvider.notifier);

  try {
    await authNotifier.login(email: email, password: password);
  } on AuthException catch (e) {
    // Handle specific auth errors
    showErrorDialog(e.message);
  } catch (e) {
    // Handle unexpected errors
    showErrorDialog('Unexpected error occurred');
  }
}
```

### 3. Retry Pattern
```dart
void handleRetry() async {
  final authNotifier = ref.read(authProvider.notifier);

  try {
    await authNotifier.retryLogin(email: email, password: password);
  } catch (e) {
    // Handle error again
  }
}
```

---

## Testing Example

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:client/presentation/providers/auth_provider.dart';

void main() {
  test('Login transitions state correctly', () async {
    final container = ProviderContainer(
      overrides: [
        // Override authServiceProvider with mock
        authServiceProvider.overrideWithValue(MockAuthService()),
      ],
    );

    // Initial state
    expect(
      container.read(authProvider),
      isA<AuthStateInitial>(),
    );

    // Trigger login
    final notifier = container.read(authProvider.notifier);
    await notifier.login(email: 'test@test.com', password: 'password');

    // Check authenticated state
    expect(
      container.read(authProvider),
      isA<AuthStateAuthenticated>(),
    );

    // Check derived provider
    expect(
      container.read(isAuthenticatedProvider),
      true,
    );

    // Check user
    expect(
      container.read(currentUserProvider)?.email,
      'test@test.com',
    );
  });
}
```

---

## Summary: Key Takeaways for UI Developer

1. **Replace StatefulWidget with ConsumerWidget** to access Riverpod providers
2. **Use `ref.watch()` for reactive updates** - automatically rebuilds when state changes
3. **Use `ref.read()` for one-time actions** - call notifier methods for login/signup
4. **Pattern match on authState** using Dart 3's switch expressions for clean UI logic
5. **Use derived providers** (isAuthenticated, currentUser, etc.) instead of watching entire state
6. **Handle errors** automatically via authErrorProvider or with try-catch
7. **Let loading state drive UI** - watch isAuthLoadingProvider to show spinners
8. **Let navigation react to auth** - AppShell watches authProvider to switch screens
9. **Session warnings are built-in** - watch sessionWarningProvider for expiry dialogs
10. **No manual state management needed** - AuthNotifier handles all logic

All timer scheduling, token refresh, and state transitions are handled by AuthNotifier automatically!
