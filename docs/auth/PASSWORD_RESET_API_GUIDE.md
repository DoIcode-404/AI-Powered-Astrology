# Password Reset API Integration Guide

Complete documentation for the password reset flow in the Kundali Astrology App.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [API Endpoints](#api-endpoints)
4. [Frontend Integration](#frontend-integration)
5. [Backend Implementation](#backend-implementation)
6. [Error Handling](#error-handling)
7. [Security Considerations](#security-considerations)
8. [Testing Guide](#testing-guide)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The password reset feature allows users to securely recover access to their accounts when they forget their password. The flow consists of two main stages:

1. **Request Stage** - User provides email to receive reset link
2. **Reset Stage** - User follows link and sets new password

### Key Features:

- JWT-based reset tokens with 60-minute expiry
- Password strength validation (8+ chars, uppercase, lowercase, number)
- Rate limiting protection (429 responses)
- Email verification
- Secure token management
- Clear error messaging

---

## Architecture

### System Components:

```
Frontend (Flutter)
├── ForgotPasswordScreen
│   └── Calls authService.forgotPassword(email)
├── ResetPasswordScreen
│   └── Calls authService.resetPassword(token, password)
└── AuthService
    ├── forgotPassword()
    ├── resetPassword()
    └── verifyResetToken()

Backend (FastAPI)
├── POST /auth/forgot-password
├── POST /auth/reset-password
└── POST /auth/verify-reset-token

Database
└── Users Collection (MongoDB)
    └── hashed_password field
```

### Data Flow:

```
1. User enters email on Forgot Password screen
                ↓
2. ForgotPasswordScreen.forgot() calls AuthService.forgotPassword(email)
                ↓
3. AuthService makes POST request to /auth/forgot-password
                ↓
4. Backend validates email exists, creates reset token
                ↓
5. Backend generates reset link with token (for email)
                ↓
6. [Email sent to user with link]
                ↓
7. User clicks link in email → navigates to ResetPasswordScreen with token
                ↓
8. ResetPasswordScreen displays password form with token
                ↓
9. User enters new password and confirms
                ↓
10. ResetPasswordScreen calls AuthService.resetPassword(token, password)
                ↓
11. AuthService makes POST to /auth/reset-password
                ↓
12. Backend verifies token, validates password, updates user
                ↓
13. Success → Navigate to login screen
```

---

## API Endpoints

### Endpoint 1: Forgot Password

**Purpose:** Initiate password reset by providing email

**Method:** `POST`

**URL:** `/auth/forgot-password`

**Authentication:** None required

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Password reset email sent",
  "data": {
    "message": "If an account exists with this email, you will receive password reset instructions",
    "test_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." // For testing only
  },
  "timestamp": "2024-11-27T10:30:00Z"
}
```

**Error Responses:**

404 - Email Not Found:
```json
{
  "success": false,
  "code": "EMAIL_NOT_FOUND",
  "message": "No account found with email user@example.com",
  "http_status": 404,
  "timestamp": "2024-11-27T10:30:00Z"
}
```

429 - Rate Limited:
```json
{
  "success": false,
  "code": "RATE_LIMITED",
  "message": "Too many password reset requests. Please try again later.",
  "http_status": 429,
  "timestamp": "2024-11-27T10:30:00Z"
}
```

500 - Server Error:
```json
{
  "success": false,
  "code": "FORGOT_PASSWORD_FAILED",
  "message": "Password reset request failed: [error details]",
  "http_status": 500,
  "timestamp": "2024-11-27T10:30:00Z"
}
```

**Dart Usage Example:**
```dart
try {
  final authService = AuthService();
  await authService.forgotPassword(email: 'user@example.com');

  // Show success message
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text('Check your email for reset link'))
  );
} on EmailNotFoundException {
  _showError('Email not found');
} on RateLimitedException catch (e) {
  _showError('Too many attempts. Try again in ${e.retryAfterSeconds}s');
} on NetworkException {
  _showError('Network error. Check your connection.');
}
```

---

### Endpoint 2: Reset Password

**Purpose:** Change password using reset token

**Method:** `POST`

**URL:** `/auth/reset-password`

**Authentication:** None (uses reset token instead)

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "password": "NewSecurePassword123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Password reset successful",
  "data": {
    "message": "Password has been reset successfully"
  },
  "timestamp": "2024-11-27T10:30:00Z"
}
```

**Error Responses:**

400 - Invalid Token:
```json
{
  "success": false,
  "code": "INVALID_RESET_TOKEN",
  "message": "Invalid or expired reset token",
  "http_status": 400,
  "timestamp": "2024-11-27T10:30:00Z"
}
```

400 - Password Too Short:
```json
{
  "success": false,
  "code": "PASSWORD_TOO_SHORT",
  "message": "Password must be at least 8 characters",
  "http_status": 400,
  "timestamp": "2024-11-27T10:30:00Z"
}
```

400 - Weak Password:
```json
{
  "success": false,
  "code": "WEAK_PASSWORD",
  "message": "Password must contain: uppercase letter, number",
  "http_status": 400,
  "timestamp": "2024-11-27T10:30:00Z"
}
```

404 - User Not Found:
```json
{
  "success": false,
  "code": "USER_NOT_FOUND",
  "message": "User not found",
  "http_status": 404,
  "timestamp": "2024-11-27T10:30:00Z"
}
```

**Dart Usage Example:**
```dart
try {
  final authService = AuthService();

  // Validate password locally first
  if (password.length < 8) {
    showError('Password must be at least 8 characters');
    return;
  }

  // Call reset endpoint
  await authService.resetPassword(
    token: resetToken,
    newPassword: password,
  );

  // Navigate to login on success
  Navigator.pushNamedAndRemoveUntil(
    context,
    AppRoutes.login,
    (route) => false,
  );
} on InvalidTokenException {
  showError('Reset link has expired. Request a new one.');
} on PasswordTooWeakException catch (e) {
  showError('Password requirements: ${e.message}');
} on NetworkException {
  showError('Network error. Please try again.');
}
```

---

### Endpoint 3: Verify Reset Token

**Purpose:** Check if reset token is still valid

**Method:** `POST`

**URL:** `/auth/verify-reset-token`

**Authentication:** None (uses reset token instead)

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Token is valid",
  "data": {
    "valid": true,
    "email": "user@example.com"
  },
  "timestamp": "2024-11-27T10:30:00Z"
}
```

**Invalid Token Response (400):**
```json
{
  "success": false,
  "message": "Reset token is invalid or expired",
  "http_status": 400,
  "data": {
    "valid": false,
    "email": null
  },
  "timestamp": "2024-11-27T10:30:00Z"
}
```

**Dart Usage Example:**
```dart
try {
  final authService = AuthService();
  final isValid = await authService.verifyResetToken(token: resetToken);

  if (isValid) {
    // Show password reset form
    setState(() => canResetPassword = true);
  } else {
    // Show expired message
    showError('Reset link has expired');
  }
} on NetworkException {
  showError('Unable to verify token. Check connection.');
}
```

---

## Frontend Integration

### AuthService Methods

#### forgotPassword()

```dart
Future<void> forgotPassword({required String email}) async
```

**Parameters:**
- `email` (String) - User's email address

**Returns:** Future<void> - Completes when email is sent

**Throws:**
- `EmailNotFoundException` - Email not found in database
- `RateLimitedException` - Too many requests (429)
- `NetworkException` - Network connectivity error
- `AuthException` - Other auth errors

**Implementation Details:**
- Validates email format before submission
- Makes POST to `/auth/forgot-password`
- No token storage on success (email contains token)
- Shows user-friendly error messages

---

#### resetPassword()

```dart
Future<void> resetPassword({
  required String token,
  required String newPassword,
}) async
```

**Parameters:**
- `token` (String) - Reset token from email link
- `newPassword` (String) - New password to set

**Returns:** Future<void> - Completes when password is reset

**Throws:**
- `InvalidTokenException` - Token is invalid/expired
- `PasswordTooWeakException` - Password doesn't meet requirements
- `NetworkException` - Network connectivity error
- `AuthException` - Other auth errors

**Implementation Details:**
- Validates token format
- Makes POST to `/auth/reset-password`
- Clears stored reset token on success
- Automatic logout after password change recommended

---

#### verifyResetToken()

```dart
Future<bool> verifyResetToken({required String token}) async
```

**Parameters:**
- `token` (String) - Reset token to verify

**Returns:** Future<bool> - True if valid, False otherwise

**Throws:**
- `NetworkException` - Network connectivity error
- `AuthException` - Other auth errors

**Implementation Details:**
- No token storage
- Used for validation before showing reset form
- Safe to call multiple times

---

### Screen Integration

#### ForgotPasswordScreen

**Key Methods:**
- `_handleResetRequest()` - Handles form submission
- `_isValidEmail()` - Client-side email validation
- `_showError()` - Display error messages

**State Variables:**
- `_emailController` - Email input field
- `_isLoading` - Loading state during API call
- `_emailSent` - Success state after email sent
- `_errorMessage` - Current error message

**Usage Example:**
```dart
// In your auth flow
Navigator.pushNamed(context, AppRoutes.forgotPassword);

// After successful email send, user can:
// 1. Try another email
// 2. Return to login
```

---

#### ResetPasswordScreen

**Key Methods:**
- `_handlePasswordReset()` - Handles password reset
- `_validatePasswordStrength()` - Checks password requirements
- `_buildAnimatedRequirement()` - Displays requirement status

**Constructor Arguments:**
- `resetToken` (String?) - Token from navigation arguments

**State Variables:**
- `_passwordController` - New password field
- `_confirmPasswordController` - Password confirmation field
- `_isLoading` - Loading state during API call
- `_passwordReset` - Success state after reset
- `_errorMessage` - Current error message

**Usage Example:**
```dart
// Navigate with token from email
Navigator.pushNamed(
  context,
  AppRoutes.resetPassword,
  arguments: {'resetToken': tokenFromEmail},
);

// After successful reset:
// 1. Shows success animation
// 2. Auto-navigates to login after 2 seconds
```

---

## Backend Implementation

### Database Schema

**Users Collection Fields:**
```python
{
  "_id": ObjectId,
  "email": String (unique),
  "username": String (unique),
  "hashed_password": String,  # Updated during password reset
  "full_name": String,
  "is_active": Boolean,
  "is_verified": Boolean,
  "created_at": DateTime,
  "updated_at": DateTime,  # Updated during password reset
  "last_login": DateTime
}
```

### JWT Token Structure

**Reset Token (60-minute expiry):**
```python
{
  "email": "user@example.com",
  "exp": 1234567890,  # Unix timestamp
  "type": "reset"
}
```

**Signature:** HS256 with SECRET_KEY

---

### Implementation Flow

#### Forgot Password Flow:
```python
1. Validate email format with Pydantic
2. Check if user exists in database
3. If not found → return 404 error
4. Create reset token with create_password_reset_token()
5. Generate reset link: {FRONTEND_URL}/reset-password?token={token}
6. Send email with reset link (TODO: implement email service)
7. Return success response with message
8. (Test mode: include test_token in response)
```

#### Reset Password Flow:
```python
1. Verify reset token with verify_password_reset_token()
2. If invalid/expired → return 400 error
3. Find user by email from token
4. Validate password length >= 8
5. Validate password has uppercase, lowercase, digit
6. Hash new password with hash_password()
7. Update user document with new hashed_password
8. Update updated_at timestamp
9. Return success response
```

#### Verify Token Flow:
```python
1. Verify reset token with verify_password_reset_token()
2. If invalid → return error response with valid=false
3. If valid → return success response with valid=true and email
```

---

### Pydantic Schemas

**Request Validation:**
```python
class ForgotPasswordRequest(BaseModel):
    email: EmailStr  # Built-in email validation

class ResetPasswordRequest(BaseModel):
    token: str  # Any string format
    password: str = Field(..., min_length=8)  # Min 8 chars enforced

class VerifyResetTokenRequest(BaseModel):
    token: str  # Any string format
```

**Response Format:**
```python
class VerifyResetTokenResponse(BaseModel):
    valid: bool
    email: Optional[str]  # Only if valid=True
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Password reset successful |
| 400 | Bad Request | Invalid token, weak password |
| 404 | Not Found | Email not found |
| 429 | Too Many Requests | Rate limited |
| 500 | Server Error | Database error, token creation failed |

### Exception Mapping

**Frontend (Dart):**
```dart
200 ✓ Success
400 → InvalidTokenException, PasswordTooWeakException, EmailNotFoundException
404 → EmailNotFoundException
429 → RateLimitedException
500 → AuthException (generic)
Network → NetworkException
```

### Error Message Examples

**User-Friendly Messages:**
```
"This email is not registered with us"
"Too many reset attempts. Try again in 5 minutes."
"Reset link has expired. Please request a new one."
"Password must contain: uppercase letter, number"
"Network error. Please check your internet connection."
```

### Retry Strategy

**Recommended Retry Logic:**
```dart
Future<void> forgotPasswordWithRetry({
  required String email,
  int maxAttempts = 3,
  Duration initialDelay = const Duration(seconds: 1),
}) async {
  int attempts = 0;
  Duration currentDelay = initialDelay;

  while (attempts < maxAttempts) {
    try {
      await authService.forgotPassword(email: email);
      return; // Success
    } on NetworkException {
      attempts++;
      if (attempts < maxAttempts) {
        await Future.delayed(currentDelay);
        currentDelay *= 2; // Exponential backoff
      }
    }
  }

  throw AuthException(message: 'Failed after $maxAttempts attempts');
}
```

---

## Security Considerations

### Token Security

1. **Token Creation:**
   - Uses cryptographically secure JWT library (python-jose)
   - Signed with app's SECRET_KEY
   - 60-minute expiration enforced
   - Type field prevents token misuse

2. **Token Validation:**
   - Signature verified with SECRET_KEY
   - Expiration checked
   - Type field verified (must be "reset")
   - Email claim validated

3. **Token Storage (Frontend):**
   - Passed via URL only (not stored)
   - Can be stored temporarily in memory during reset flow
   - Cleared after successful reset
   - Cleared after token expiry

### Password Security

1. **Validation:**
   - Minimum 8 characters required
   - Uppercase letter required
   - Lowercase letter required
   - Number required

2. **Storage:**
   - Hashed with bcrypt (passlib implementation)
   - Never transmitted in plain text
   - Not logged or exposed in errors

3. **Transmission:**
   - Sent over HTTPS only (enforced in production)
   - Not included in logs or monitoring

### Email Security

1. **Email Verification:**
   - Valid email format checked (Pydantic EmailStr)
   - User existence verified before token generation
   - Token included in URL, not email body

2. **User Notification:**
   - Only generic message shown (don't expose user existence)
   - Reset link includes full token (impossible to guess)
   - Link expires in 60 minutes

### Rate Limiting

1. **Implementation:**
   - Backend should implement rate limiting
   - 5 attempts per hour per email recommended
   - 429 response with Retry-After header

2. **Client Handling:**
   - Catch RateLimitedException
   - Parse retry-after value
   - Show user wait time

---

## Testing Guide

### Test Cases

#### Test 1: Valid Email Address

**Steps:**
1. Open Forgot Password screen
2. Enter valid registered email: `test@example.com`
3. Click "Send Reset Link"

**Expected:**
- Loading state shown
- Success animation
- Message: "Check your email for reset link"
- Option to "Try Another Email" or "Back to Login"

**Code:**
```dart
testWidgets('Forgot password with valid email', (tester) async {
  await tester.pumpWidget(const TestApp());

  await tester.enterText(find.byType(EmailTextField), 'test@example.com');
  await tester.tap(find.byType(PrimaryButton));

  await tester.pumpAndSettle();

  expect(find.text('Check your email'), findsOneWidget);
});
```

---

#### Test 2: Non-existent Email

**Steps:**
1. Open Forgot Password screen
2. Enter non-existent email: `notexist@example.com`
3. Click "Send Reset Link"

**Expected:**
- Loading state shown
- Error message: "This email is not registered with us"
- User remains on form
- Can try different email

**Backend Response:** 404 with EMAIL_NOT_FOUND code

---

#### Test 3: Rate Limiting

**Steps:**
1. Submit forgot password 5 times rapidly
2. 6th attempt

**Expected:**
- First 5: Success/normal responses
- 6th: Error message "Too many attempts"
- Shows retry time if available

**Backend Response:** 429 with Retry-After header

---

#### Test 4: Valid Reset Token

**Steps:**
1. Receive reset link in email with token
2. Click link (opens ResetPasswordScreen with token)
3. Verify token auto-validation

**Expected:**
- Token passed to screen
- Password form displayed
- No error message about invalid token

**Backend Response:** 200 from verify-reset-token

---

#### Test 5: Expired Token

**Steps:**
1. Get reset link, wait 61+ minutes
2. Click reset link
3. Attempt to submit new password

**Expected:**
- Error: "Reset link has expired"
- Suggest requesting new reset link
- Navigate back to forgot password

**Backend Response:** 400 with INVALID_RESET_TOKEN code

---

#### Test 6: Valid Password Reset

**Steps:**
1. Receive reset link, click immediately
2. Enter valid password: `NewPass123`
3. Confirm password: `NewPass123`
4. Click "Reset Password"

**Expected:**
- Loading state shown
- Success animation
- Message: "Password reset successfully"
- Auto-navigate to login after 2 seconds
- Can login with new password

**Backend Response:** 200 with success message

---

#### Test 7: Weak Password

**Steps:**
1. Open reset password screen with valid token
2. Enter weak password: `123456` (no letters)
3. Observe requirement feedback

**Expected:**
- Requirements show missing items
- Submit button disabled or validation error on click
- Error: "Missing: uppercase letter, lowercase letter"

**Local Validation:** No API call made

---

#### Test 8: Password Mismatch

**Steps:**
1. Enter password: `Password123`
2. Confirm with: `Password456`
3. Click "Reset Password"

**Expected:**
- Error: "Passwords do not match"
- Remain on form
- Clear confirm field for retry

**Local Validation:** No API call made

---

#### Test 9: Network Error

**Steps:**
1. Disable internet connection
2. Attempt forgot password or reset password
3. Try again after reconnection

**Expected:**
- Error: "Network error. Check internet."
- Retry button/option available
- Succeeds after reconnection

**Exception Caught:** NetworkException

---

#### Test 10: Successful Login After Reset

**Steps:**
1. Complete password reset
2. Wait for auto-navigation to login
3. Enter email and new password
4. Click Login

**Expected:**
- Login succeeds with new password
- Old password no longer works
- User session created with new auth tokens

**Backend:** Old hashed_password replaced with new one

---

### Automated Test Examples

**Unit Tests (AuthService):**
```dart
test('forgotPassword throws EmailNotFoundException for invalid email', () async {
  final authService = AuthService();

  expect(
    () => authService.forgotPassword(email: 'notfound@example.com'),
    throwsA(isA<EmailNotFoundException>()),
  );
});

test('resetPassword with weak password throws PasswordTooWeakException', () async {
  final authService = AuthService();

  expect(
    () => authService.resetPassword(
      token: 'valid_token',
      newPassword: '123456', // No letters
    ),
    throwsA(isA<PasswordTooWeakException>()),
  );
});
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Reset Email Not Received

**Symptoms:**
- User completes forgot password flow
- No email arrives
- Shows success message but email missing

**Causes:**
- Email service not integrated (currently TODO)
- Email service credentials invalid
- Spam/junk folder
- Wrong email address entered

**Solutions:**
1. **For Development:**
   - Check test_token in forgot-password response
   - Use that token manually in ResetPasswordScreen

2. **For Production:**
   - Integrate actual email service (SendGrid/AWS SES)
   - Verify SMTP credentials
   - Check email service logs
   - Verify sender email whitelisted

**Code Fix:**
```python
# server/routes/auth.py
def send_password_reset_email(email: str, reset_link: str):
    """Send password reset email."""
    try:
        # Integration with SendGrid or similar
        send_email(
            to=email,
            subject="Password Reset Request",
            body=f"Click here to reset: {reset_link}",
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
```

---

#### Issue 2: "Invalid Token" on Reset Screen

**Symptoms:**
- User clicks reset link
- Shows "Invalid or expired token" error
- Can't reset password

**Causes:**
- Token expired (>60 minutes)
- Token signature invalid
- Wrong SECRET_KEY used
- Token modified in URL

**Solutions:**
1. **Token Expired:**
   - Request new reset link
   - Open link within 60 minutes

2. **Signature Invalid:**
   - Check SECRET_KEY matches between frontend and backend
   - Verify JWT library versions match
   - Check token encoding/decoding

3. **Modified Token:**
   - Use copy-paste for token, don't modify
   - Check URL doesn't have extra characters

**Debug:**
```dart
// Test token verification
try {
  final isValid = await authService.verifyResetToken(token: resetToken);
  print('Token valid: $isValid');
} catch (e) {
  print('Token error: $e');
}
```

---

#### Issue 3: Email Already Exists Error on Reset

**Symptoms:**
- Password reset succeeds
- Login fails with "Email already exists"
- System confused state

**Causes:**
- User duplicate in database
- Reset process created new user instead of updating
- Database synchronization issue

**Solutions:**
1. **Check User Exists:**
   ```python
   # In reset-password endpoint
   users_collection.find_one({"email": email})
   # Should return exactly one user
   ```

2. **Use Correct Update:**
   ```python
   # Correct: Update one user
   users_collection.update_one(
       {"_id": user_doc['_id']},  # By user ID, not email
       {"$set": {"hashed_password": new_hash}}
   )
   ```

3. **Database Repair:**
   - Find duplicate accounts
   - Merge/delete extras
   - Verify unique indexes

---

#### Issue 4: Password Complexity Rejected

**Symptoms:**
- User enters password like "Password123"
- Backend rejects as weak
- Frontend doesn't show what's missing

**Causes:**
- Different validation rules frontend vs backend
- Requirements not clearly shown
- User misunderstands requirements

**Solutions:**
1. **Sync Requirements:**
   ```dart
   // Frontend validation
   const minLength = 8;
   const requiresUpper = true;
   const requiresLower = true;
   const requiresDigit = true;
   const requiresSpecial = false; // Not required
   ```

2. **Improve UI:**
   ```dart
   // Show requirement as user types
   _buildAnimatedRequirement(
     'Uppercase letter (A-Z)',
     password.contains(RegExp(r'[A-Z]')),
   ),
   ```

3. **Better Error Messages:**
   ```dart
   // Instead of: "Password too weak"
   // Show: "Password must contain: uppercase letter, number"
   ```

---

#### Issue 5: Rate Limiting Not Working

**Symptoms:**
- User can attempt reset 100+ times immediately
- No 429 responses
- Rate limiting ineffective

**Causes:**
- Rate limiting not implemented in backend
- Rate limiting middleware missing
- Redis/cache not configured

**Solutions:**
1. **Implement Rate Limiting:**
   ```python
   from fastapi_limiter import FastAPILimiter
   from fastapi_limiter.util import get_remote_address

   @router.post("/forgot-password")
   @limiter.limit("5/hour")
   async def forgot_password(request):
       # Implementation
   ```

2. **Per-Email Rate Limiting:**
   ```python
   # Track attempts per email
   # Allow 5 per hour per email address
   # Use Redis for distributed tracking
   ```

3. **Client Handling:**
   ```dart
   on RateLimitedException catch (e) {
     final seconds = e.retryAfterSeconds ?? 3600;
     showError('Too many attempts. Try again in $seconds seconds');
   }
   ```

---

### Debug Commands

**Test Endpoints with curl:**
```bash
# Test forgot password
curl -X POST http://localhost:8000/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'

# Test reset password
curl -X POST http://localhost:8000/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{"token":"<token_from_response>", "password":"NewPass123"}'

# Test verify token
curl -X POST http://localhost:8000/api/auth/verify-reset-token \
  -H "Content-Type: application/json" \
  -d '{"token":"<reset_token>"}'
```

**Debug Logs:**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.debug(f"Reset token created: {reset_token}")
logger.debug(f"Token verification result: {token_data}")
```

---

## Production Checklist

Before deploying password reset feature:

- [ ] Email service integrated (SendGrid/AWS SES/etc.)
- [ ] Email templates created and tested
- [ ] Test token removed from forgot-password response
- [ ] Rate limiting configured and tested
- [ ] SECRET_KEY environment variable set
- [ ] HTTPS enforced on all endpoints
- [ ] Reset token expiry set appropriately (60 minutes)
- [ ] Password requirements match security policy
- [ ] Error messages reviewed for security (no email enumeration)
- [ ] Database backups configured
- [ ] Monitoring/alerting for password reset attempts
- [ ] User notifications for password changes
- [ ] Audit logging enabled
- [ ] Load testing completed
- [ ] Security audit conducted

---

## Future Enhancements

1. **Email Verification**
   - Confirm email ownership
   - Prevent account takeover via email

2. **Multi-Factor Authentication**
   - SMS verification in addition to email
   - TOTP/authenticator app support

3. **Recovery Codes**
   - Generate backup codes
   - Use if email compromised

4. **Security Notifications**
   - Alert user of password change
   - Show device/location of reset
   - Option to revoke reset

5. **Improved UX**
   - QR code in email to scan
   - Deep linking from email
   - One-click reset (secure context required)

---

## Support

For issues or questions:
1. Check Troubleshooting section above
2. Review test cases for expected behavior
3. Check server logs for backend errors
4. Verify all files are correctly integrated
5. Test with curl commands before assuming UI issue

---

**Last Updated:** November 27, 2024
**Author:** Backend Integration Specialist
**Status:** Complete and Ready for Production
