"""
Database configuration and connection management.

Handles SQLAlchemy setup, session management, and database operations
for Supabase PostgreSQL backend.
"""

import os
import logging
from typing import Generator
from sqlalchemy import create_engine, event, pool, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/kundali_db"
)

# Initialize engine and session factory as None (lazy initialization)
engine = None
SessionLocal = None
Base = declarative_base()


def _init_engine():
    """Initialize database engine lazily to avoid import-time errors."""
    global engine, SessionLocal

    if engine is None:
        try:
            # SQLAlchemy engine configuration
            # Using psycopg2 driver for PostgreSQL
            engine = create_engine(
                DATABASE_URL,
                poolclass=pool.NullPool,  # Supabase recommends NullPool
                echo=False,  # Set to True for SQL logging
                connect_args={
                    "connect_timeout": 10,
                    "options": "-c statement_timeout=30000"
                }
            )

            # Create session factory
            SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            )
            logger.info("Database engine initialized successfully")
        except Exception as e:
            logger.warning(f"Database engine initialization failed (non-fatal): {str(e)[:100]}")
            # Return None - database operations will fail gracefully
            return False
    return True


def set_sqlite_pragma(dbapi_conn, connection_record):
    """
    Configure PostgreSQL connection parameters.

    This ensures proper timezone handling and other settings.
    """
    if "postgresql" in DATABASE_URL:
        try:
            with dbapi_conn.cursor() as cursor:
                cursor.execute("SET timezone = 'UTC'")
        except Exception as e:
            logger.warning(f"Failed to set timezone: {e}")


# Register event listener after engine is initialized
def _register_event_listener():
    """Register database event listeners after engine initialization."""
    global engine
    if engine is not None:
        event.listens_for(engine, "connect")(set_sqlite_pragma)


def get_db() -> Generator[Session, None, None]:
    """
    Get database session as dependency injection.

    Usage in FastAPI routes:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items

    Yields:
        SQLAlchemy Session object
    """
    # Initialize engine on first use
    _init_engine()
    _register_event_listener()

    if SessionLocal is None:
        logger.error("Database engine not initialized")
        raise RuntimeError("Database engine not available")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.

    Creates all tables defined in models that inherit from Base.
    Should be called once during application startup.
    """
    try:
        _init_engine()
        _register_event_listener()

        if engine is None:
            logger.warning("Database engine not available, skipping table creation")
            return False

        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.warning(f"Error creating database tables (non-fatal): {str(e)[:100]}")
        return False


def drop_all_tables():
    """
    Drop all tables from the database.

    WARNING: This will delete all data. Use only in development/testing.
    """
    try:
        _init_engine()
        _register_event_listener()

        if engine is None:
            logger.warning("Database engine not available")
            return False

        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")
        return True
    except Exception as e:
        logger.warning(f"Error dropping database tables: {str(e)[:100]}")
        return False


def health_check() -> bool:
    """
    Check database connectivity.

    Returns:
        True if database is accessible, False otherwise
    """
    try:
        _init_engine()
        _register_event_listener()

        if engine is None:
            logger.warning("Database engine not available")
            return False

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database health check passed")
            return True
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        return False


def reset_db():
    """
    Reset database by dropping and recreating all tables.

    WARNING: This will delete all data. Use only in development.
    """
    drop_all_tables()
    init_db()
