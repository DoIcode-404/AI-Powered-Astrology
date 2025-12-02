# main.dart - AuthService Initialization Setup

## Overview

This document explains how `main.dart` is configured to initialize and manage the authentication service for the Kundali Astrology application.

## Initialization Flow

### Step 1: Flutter Binding
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Ensures Flutter is ready before running app
}
```

### Step 2: Initialize API Client
```dart
final apiClient = ApiClient();
apiClient.init(
  baseUrl: 'http://localhost:8000/api',
  connectTimeout: const Duration(seconds: 30),
  receiveTimeout: const Duration(seconds: 30),
);
```

**Purpose**: Sets up Dio HTTP client for API communication
- **Development URL**: `http://localhost:8000/api`
- **Production URL**: Update to your production server
- **Timeouts**: 30 seconds for both connect and receive operations

### Step 3: Initialize SharedPreferences
```dart
final sharedPreferences = await SharedPreferences.getInstance();
```

**Purpose**: Initializes local storage for:
- Access tokens
- Refresh tokens
- User session data
- Authentication state persistence

### Step 4: Initialize AuthService
```dart
final authService = AuthService();
await authService.init(
  apiClient: apiClient,
  preferences: sharedPreferences,
);
```

**Purpose**: Initializes the central authentication service with:
- **API Client**: For making HTTP requests
- **SharedPreferences**: For storing tokens and session data

### Step 5: Wrap App with Riverpod ProviderScope
```dart
runApp(
  ProviderScope(
    child: DevicePreview(
      builder: (context) => KundaliApp(authService: authService),
    ),
  ),
);
```

**Purpose**:
- `ProviderScope`: Enables Riverpod state management across the entire app
- `DevicePreview`: Development tool for previewing app on different devices
- `authService`: Passed to KundaliApp for initialization

## What Happens After Initialization

### Session Loading
When `authService.init()` completes:
1. Any stored tokens are loaded from SharedPreferences
2. If valid tokens exist, the user is considered authenticated
3. If tokens are expired, AuthService attempts automatic refresh
4. Auth state is updated accordingly

### Token Management
The AuthService automatically handles:
- Storing new tokens after login
- Refreshing expired access tokens (before expiry)
- Clearing tokens on logout
- Retrying requests with fresh tokens if needed

### Navigation Routing
The Splash Screen detects authentication state:
- **Authenticated**: Routes to Dashboard
- **Not Authenticated**: Routes to Login
- **Loading**: Shows loading spinner during initialization

## Backend Configuration

### Environment Setup

**Development**:
```dart
baseUrl: 'http://localhost:8000/api'
```

**Production**:
```dart
baseUrl: 'https://your-production-api.com/api'
```

### Required Backend Endpoints

The backend must provide these endpoints:

```
POST   /auth/login              - User login
POST   /auth/signup             - User registration
POST   /auth/refresh-token      - Refresh access token
POST   /auth/logout             - User logout
GET    /auth/me                 - Get current user info
POST   /auth/forgot-password    - Initiate password reset
POST   /auth/reset-password     - Complete password reset
POST   /auth/verify-reset-token - Verify reset token
```

## Token Lifecycle

### Login Flow
1. User enters credentials on LoginScreen
2. Screen calls: `ref.read(authProvider.notifier).login(email, password)`
3. AuthNotifier calls: `authService.login(email, password)`
4. AuthService makes POST to `/auth/login`
5. Backend returns `accessToken` and `refreshToken`
6. Tokens stored in SharedPreferences
7. AuthNotifier updates state to Authenticated
8. UI navigates to Dashboard

### Automatic Token Refresh
1. AuthNotifier detects token expiring within 5 minutes
2. Automatically calls: `authService.refreshAccessToken()`
3. AuthService makes POST to `/auth/refresh-token` with refresh token
4. Backend returns new `accessToken`
5. New token stored in SharedPreferences
6. All subsequent requests use fresh token
7. User experience: seamless, no interruption

### Logout Flow
1. User taps logout button
2. Screen calls: `ref.read(authProvider.notifier).logout()`
3. AuthNotifier calls: `authService.logout()`
4. AuthService clears all tokens from SharedPreferences
5. AuthNotifier updates state to Unauthenticated
6. UI navigates to Login screen

## Configuration Updates

### For Local Development
```dart
apiClient.init(
  baseUrl: 'http://localhost:8000/api',  // Your local backend
  connectTimeout: const Duration(seconds: 30),
  receiveTimeout: const Duration(seconds: 30),
);
```

Make sure your Flask/Python backend is running on port 8000.

### For Production Deployment
1. Update baseUrl to production server:
   ```dart
   baseUrl: 'https://your-production-api.com/api'
   ```

2. Update timeouts if needed (currently 30 seconds):
   ```dart
   connectTimeout: const Duration(seconds: 60),  // Increase if needed
   receiveTimeout: const Duration(seconds: 60),
   ```

3. Ensure CORS is configured on backend to allow your app's domain

## Debugging

### Check Initialization Status
The Splash Screen shows initialization status via `authService.isAuthenticated`:
- If true: User was previously logged in and tokens are valid
- If false: User is not logged in or tokens expired

### View Stored Tokens
SharedPreferences stores tokens under these keys:
- `auth_access_token` - Current access token
- `auth_refresh_token` - Refresh token for getting new access tokens
- `auth_user_data` - Current user information

### Common Issues

**Issue**: App always shows login screen even after login
- **Cause**: Tokens not being stored properly
- **Fix**: Check SharedPreferences is initialized before AuthService

**Issue**: Token refresh not working
- **Cause**: Backend refresh token endpoint not implemented
- **Fix**: Ensure `/auth/refresh-token` endpoint is available on backend

**Issue**: Long initialization delay
- **Cause**: Backend timeout
- **Fix**: Reduce `connectTimeout` and `receiveTimeout`, or check backend is running

## Related Files

- **Auth Service**: `client/lib/data/services/auth_service.dart`
- **API Client**: `client/lib/data/services/api_client.dart`
- **Auth Provider**: `client/lib/presentation/providers/auth_provider.dart`
- **Splash Screen**: `client/lib/presentation/screens/splash_screen.dart`
- **Login Screen**: `client/lib/presentation/screens/auth/login_screen.dart`

## Next Steps

1. Update `baseUrl` to match your backend server
2. Ensure all required auth endpoints are implemented on backend
3. Test login flow with local backend
4. Deploy and update production URL when ready
5. Monitor token refresh in production for any issues

---

**Last Updated**: November 2024
**Status**: Production Ready
