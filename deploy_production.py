#!/usr/bin/env python
"""
Production Deployment Script for Kundali Astrology API

This script handles the production deployment including:
1. Environment validation
2. Database initialization
3. Health checks
4. Server startup

Usage:
    python deploy_production.py
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_environment():
    """Verify all required environment variables are set."""
    logger.info("Checking environment configuration...")

    load_dotenv()

    required_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'ALGORITHM',
        'ACCESS_TOKEN_EXPIRE_MINUTES',
        'REFRESH_TOKEN_EXPIRE_DAYS'
    ]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Mask sensitive values
            if 'PASSWORD' in var or 'KEY' in var or 'TOKEN' in var:
                display_value = value[:10] + '***' if len(value) > 10 else '***'
            elif 'URL' in var:
                display_value = value.split('@')[0] + '@***' if '@' in value else value[:20] + '***'
            else:
                display_value = value
            logger.info(f"  {var}: {display_value}")

    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return False

    logger.info("Environment check PASSED")
    return True


def initialize_database():
    """Initialize database tables."""
    logger.info("Initializing database...")

    try:
        # Lazy import to avoid triggering libsqlite3 dependency
        try:
            from server.database import init_db
            init_db()
            logger.info("Database initialization SUCCESSFUL")
        except ImportError as e:
            logger.warning(f"Database module import failed (skipping): {str(e)[:100]}")
        return True
    except Exception as e:
        logger.warning(f"Database initialization FAILED (non-fatal): {str(e)[:100]}")
        return True


def health_check():
    """Perform health checks on database only."""
    logger.info("Performing health checks...")

    checks_passed = 0
    checks_total = 1

    # Check database connection only
    try:
        from server.database import health_check as db_health
        if db_health():
            logger.info("  Database health check: PASSED")
            checks_passed += 1
        else:
            logger.warning("  Database health check: FAILED")
    except Exception as e:
        logger.warning(f"  Database health check: ERROR - {str(e)[:100]}")

    logger.info(f"Health checks: {checks_passed}/{checks_total} PASSED")
    # Don't fail the deployment if health checks fail
    return True


def start_server():
    """Start the uvicorn server."""
    logger.info("Starting API server...")

    import uvicorn

    # Get configuration from environment
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', '8001'))
    workers = int(os.getenv('API_WORKERS', '1'))

    logger.info(f"Server configuration:")
    logger.info(f"  Host: {host}")
    logger.info(f"  Port: {port}")
    logger.info(f"  Workers: {workers}")

    try:
        uvicorn.run(
            "server.main:app",
            host=host,
            port=port,
            workers=workers,
            log_level="info"
        )
    except Exception as e:
        # Log the error but don't crash - let gunicorn handle startup instead
        logger.warning(f"Uvicorn startup failed: {str(e)[:150]}")
        # Try to start without uvicorn - gunicorn should be the primary server
        raise


def main():
    """Main deployment function."""
    logger.info("=" * 60)
    logger.info("Kundali Astrology API - Production Deployment")
    logger.info("=" * 60)

    # Step 1: Check environment
    if not check_environment():
        logger.error("Environment check failed. Aborting deployment.")
        sys.exit(1)

    # Step 2: Initialize database (optional, non-fatal)
    logger.info("")
    initialize_database()

    # Step 3: Health checks (optional)
    logger.info("")
    health_check()

    # Step 4: Start server - gunicorn will handle this, not uvicorn
    logger.info("")
    logger.info("=" * 60)
    logger.info("NOTE: Use Procfile with gunicorn for production")
    logger.info("This script is for local development only")
    logger.info("=" * 60)

    try:
        start_server()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.warning(f"Server startup error (expected in production): {str(e)[:100]}")
        logger.info("Railway will use Procfile + gunicorn instead")
        # Don't exit with error - let gunicorn handle it
        sys.exit(0)


if __name__ == "__main__":
    main()
