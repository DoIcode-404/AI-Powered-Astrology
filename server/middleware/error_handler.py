"""
Error Handling Middleware
Provides comprehensive error handling and standardized error responses.

Catches all exceptions and returns consistent error responses.
Includes error tracking, logging, and user-friendly messages.

Author: Backend API Team
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import ValidationError
import logging
import traceback
import uuid
from datetime import datetime
from typing import Callable, Optional

from server.pydantic_schemas.api_response import (
    APIResponse,
    ErrorDetail,
    ResponseStatus,
    error_response,
    validation_error_response
)

logger = logging.getLogger(__name__)


class ErrorTracker:
    """Track errors for monitoring and analytics."""

    def __init__(self):
        self.errors = []
        self.error_counts = {}

    def log_error(
        self,
        error_code: str,
        message: str,
        request_path: str,
        error_type: str,
        status_code: int,
        details: Optional[dict] = None
    ):
        """Log an error occurrence."""
        error_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'error_code': error_code,
            'message': message,
            'request_path': request_path,
            'error_type': error_type,
            'status_code': status_code,
            'details': details
        }

        self.errors.append(error_entry)
        self.error_counts[error_code] = self.error_counts.get(error_code, 0) + 1

        # Keep only last 1000 errors
        if len(self.errors) > 1000:
            self.errors = self.errors[-1000:]

    def get_error_summary(self) -> dict:
        """Get error summary statistics."""
        return {
            'total_errors': len(self.errors),
            'unique_error_types': len(self.error_counts),
            'error_counts': self.error_counts,
            'recent_errors': self.errors[-10:]  # Last 10 errors
        }


# Global error tracker instance
error_tracker = ErrorTracker()


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.

    Catches all exceptions and returns standardized error responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        """
        Process request and handle any errors.

        Args:
            request: HTTP request
            call_next: Next middleware/handler

        Returns:
            Response or error response
        """
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        try:
            response = await call_next(request)
            return response

        except ValidationError as e:
            logger.warning(f"Validation error in {request.url.path}: {str(e)}")

            errors = [
                {
                    "field": err.get("loc", [None])[-1],
                    "message": err.get("msg", "Validation failed"),
                    "type": err.get("type")
                }
                for err in e.errors()
            ]

            error_tracker.log_error(
                error_code="VALIDATION_ERROR",
                message="Request validation failed",
                request_path=str(request.url.path),
                error_type="ValidationError",
                status_code=422,
                details={"validation_errors": errors}
            )

            return validation_error_response(errors, request_id)

        except ValueError as e:
            logger.warning(f"Value error in {request.url.path}: {str(e)}")

            error_tracker.log_error(
                error_code="VALUE_ERROR",
                message=str(e),
                request_path=str(request.url.path),
                error_type="ValueError",
                status_code=400
            )

            return error_response(
                code="VALUE_ERROR",
                message=str(e),
                request_id=request_id,
                http_status=400
            )

        except Exception as e:
            logger.error(
                f"Unhandled exception in {request.url.path}: {str(e)}",
                exc_info=True
            )

            # Extract error information
            error_type = type(e).__name__
            error_message = str(e) if str(e) else f"An unexpected {error_type} occurred"

            # Determine status code based on exception type
            status_code = self._get_status_code_for_exception(e)

            # Log to error tracker
            error_tracker.log_error(
                error_code=error_type,
                message=error_message,
                request_path=str(request.url.path),
                error_type=error_type,
                status_code=status_code,
                details={
                    "traceback": traceback.format_exc()
                }
            )

            # Return standardized error response
            return error_response(
                code=error_type,
                message=error_message,
                status=ResponseStatus.SERVER_ERROR,
                request_id=request_id,
                http_status=status_code
            )

    @staticmethod
    def _get_status_code_for_exception(exception: Exception) -> int:
        """
        Determine HTTP status code based on exception type.

        Args:
            exception: The exception that occurred

        Returns:
            HTTP status code
        """
        error_type = type(exception).__name__

        status_code_map = {
            'FileNotFoundError': 404,
            'NotFoundError': 404,
            'PermissionError': 403,
            'AuthenticationError': 401,
            'UnauthorizedError': 401,
            'ValueError': 400,
            'TypeError': 400,
            'ValidationError': 422,
            'TimeoutError': 504,
            'ConnectionError': 503,
        }

        return status_code_map.get(error_type, 500)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add request IDs for tracking.

    Generates unique request IDs and includes them in responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        """
        Add request ID to request and response.

        Args:
            request: HTTP request
            call_next: Next middleware/handler

        Returns:
            Response with request ID header
        """
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all requests and responses.

    Logs request details and response status for monitoring.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        """
        Log request and response details.

        Args:
            request: HTTP request
            call_next: Next middleware/handler

        Returns:
            Response from next handler
        """
        request_id = getattr(request.state, 'request_id', 'unknown')

        # Log request
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        try:
            response = await call_next(request)

            # Log response
            logger.info(
                f"[{request_id}] Response: {response.status_code}"
            )

            return response

        except Exception as e:
            logger.error(
                f"[{request_id}] Request failed with error: {str(e)}"
            )
            raise


def setup_error_handlers(app):
    """
    Setup all error handling middleware for FastAPI app.

    Args:
        app: FastAPI application instance
    """
    # Add middleware in reverse order of execution
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(RequestIdMiddleware)


def get_error_tracker() -> ErrorTracker:
    """Get the global error tracker instance."""
    return error_tracker
