# Auth Service - Practical Usage Examples

This document provides real-world examples of how to use the AuthService in different scenarios.

---

## Table of Contents

1. [Login Screen](#login-screen)
2. [Signup Screen](#signup-screen)
3. [Profile Screen](#profile-screen)
4. [Navigation & Auth Guards](#navigation--auth-guards)
5. [Error Handling Patterns](#error-handling-patterns)
6. [Advanced Usage](#advanced-usage)

---

## Login Screen

### Basic Login Implementation

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:client/data/models/auth_models.dart';
import 'package:client/presentation/providers/auth_provider.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  /// Handle login button press
  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    try {
      // Call AuthNotifier.login() which internally uses AuthService
      await ref.read(authProvider.notifier).login(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );

      // AuthNotifier will update state to AuthStateAuthenticated
      // No need to navigate manually - listen to state changes
    } catch (e) {
      // Error is handled in AuthNotifier
      // State will be AuthStateUnauthenticated with error message
    }
  }

  @override
  Widget build(BuildContext context) {
    // Watch auth state
    final authState = ref.watch(authProvider);

    // Handle state changes
    ref.listen(authProvider, (previous, next) {
      if (next is AuthStateAuthenticated) {
        // Successfully logged in - navigate to home
        Navigator.of(context).pushNamedAndRemoveUntil(
          '/home',
          (route) => false,
        );
      }
    });

    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              // Email field
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(labelText: 'Email'),
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Email is required';
                  if (!value!.contains('@')) return 'Invalid email';
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Password field
              TextFormField(
                controller: _passwordController,
                decoration: const InputDecoration(labelText: 'Password'),
                obscureText: true,
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Password is required';
                  if ((value?.length ?? 0) < 6) {
                    return 'Password must be at least 6 characters';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),

              // Login button
              if (authState is! AuthStateLoading)
                ElevatedButton(
                  onPressed: _handleLogin,
                  child: const Padding(
                    padding: EdgeInsets.symmetric(
                      horizontal: 32,
                      vertical: 12,
                    ),
                    child: Text('Login'),
                  ),
                )
              else
                const CircularProgressIndicator(),

              const SizedBox(height: 16),

              // Error message
              if (authState is AuthStateUnauthenticated &&
                  authState.errorMessage != null)
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade100,
                    border: Border.all(color: Colors.red),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    authState.errorMessage!,
                    style: const TextStyle(color: Colors.red),
                  ),
                ),

              const SizedBox(height: 16),

              // Link to signup
              TextButton(
                onPressed: () {
                  Navigator.of(context).pushNamed('/signup');
                },
                child: const Text("Don't have an account? Sign up"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### Login with Remember Me Feature

```dart
class LoginScreenWithRememberMe extends ConsumerStatefulWidget {
  const LoginScreenWithRememberMe({Key? key}) : super(key: key);

  @override
  ConsumerState<LoginScreenWithRememberMe> createState() =>
      _LoginScreenWithRememberMeState();
}

class _LoginScreenWithRememberMeState
    extends ConsumerState<LoginScreenWithRememberMe> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _rememberMe = false;

  @override
  void initState() {
    super.initState();
    _loadSavedEmail();
  }

  /// Load previously saved email if remember me was checked
  Future<void> _loadSavedEmail() async {
    final prefs = await SharedPreferences.getInstance();
    final savedEmail = prefs.getString('saved_email');
    if (savedEmail != null) {
      setState(() {
        _emailController.text = savedEmail;
        _rememberMe = true;
      });
    }
  }

  /// Save or clear saved email based on remember me checkbox
  Future<void> _saveEmail() async {
    final prefs = await SharedPreferences.getInstance();
    if (_rememberMe) {
      await prefs.setString('saved_email', _emailController.text);
    } else {
      await prefs.remove('saved_email');
    }
  }

  Future<void> _handleLogin() async {
    try {
      // Login first
      await ref.read(authProvider.notifier).login(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );

      // If successful, save email if remember me is checked
      await _saveEmail();
    } catch (e) {
      // Error is handled by AuthNotifier
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(
                hintText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: const InputDecoration(
                hintText: 'Password',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),

            // Remember me checkbox
            CheckboxListTile(
              value: _rememberMe,
              onChanged: (value) {
                setState(() {
                  _rememberMe = value ?? false;
                });
              },
              title: const Text('Remember me'),
            ),
            const SizedBox(height: 24),

            // Login button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: authState is AuthStateLoading
                    ? null
                    : _handleLogin,
                child: authState is AuthStateLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                        ),
                      )
                    : const Text('LOGIN'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
```

---

## Signup Screen

### Basic Signup Implementation

```dart
class SignupScreen extends ConsumerStatefulWidget {
  const SignupScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends ConsumerState<SignupScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  final _usernameController = TextEditingController();
  final _fullNameController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    _usernameController.dispose();
    _fullNameController.dispose();
    super.dispose();
  }

  /// Validate form and create account
  Future<void> _handleSignup() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    try {
      // Create signup request
      final request = SignupRequest(
        email: _emailController.text.trim(),
        password: _passwordController.text,
        username: _usernameController.text.trim(),
        fullName: _fullNameController.text.trim(),
      );

      // Call AuthNotifier.signup() which internally uses AuthService
      await ref.read(authProvider.notifier).signup(
        email: request.email,
        password: request.password,
        name: request.fullName,
      );

      // On success, AuthNotifier updates state to AuthStateAuthenticated
    } catch (e) {
      // Error is handled in AuthNotifier
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);

    // Navigate on successful signup
    ref.listen(authProvider, (previous, next) {
      if (next is AuthStateAuthenticated) {
        Navigator.of(context).pushNamedAndRemoveUntil(
          '/home',
          (route) => false,
        );
      }
    });

    return Scaffold(
      appBar: AppBar(title: const Text('Sign Up')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              // Email field
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  hintText: 'user@example.com',
                ),
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Email is required';
                  if (!value!.contains('@')) return 'Invalid email format';
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Username field
              TextFormField(
                controller: _usernameController,
                decoration: const InputDecoration(
                  labelText: 'Username',
                  hintText: 'Choose a username',
                ),
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Username is required';
                  if ((value?.length ?? 0) < 3) {
                    return 'Username must be at least 3 characters';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Full name field
              TextFormField(
                controller: _fullNameController,
                decoration: const InputDecoration(
                  labelText: 'Full Name',
                  hintText: 'Your full name',
                ),
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Full name is required';
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Password field
              TextFormField(
                controller: _passwordController,
                decoration: const InputDecoration(
                  labelText: 'Password',
                ),
                obscureText: true,
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Password is required';
                  if ((value?.length ?? 0) < 8) {
                    return 'Password must be at least 8 characters';
                  }
                  if (!value!.contains(RegExp(r'[A-Z]'))) {
                    return 'Password must contain uppercase letter';
                  }
                  if (!value.contains(RegExp(r'[0-9]'))) {
                    return 'Password must contain number';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Confirm password field
              TextFormField(
                controller: _confirmPasswordController,
                decoration: const InputDecoration(
                  labelText: 'Confirm Password',
                ),
                obscureText: true,
                validator: (value) {
                  if (value != _passwordController.text) {
                    return 'Passwords do not match';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),

              // Signup button
              if (authState is! AuthStateLoading)
                ElevatedButton(
                  onPressed: _handleSignup,
                  child: const Padding(
                    padding: EdgeInsets.symmetric(
                      horizontal: 32,
                      vertical: 12,
                    ),
                    child: Text('Create Account'),
                  ),
                )
              else
                const CircularProgressIndicator(),

              const SizedBox(height: 16),

              // Error message
              if (authState is AuthStateUnauthenticated &&
                  authState.errorMessage != null)
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade100,
                    border: Border.all(color: Colors.red),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    authState.errorMessage!,
                    style: const TextStyle(color: Colors.red),
                  ),
                ),

              const SizedBox(height: 16),

              // Link to login
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text('Already have an account? Login'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### Signup with Email Verification

```dart
class SignupWithVerificationScreen extends ConsumerStatefulWidget {
  const SignupWithVerificationScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<SignupWithVerificationScreen> createState() =>
      _SignupWithVerificationScreenState();
}

class _SignupWithVerificationScreenState
    extends ConsumerState<SignupWithVerificationScreen> {
  late PageController _pageController;
  int _currentPage = 0;

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: PageView(
        controller: _pageController,
        onPageChanged: (index) {
          setState(() => _currentPage = index);
        },
        children: [
          // Page 1: Enter credentials
          SignupFormPage(
            onNext: (request) {
              // Save request and go to next page
              _pageController.nextPage(
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeInOut,
              );
            },
          ),
          // Page 2: Verify email
          EmailVerificationPage(
            onVerified: () {
              // Complete signup
              _pageController.nextPage(
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeInOut,
              );
            },
          ),
          // Page 3: Success
          const SignupSuccessPage(),
        ],
      ),
    );
  }
}
```

---

## Profile Screen

### Displaying Current User

```dart
class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch current user from provider
    final user = ref.watch(currentUserProvider);
    final isLoading = ref.watch(isAuthLoadingProvider);

    if (user == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Profile')),
        body: const Center(
          child: Text('Not authenticated'),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () async {
              // Refresh user data
              final authService = ref.read(authServiceProvider);
              try {
                await authService.getCurrentUser();
              } catch (e) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Failed to refresh: $e')),
                );
              }
            },
          ),
        ],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  // User avatar
                  CircleAvatar(
                    radius: 50,
                    child: Text(user.email[0].toUpperCase()),
                  ),
                  const SizedBox(height: 16),

                  // User info
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          ListTile(
                            title: const Text('Email'),
                            subtitle: Text(user.email),
                          ),
                          ListTile(
                            title: const Text('Username'),
                            subtitle: Text(user.username),
                          ),
                          if (user.fullName != null)
                            ListTile(
                              title: const Text('Full Name'),
                              subtitle: Text(user.fullName!),
                            ),
                          ListTile(
                            title: const Text('Account Status'),
                            subtitle: Text(
                              user.isActive ? 'Active' : 'Inactive',
                              style: TextStyle(
                                color: user.isActive
                                    ? Colors.green
                                    : Colors.red,
                              ),
                            ),
                          ),
                          ListTile(
                            title: const Text('Verified'),
                            subtitle: Text(
                              user.isVerified ? 'Yes' : 'No',
                            ),
                          ),
                          ListTile(
                            title: const Text('Member Since'),
                            subtitle: Text(
                              _formatDate(user.createdAt),
                            ),
                          ),
                          if (user.lastLogin != null)
                            ListTile(
                              title: const Text('Last Login'),
                              subtitle: Text(
                                _formatDate(user.lastLogin!),
                              ),
                            ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Edit profile button
                  ElevatedButton.icon(
                    onPressed: () {
                      Navigator.of(context).pushNamed('/edit-profile');
                    },
                    icon: const Icon(Icons.edit),
                    label: const Text('Edit Profile'),
                  ),
                  const SizedBox(height: 12),

                  // Logout button
                  ElevatedButton.icon(
                    onPressed: () async {
                      final confirmed = await showDialog<bool>(
                        context: context,
                        builder: (context) => AlertDialog(
                          title: const Text('Logout'),
                          content:
                              const Text('Are you sure you want to logout?'),
                          actions: [
                            TextButton(
                              onPressed: () =>
                                  Navigator.pop(context, false),
                              child: const Text('Cancel'),
                            ),
                            TextButton(
                              onPressed: () =>
                                  Navigator.pop(context, true),
                              child: const Text('Logout'),
                            ),
                          ],
                        ),
                      );

                      if (confirmed ?? false) {
                        await ref.read(authProvider.notifier).logout();
                        if (context.mounted) {
                          Navigator.of(context)
                              .pushNamedAndRemoveUntil(
                            '/login',
                            (route) => false,
                          );
                        }
                      }
                    },
                    icon: const Icon(Icons.logout),
                    label: const Text('Logout'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      foregroundColor: Colors.white,
                    ),
                  ),
                ],
              ),
            ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }
}
```

---

## Navigation & Auth Guards

### Route Guard / Protected Routes

```dart
class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    return MaterialPageRoute(
      settings: settings,
      builder: (context) {
        return Consumer(
          builder: (context, ref, child) {
            final isAuthenticated = ref.watch(isAuthenticatedProvider);

            // Protected routes that require authentication
            final protectedRoutes = {
              '/home',
              '/profile',
              '/horoscope',
              '/readings',
            };

            final isProtectedRoute =
                protectedRoutes.contains(settings.name);

            // Redirect to login if accessing protected route while unauthenticated
            if (isProtectedRoute && !isAuthenticated) {
              return LoginScreen();
            }

            // Redirect to home if accessing login/signup while authenticated
            if ((settings.name == '/login' || settings.name == '/signup') &&
                isAuthenticated) {
              return const HomeScreen();
            }

            // Route mapping
            switch (settings.name) {
              case '/login':
                return const LoginScreen();
              case '/signup':
                return const SignupScreen();
              case '/home':
                return const HomeScreen();
              case '/profile':
                return const ProfileScreen();
              default:
                return Scaffold(
                  body: Center(
                    child: Text('No route defined for ${settings.name}'),
                  ),
                );
            }
          },
        );
      },
    );
  }
}
```

### Auth State Listener

```dart
class RootScreen extends ConsumerWidget {
  const RootScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);

    // Listen to auth state changes
    ref.listen(authProvider, (previous, next) {
      if (next is AuthStateUnauthenticated && previous is AuthStateAuthenticated) {
        // User was logged out
        Navigator.of(context).pushNamedAndRemoveUntil(
          '/login',
          (route) => false,
        );
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('You have been logged out')),
        );
      }
    });

    // Show appropriate screen based on auth state
    if (authState is AuthStateInitial || authState is AuthStateLoading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    } else if (authState is AuthStateAuthenticated) {
      return const HomeScreen();
    } else {
      return const LoginScreen();
    }
  }
}
```

---

## Error Handling Patterns

### Specific Exception Handling

```dart
Future<void> handleLoginError(BuildContext context, dynamic error) {
  if (error is InvalidCredentialsException) {
    return showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Login Failed'),
        content: const Text('Invalid email or password. Please try again.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  } else if (error is NetworkException) {
    return showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Network Error'),
        content:
            const Text('Unable to connect. Please check your internet.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              // Retry login
            },
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  } else if (error is UserAlreadyExistsException) {
    return showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Email Already Registered'),
        content: const Text(
          'This email is already registered. Please login instead.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Go to Login'),
          ),
        ],
      ),
    );
  } else {
    return showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Error'),
        content: Text('An error occurred: $error'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}
```

### Error Handling with Snackbar

```dart
class LoginScreenWithSnackbarErrors extends ConsumerStatefulWidget {
  const LoginScreenWithSnackbarErrors({Key? key}) : super(key: key);

  @override
  ConsumerState<LoginScreenWithSnackbarErrors> createState() =>
      _LoginScreenWithSnackbarErrorsState();
}

class _LoginScreenWithSnackbarErrorsState
    extends ConsumerState<LoginScreenWithSnackbarErrors> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();
    // Listen to auth errors
    _setupErrorListener();
  }

  void _setupErrorListener() {
    // Listen to error changes
    Future.microtask(() {
      ref.listen(authErrorProvider, (previous, next) {
        if (next != null) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(next),
              backgroundColor: Colors.red,
              duration: const Duration(seconds: 4),
            ),
          );
        }
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(
                hintText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: const InputDecoration(
                hintText: 'Password',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () async {
                try {
                  await ref.read(authProvider.notifier).login(
                    email: _emailController.text,
                    password: _passwordController.text,
                  );
                } catch (e) {
                  // Error already shown in snackbar via listener
                }
              },
              child: const Text('LOGIN'),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
```

---

## Advanced Usage

### Checking Token Before Making API Call

```dart
Future<void> fetchUserData() async {
  final authService = ref.read(authServiceProvider);

  // Check if token is still valid
  if (!authService.isTokenValid()) {
    try {
      // Try to refresh token
      await authService.refreshAccessToken();
    } on InvalidTokenException {
      // No refresh token - user must login again
      await ref.read(authProvider.notifier).logout();
      showLoginScreen();
      return;
    }
  }

  // Now safe to make API call - token is valid
  final response = await apiClient.get('/user/data');
  // ...
}
```

### Getting Token Expiry Information

```dart
class TokenExpiryIndicator extends ConsumerWidget {
  const TokenExpiryIndicator({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final expiryInfo = ref.watch(tokenExpiryProvider);
    final isSessionExpiring = ref.watch(isSessionExpiringProvider);

    if (expiryInfo == null) {
      return const SizedBox.shrink();
    }

    if (isSessionExpiring) {
      return Container(
        color: Colors.orange,
        padding: const EdgeInsets.all(8),
        child: Row(
          children: [
            const Icon(Icons.warning, color: Colors.white),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                'Session expiring in ${expiryInfo.timeRemaining.inMinutes} minutes',
                style: const TextStyle(color: Colors.white),
              ),
            ),
            ElevatedButton(
              onPressed: () async {
                try {
                  await ref
                      .read(authProvider.notifier)
                      .refreshAccessToken();
                } catch (e) {
                  // Handle error
                }
              },
              child: const Text('Extend'),
            ),
          ],
        ),
      );
    }

    return const SizedBox.shrink();
  }
}
```

### Auto-refresh Token Timer

```dart
class AutoTokenRefresh extends ConsumerStatefulWidget {
  final Widget child;

  const AutoTokenRefresh({
    Key? key,
    required this.child,
  }) : super(key: key);

  @override
  ConsumerState<AutoTokenRefresh> createState() => _AutoTokenRefreshState();
}

class _AutoTokenRefreshState extends ConsumerState<AutoTokenRefresh> {
  Timer? _refreshTimer;

  @override
  void initState() {
    super.initState();
    _scheduleTokenRefresh();
  }

  void _scheduleTokenRefresh() {
    _refreshTimer?.cancel();

    final authService = ref.read(authServiceProvider);
    final expiry = authService.getTokenExpiry();

    if (expiry != null) {
      // Refresh 5 minutes before expiry
      final refreshTime = expiry.subtract(const Duration(minutes: 5));
      final now = DateTime.now();

      if (refreshTime.isAfter(now)) {
        final duration = refreshTime.difference(now);
        _refreshTimer = Timer(duration, _performRefresh);
      } else {
        // Token expires soon, refresh immediately
        _performRefresh();
      }
    }
  }

  Future<void> _performRefresh() async {
    try {
      await ref.read(authProvider.notifier).refreshAccessToken();
      _scheduleTokenRefresh();
    } catch (e) {
      // Refresh failed, user will be logged out by AuthNotifier
    }
  }

  @override
  void dispose() {
    _refreshTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => widget.child;
}
```

---

## Summary

The AuthService provides flexible authentication that can be:
- Used directly from screens via Riverpod providers
- Integrated into state management
- Extended with custom logic
- Tested with mocks
- Combined with UI patterns for better UX

All examples follow the single responsibility principle and are compatible with the existing AuthService implementation.
