"""
Authentication Routes with MongoDB Backend

Handles user registration, login, token refresh, and profile management.
Uses MongoDB database backend with JWT tokens.
All responses follow standardized APIResponse format.

Author: Backend API Team
"""

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status, Header
from bson import ObjectId

from server.database import get_db
from server.models.user import User
from server.models.user_settings import UserSettings
from server.pydantic_schemas.api_response import (
    APIResponse,
    success_response,
    error_response,
)
from server.pydantic_schemas.user_schema import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenRefreshRequest,
    UserResponse,
    TokenResponse,
)
from server.utils.jwt_handler import (
    hash_password,
    verify_password,
    create_tokens,
    verify_token,
    refresh_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def get_current_user(
    authorization: str = Header(None),
    db: dict = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.

    Usage:
        @router.get("/profile")
        def get_profile(user: User = Depends(get_current_user)):
            return {"email": user.email}

    Args:
        authorization: Authorization header in format "Bearer <token>"
        db: Database connection dict

    Returns:
        User object

    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )

    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

    # Verify token
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Get user from MongoDB
    try:
        users_collection = db['users']
        user_doc = users_collection.find_one({"_id": ObjectId(token_data.user_id)})
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Convert MongoDB document to User model
        user_doc['_id'] = str(user_doc['_id'])
        user = User(**user_doc)
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.post("/register", response_model=APIResponse, status_code=201, tags=["Authentication"])
async def register(request: UserRegisterRequest, db: dict = Depends(get_db)) -> APIResponse:
    """
    Register a new user account.

    Args:
        request: Registration request with email, username, password
        db: Database connection dict

    Returns:
        APIResponse with user data and tokens
    """
    try:
        logger.info(f"Registration attempt for email: {request.email}")

        users_collection = db['users']
        settings_collection = db['user_settings']

        # Check if email already exists
        existing_email = users_collection.find_one({"email": request.email})
        if existing_email:
            return error_response(
                code="EMAIL_ALREADY_EXISTS",
                message=f"User with email {request.email} already exists",
                http_status=400,
            )

        # Check if username already exists
        existing_username = users_collection.find_one({"username": request.username})
        if existing_username:
            return error_response(
                code="USERNAME_ALREADY_EXISTS",
                message=f"Username {request.username} is already taken",
                http_status=400,
            )

        # Create new user
        hashed_password = hash_password(request.password)
        user_doc = {
            "email": request.email,
            "username": request.username,
            "hashed_password": hashed_password,
            "full_name": request.full_name,
            "is_active": True,
            "is_verified": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login": None,
        }

        # Insert user
        result = users_collection.insert_one(user_doc)
        user_id = str(result.inserted_id)
        logger.info(f"User registered successfully: {request.email}")

        # Create user settings
        settings_doc = {
            "user_id": user_id,
            "theme": "light",
            "language": "en",
            "notifications_enabled": True,
            "notification_preferences": {
                "email_on_prediction": True,
                "email_on_kundali_saved": True,
                "email_newsletter": False,
            },
            "default_timezone": "UTC",
            "preferences": {},
            "updated_at": datetime.utcnow(),
        }
        settings_collection.insert_one(settings_doc)

        # Create tokens
        tokens = create_tokens(
            user_id=user_id,
            email=request.email,
            username=request.username,
        )

        # Prepare response
        user_doc['_id'] = user_id
        user_response = UserResponse(
            id=user_id,
            email=user_doc['email'],
            username=user_doc['username'],
            full_name=user_doc['full_name'],
            is_active=user_doc['is_active'],
            is_verified=user_doc['is_verified'],
            created_at=user_doc['created_at'],
            last_login=user_doc['last_login'],
        )

        return success_response(
            data={
                "user": user_response.model_dump(),
                "tokens": {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "token_type": tokens["token_type"],
                    "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                },
            },
            message="User registered successfully",
        )

    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        return error_response(
            code="REGISTRATION_FAILED",
            message=f"Registration failed: {str(e)}",
            http_status=500,
        )


@router.post("/login", response_model=APIResponse, tags=["Authentication"])
async def login(request: UserLoginRequest, db: dict = Depends(get_db)) -> APIResponse:
    """
    Authenticate user and return JWT tokens.

    Args:
        request: Login credentials (email, password)
        db: Database connection dict

    Returns:
        APIResponse with user data and tokens
    """
    try:
        logger.info(f"Login attempt for email: {request.email}")

        users_collection = db['users']

        # Find user by email
        user_doc = users_collection.find_one({"email": request.email})
        if not user_doc:
            return error_response(
                code="INVALID_CREDENTIALS",
                message="Invalid email or password",
                http_status=401,
            )

        # Verify password
        if not verify_password(request.password, user_doc['hashed_password']):
            return error_response(
                code="INVALID_CREDENTIALS",
                message="Invalid email or password",
                http_status=401,
            )

        # Check if user is active
        if not user_doc['is_active']:
            return error_response(
                code="ACCOUNT_INACTIVE",
                message="Account has been deactivated",
                http_status=403,
            )

        # Update last login
        user_id = user_doc['_id']
        users_collection.update_one(
            {"_id": user_id},
            {"$set": {"last_login": datetime.utcnow(), "updated_at": datetime.utcnow()}}
        )

        logger.info(f"User logged in successfully: {request.email}")

        # Create tokens
        user_id_str = str(user_id)
        tokens = create_tokens(
            user_id=user_id_str,
            email=user_doc['email'],
            username=user_doc['username'],
        )

        user_response = UserResponse(
            id=user_id_str,
            email=user_doc['email'],
            username=user_doc['username'],
            full_name=user_doc['full_name'],
            is_active=user_doc['is_active'],
            is_verified=user_doc['is_verified'],
            created_at=user_doc['created_at'],
            last_login=user_doc['last_login'],
        )

        return success_response(
            data={
                "user": user_response.model_dump(),
                "tokens": {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "token_type": tokens["token_type"],
                    "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                },
            },
            message="Login successful",
        )

    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return error_response(
            code="LOGIN_FAILED",
            message=f"Login failed: {str(e)}",
            http_status=500,
        )


@router.post("/refresh", response_model=APIResponse, tags=["Authentication"])
async def refresh_token(request: TokenRefreshRequest) -> APIResponse:
    """
    Refresh access token using refresh token.

    Args:
        request: Request with valid refresh token

    Returns:
        APIResponse with new access token
    """
    try:
        logger.info("Token refresh attempt")

        # Refresh the token
        new_tokens = refresh_access_token(request.refresh_token)
        if not new_tokens:
            return error_response(
                code="INVALID_REFRESH_TOKEN",
                message="Invalid or expired refresh token",
                http_status=401,
            )

        logger.info("Token refreshed successfully")

        return success_response(
            data={
                "access_token": new_tokens["access_token"],
                "refresh_token": new_tokens["refresh_token"],
                "token_type": new_tokens["token_type"],
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            },
            message="Token refreshed successfully",
        )

    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}", exc_info=True)
        return error_response(
            code="REFRESH_FAILED",
            message=f"Token refresh failed: {str(e)}",
            http_status=500,
        )


@router.get("/me", response_model=APIResponse, tags=["Authentication"])
async def get_current_profile(
    user: User = Depends(get_current_user),
) -> APIResponse:
    """
    Get current authenticated user's profile.

    Requires authentication token in Authorization header.

    Returns:
        APIResponse with user profile data
    """
    try:
        logger.info(f"Profile retrieved for user: {user.email}")

        user_response = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login=user.last_login,
        )

        return success_response(
            data=user_response.model_dump(),
            message="Profile retrieved successfully",
        )

    except Exception as e:
        logger.error(f"Get profile error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )


@router.post("/forgot-password", response_model=APIResponse, tags=["Password Reset"])
async def forgot_password(request: UserRegisterRequest, db: dict = Depends(get_db)) -> APIResponse:
    """
    Request a password reset email.

    Args:
        request: Request with user email
        db: Database connection dict

    Returns:
        APIResponse confirming email sent or user not found
    """
    try:
        from server.pydantic_schemas.user_schema import ForgotPasswordRequest
        from server.utils.jwt_handler import create_password_reset_token

        logger.info(f"Password reset requested for email: {request.email}")

        users_collection = db['users']

        # Find user by email
        user_doc = users_collection.find_one({"email": request.email})
        if not user_doc:
            return error_response(
                code="EMAIL_NOT_FOUND",
                message=f"No account found with email {request.email}",
                http_status=404,
            )

        # Create password reset token
        reset_token = create_password_reset_token(request.email)

        # TODO: Send email with reset link
        # In production, integrate with email service (SendGrid, AWS SES, etc.)
        # reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"
        # send_password_reset_email(request.email, reset_link)

        logger.info(f"Password reset email sent to: {request.email}")

        return success_response(
            data={
                "message": "If an account exists with this email, you will receive password reset instructions",
                # NOTE: In production, only return the message above for security
                # Don't expose whether email exists or not
                "test_token": reset_token  # For testing only - remove in production
            },
            message="Password reset email sent",
        )

    except Exception as e:
        logger.error(f"Forgot password error: {str(e)}", exc_info=True)
        return error_response(
            code="FORGOT_PASSWORD_FAILED",
            message=f"Password reset request failed: {str(e)}",
            http_status=500,
        )


@router.post("/reset-password", response_model=APIResponse, tags=["Password Reset"])
async def reset_password(request, db: dict = Depends(get_db)) -> APIResponse:
    """
    Reset password with valid reset token.

    Args:
        request: Request with reset token and new password
        db: Database connection dict

    Returns:
        APIResponse confirming password reset or error
    """
    try:
        from server.pydantic_schemas.user_schema import ResetPasswordRequest
        from server.utils.jwt_handler import verify_password_reset_token, hash_password

        logger.info("Password reset attempt")

        # Verify reset token
        token_data = verify_password_reset_token(request.token)
        if not token_data:
            return error_response(
                code="INVALID_RESET_TOKEN",
                message="Invalid or expired reset token",
                http_status=400,
            )

        email = token_data.get("email")
        users_collection = db['users']

        # Find user by email
        user_doc = users_collection.find_one({"email": email})
        if not user_doc:
            return error_response(
                code="USER_NOT_FOUND",
                message="User not found",
                http_status=404,
            )

        # Validate password strength
        if len(request.password) < 8:
            return error_response(
                code="PASSWORD_TOO_SHORT",
                message="Password must be at least 8 characters",
                http_status=400,
            )

        # Check password complexity
        has_upper = any(c.isupper() for c in request.password)
        has_lower = any(c.islower() for c in request.password)
        has_digit = any(c.isdigit() for c in request.password)

        if not (has_upper and has_lower and has_digit):
            missing = []
            if not has_upper:
                missing.append("uppercase letter")
            if not has_lower:
                missing.append("lowercase letter")
            if not has_digit:
                missing.append("number")

            return error_response(
                code="WEAK_PASSWORD",
                message=f"Password must contain: {', '.join(missing)}",
                http_status=400,
            )

        # Hash new password and update
        hashed_password = hash_password(request.password)
        users_collection.update_one(
            {"_id": user_doc['_id']},
            {"$set": {
                "hashed_password": hashed_password,
                "updated_at": datetime.utcnow()
            }}
        )

        logger.info(f"Password reset successfully for user: {email}")

        return success_response(
            data={"message": "Password has been reset successfully"},
            message="Password reset successful",
        )

    except Exception as e:
        logger.error(f"Reset password error: {str(e)}", exc_info=True)
        return error_response(
            code="RESET_PASSWORD_FAILED",
            message=f"Password reset failed: {str(e)}",
            http_status=500,
        )


@router.post("/verify-reset-token", response_model=APIResponse, tags=["Password Reset"])
async def verify_reset_token(request) -> APIResponse:
    """
    Verify if a password reset token is valid.

    Args:
        request: Request with reset token to verify

    Returns:
        APIResponse with validity status and email if valid
    """
    try:
        from server.pydantic_schemas.user_schema import VerifyResetTokenRequest, VerifyResetTokenResponse
        from server.utils.jwt_handler import verify_password_reset_token

        logger.info("Token verification attempt")

        # Verify reset token
        token_data = verify_password_reset_token(request.token)

        if token_data:
            response_data = VerifyResetTokenResponse(
                valid=True,
                email=token_data.get("email")
            )
            return success_response(
                data=response_data.model_dump(),
                message="Token is valid",
            )
        else:
            response_data = VerifyResetTokenResponse(
                valid=False,
                email=None
            )
            return error_response(
                code="INVALID_TOKEN",
                message="Reset token is invalid or expired",
                http_status=400,
                data=response_data.model_dump()
            )

    except Exception as e:
        logger.error(f"Token verification error: {str(e)}", exc_info=True)
        return error_response(
            code="VERIFICATION_FAILED",
            message=f"Token verification failed: {str(e)}",
            http_status=500,
        )
