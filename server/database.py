"""
MongoDB Database Configuration and Connection Management.

Handles pymongo setup for MongoDB Atlas backend.
Replaces previous PostgreSQL/SQLAlchemy configuration.
"""

import os
import logging
from typing import Generator
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# MongoDB connection URL
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb+srv://astrology_user:password@astrology-db.0w3uft1.mongodb.net/?retryWrites=true&w=majority"
)

# Debug: Log the loaded connection URL (without password)
if MONGODB_URL:
    masked_url = MONGODB_URL.split("@")[0] + "@***" if "@" in MONGODB_URL else MONGODB_URL
    logger.info(f"MongoDB URL loaded: {masked_url}")

# Initialize MongoDB client and database
client = None
db = None


def _init_mongo():
    """Initialize MongoDB client and database connection."""
    global client, db

    if client is None or db is None:
        try:
            # Log connection attempt (without password)
            if MONGODB_URL:
                masked_url = MONGODB_URL.split("@")[0] + "@***" if "@" in MONGODB_URL else MONGODB_URL
                logger.info(f"Attempting MongoDB connection to: {masked_url}")
            else:
                logger.warning("CRITICAL: MONGODB_URL environment variable is not set!")

            # Create MongoDB client with connection pooling
            client = MongoClient(
                MONGODB_URL,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,  # 10 second connection timeout
                retryWrites=True,
                w="majority"
            )

            # Test connection
            client.admin.command('ping')
            logger.info("MongoDB connection established")

            # Get database reference
            db = client['astrology_db']
            logger.info("MongoDB database initialized")

            # Create indexes
            _create_indexes()

            return True
        except ServerSelectionTimeoutError as e:
            logger.error(f"MongoDB connection timeout: {e}")
            logger.error("CRITICAL: Ensure MONGODB_URL environment variable is set in Railway deployment")
            return False
        except Exception as e:
            logger.error(f"MongoDB initialization error: {e}")
            logger.error(f"CRITICAL: MongoDB connection failed. Check if MONGODB_URL is set and MongoDB Atlas is accessible")
            return False

    return True


def _create_indexes():
    """Create necessary indexes for collections."""
    try:
        if db is None:
            return

        # Users collection indexes
        users_collection = db['users']
        users_collection.create_index([('email', ASCENDING)], unique=True, sparse=True)
        users_collection.create_index([('username', ASCENDING)], unique=True, sparse=True)
        users_collection.create_index([('created_at', DESCENDING)])

        # User settings collection indexes
        settings_collection = db['user_settings']
        settings_collection.create_index([('user_id', ASCENDING)], unique=True, sparse=True)

        # Kundalis collection indexes
        kundalis_collection = db['kundalis']
        kundalis_collection.create_index([('user_id', ASCENDING)])
        kundalis_collection.create_index([('created_at', DESCENDING)])

        # Predictions collection indexes
        predictions_collection = db['predictions']
        predictions_collection.create_index([('kundali_id', ASCENDING)])
        predictions_collection.create_index([('user_id', ASCENDING)])
        predictions_collection.create_index([('created_at', DESCENDING)])

        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Error creating indexes: {e}")


def get_db() -> dict:
    """
    Get MongoDB database connection.

    Returns:
        Dictionary with collection references for dependency injection.

    Usage in FastAPI routes:
        def get_items(db: dict = Depends(get_db)):
            users = db['users'].find_one({'_id': ObjectId(user_id)})
    """
    _init_mongo()

    if db is None:
        error_msg = "MongoDB database not initialized. Ensure MONGODB_URL environment variable is set correctly in Railway deployment."
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    return {
        'users': db['users'],
        'user_settings': db['user_settings'],
        'kundalis': db['kundalis'],
        'predictions': db['predictions'],
    }


def health_check() -> bool:
    """
    Check MongoDB connectivity.

    Returns:
        True if database is accessible, False otherwise
    """
    try:
        _init_mongo()

        if client is None:
            logger.warning("MongoDB client not initialized")
            return False

        client.admin.command('ping')
        logger.info("MongoDB health check passed")
        return True
    except Exception as e:
        logger.warning(f"MongoDB health check failed: {e}")
        return False


def close_db():
    """
    Close MongoDB connection.

    Call this during application shutdown.
    """
    global client

    if client is not None:
        try:
            client.close()
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.warning(f"Error closing MongoDB connection: {e}")
        finally:
            client = None


def reset_db():
    """
    Reset database by dropping all collections.

    WARNING: This will delete all data. Use only in development.
    """
    try:
        _init_mongo()

        if db is None:
            logger.warning("MongoDB database not initialized")
            return False

        # Drop all collections
        for collection_name in db.list_collection_names():
            db[collection_name].drop()
            logger.warning(f"Dropped collection: {collection_name}")

        logger.warning("Database reset completed")
        return True
    except Exception as e:
        logger.warning(f"Error resetting database: {e}")
        return False
