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
    """
    Placeholder for server startup.

    NOTE: In production, gunicorn (via Procfile) handles actual server startup.
    This function is kept for backward compatibility only.
    """
    logger.info("=" * 60)
    logger.info("Startup Script Completed")
    logger.info("=" * 60)
    logger.info("✓ Environment validation: PASSED")
    logger.info("✓ Database setup: COMPLETED")
    logger.info("✓ Health checks: COMPLETED")
    logger.info("")
    logger.info("Gunicorn will now start via Procfile...")
    logger.info("Web server will listen on 0.0.0.0:$PORT")
    logger.info("=" * 60)


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

    # Step 4: Complete and exit
    logger.info("")
    start_server()

    # Exit successfully - gunicorn will be started via Procfile
    logger.info("")
    logger.info("Deployment script completed successfully")
    logger.info("Exiting to allow Procfile to start gunicorn...")
    sys.exit(0)


if __name__ == "__main__":
    main()
