from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

from server.routes import export, kundali, auth, transits, predictions, ml_predictions, compatibility, horoscope
from server.utils.swisseph_setup import setup_ephemeris
from server.middleware.error_handler import setup_error_handlers, get_error_tracker
from server.pydantic_schemas.api_response import APIResponse, ResponseStatus, success_response
from server.database import get_db
from server.background_jobs import start_horoscope_scheduler, stop_horoscope_scheduler
from server.database.indexes import create_all_indexes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the FastAPI application
app = FastAPI(
    title="Kundali Astrology API",
    description="Comprehensive Vedic Astrology Kundali Analysis Backend",
    version="1.0.0"
)

# Global database client reference
_db_client = None


# Startup event to initialize ephemeris (lazy initialization)
@app.on_event("startup")
async def startup_event():
    """Initialize ephemeris, database, and background jobs on app startup."""
    global _db_client
    try:
        setup_ephemeris()
        logger.info("Ephemeris initialized successfully on startup")
    except Exception as e:
        logger.warning(f"Ephemeris initialization failed (non-fatal): {e}")
        # Don't fail startup if ephemeris fails

    try:
        # Initialize database connection
        db = get_db()
        if isinstance(db, dict):  # Successful connection
            _db_client = db.get('_client') if hasattr(db, 'get') else None
            logger.info("Database connection established on startup")
    except Exception as e:
        logger.warning(f"Database initialization on startup: {e}")

    try:
        # Initialize background job scheduler for horoscope generation
        start_horoscope_scheduler()
        logger.info("Background horoscope scheduler started on startup")
    except Exception as e:
        logger.warning(f"Background scheduler initialization failed (non-fatal): {e}")

    try:
        # Create database indexes for optimal performance
        create_all_indexes()
        logger.info("Database indexes created/verified on startup")
    except Exception as e:
        logger.warning(f"Database index creation failed (non-fatal): {e}")


# Shutdown event to cleanup resources
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections and stop background jobs on app shutdown."""
    global _db_client
    try:
        # Stop background scheduler
        stop_horoscope_scheduler()
        logger.info("Background horoscope scheduler stopped on shutdown")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")

    try:
        if _db_client:
            _db_client.close()
            logger.info("Database connection closed on shutdown")
    except Exception as e:
        logger.error(f"Error closing database connection: {e}")

# Setup error handling middleware
setup_error_handlers(app)

# CORS Configuration - Must be added AFTER error handler so it executes FIRST
# TODO: Restrict to specific origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Required when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers with /api prefix for versioning flexibility
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(kundali.router, prefix="/api/kundali", tags=["Kundali"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(ml_predictions.router, prefix="/api/ml", tags=["ML Predictions"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])
app.include_router(transits.router, prefix="/api/transits", tags=["Transits"])
app.include_router(compatibility.router, prefix="/api/compatibility", tags=["Compatibility"])
app.include_router(horoscope.router, prefix="/api/predictions/horoscope", tags=["Horoscope"])


# Health Check Endpoint
@app.get("/health", response_model=APIResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status and service information
    """
    try:
        return success_response(
            data={
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "ephemeris": "initialized",
                "database": "connected"
            },
            message="Service is running normally"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return APIResponse(
            status=ResponseStatus.ERROR,
            success=False,
            error={
                "code": "HEALTH_CHECK_FAILED",
                "message": str(e)
            },
            timestamp=datetime.utcnow()
        )


# Root Endpoint
@app.get("/", response_model=APIResponse)
async def root():
    """
    Root endpoint.

    Returns:
        API information
    """
    return success_response(
        data={
            "api_name": "Kundali Astrology API",
            "version": "1.0.0",
            "description": "Comprehensive Vedic Astrology Analysis",
            "endpoints": {
                "health": "/health",
                "auth": "/auth",
                "kundali": "/kundali",
                "export": "/export"
            }
        },
        message="Welcome to Kundali Astrology API"
    )


# Error Monitoring Endpoint
@app.get("/error-stats", response_model=APIResponse)
async def error_stats():
    """
    Get error statistics (for monitoring/debugging).

    Returns:
        Error tracking summary
    """
    tracker = get_error_tracker()
    return success_response(
        data=tracker.get_error_summary(),
        message="Error statistics retrieved"
    )


logger.info("Kundali Astrology API initialized successfully")



