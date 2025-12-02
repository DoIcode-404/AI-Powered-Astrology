"""
MongoDB Index Management
Creates and manages indexes for optimal query performance.
"""

import logging
from datetime import datetime, timedelta
from server.database import get_db

logger = logging.getLogger(__name__)


def create_horoscope_indexes():
    """
    Create indexes for the horoscopes collection.
    Optimizes queries for:
    - Daily horoscope retrieval by sign and date
    - Weekly horoscope retrieval
    - Monthly horoscope retrieval
    - Historical archive queries
    """
    try:
        db = get_db()
        horoscopes_col = db["horoscopes"]

        # Index 1: Compound index on zodiac_sign and date for daily horoscopes
        horoscopes_col.create_index(
            [("zodiac_sign", 1), ("date", -1)],
            name="idx_daily_horoscope",
            sparse=True,
            background=True
        )
        logger.info("Created index: idx_daily_horoscope")

        # Index 2: Compound index on zodiac_sign and week_start for weekly horoscopes
        horoscopes_col.create_index(
            [("zodiac_sign", 1), ("week_start", -1)],
            name="idx_weekly_horoscope",
            sparse=True,
            background=True
        )
        logger.info("Created index: idx_weekly_horoscope")

        # Index 3: Compound index on zodiac_sign and year_month for monthly horoscopes
        horoscopes_col.create_index(
            [("zodiac_sign", 1), ("year_month", -1)],
            name="idx_monthly_horoscope",
            sparse=True,
            background=True
        )
        logger.info("Created index: idx_monthly_horoscope")

        # Index 4: TTL index on ttl field to auto-delete old cached horoscopes after 30 days
        horoscopes_col.create_index(
            [("ttl", 1)],
            name="idx_ttl_horoscope",
            expireAfterSeconds=2592000,  # 30 days
            sparse=True,
            background=True
        )
        logger.info("Created index: idx_ttl_horoscope (TTL: 30 days)")

        # Index 5: Index on type field for filtering by horoscope type
        horoscopes_col.create_index(
            [("type", 1)],
            name="idx_horoscope_type",
            background=True
        )
        logger.info("Created index: idx_horoscope_type")

        # Index 6: Index on generated_at for sorting by recency
        horoscopes_col.create_index(
            [("generated_at", -1)],
            name="idx_generated_at",
            background=True
        )
        logger.info("Created index: idx_generated_at")

        logger.info("All horoscope indexes created successfully")

    except Exception as e:
        logger.error(f"Error creating horoscope indexes: {str(e)}", exc_info=True)


def create_compatibility_indexes():
    """
    Create indexes for the compatibility cache collection.
    Optimizes queries for:
    - Compatibility lookup by person pair
    - Bulk comparisons
    - Archive and history queries
    """
    try:
        db = get_db()
        compatibility_col = db["compatibility_cache"]

        # Index 1: Compound index on user_id and partner_id for quick pair lookups
        compatibility_col.create_index(
            [("user_id", 1), ("partner_id", 1)],
            name="idx_compatibility_pair",
            unique=False,
            background=True
        )
        logger.info("Created index: idx_compatibility_pair")

        # Index 2: Index on user_id for finding all compatibilities for a person
        compatibility_col.create_index(
            [("user_id", 1)],
            name="idx_user_compatibilities",
            background=True
        )
        logger.info("Created index: idx_user_compatibilities")

        # Index 3: Index on relationship_type for filtering by relationship type
        compatibility_col.create_index(
            [("relationship_type", 1)],
            name="idx_relationship_type",
            background=True
        )
        logger.info("Created index: idx_relationship_type")

        # Index 4: TTL index on ttl field to auto-delete cached compatibility after 7 days
        compatibility_col.create_index(
            [("ttl", 1)],
            name="idx_ttl_compatibility",
            expireAfterSeconds=604800,  # 7 days
            sparse=True,
            background=True
        )
        logger.info("Created index: idx_ttl_compatibility (TTL: 7 days)")

        # Index 5: Index on calculated_at for sorting by recency
        compatibility_col.create_index(
            [("calculated_at", -1)],
            name="idx_calculated_at",
            background=True
        )
        logger.info("Created index: idx_calculated_at")

        # Index 6: Index on compatibility_percentage for range queries and sorting
        compatibility_col.create_index(
            [("compatibility_percentage", -1)],
            name="idx_compatibility_percentage",
            background=True
        )
        logger.info("Created index: idx_compatibility_percentage")

        logger.info("All compatibility indexes created successfully")

    except Exception as e:
        logger.error(f"Error creating compatibility indexes: {str(e)}", exc_info=True)


def create_kundali_indexes():
    """
    Create indexes for the kundali collection for optimal performance.
    """
    try:
        db = get_db()
        kundali_col = db["kundalis"]

        # Index 1: Index on user_id for quick user lookups
        kundali_col.create_index(
            [("user_id", 1)],
            name="idx_user_kundali",
            unique=True,
            sparse=True,
            background=True
        )
        logger.info("Created index: idx_user_kundali")

        # Index 2: Index on email for authentication lookups
        kundali_col.create_index(
            [("email", 1)],
            name="idx_email",
            unique=True,
            sparse=True,
            background=True
        )
        logger.info("Created index: idx_email")

        # Index 3: Index on sun_sign for grouping by zodiac
        kundali_col.create_index(
            [("sun_sign", 1)],
            name="idx_sun_sign",
            background=True
        )
        logger.info("Created index: idx_sun_sign")

        logger.info("All kundali indexes created successfully")

    except Exception as e:
        logger.error(f"Error creating kundali indexes: {str(e)}", exc_info=True)


def create_all_indexes():
    """
    Create all database indexes in the correct order.
    Should be called once during application initialization.
    """
    logger.info("Starting index creation process...")
    create_horoscope_indexes()
    create_compatibility_indexes()
    create_kundali_indexes()
    logger.info("All indexes created successfully")


def drop_all_indexes():
    """
    Drop all application-specific indexes (except _id).
    Use with caution - only for testing or database maintenance.
    """
    try:
        db = get_db()

        for collection_name in ["horoscopes", "compatibility_cache", "kundalis"]:
            col = db[collection_name]
            indexes = col.list_indexes()
            for index in indexes:
                if index["name"] != "_id_":
                    col.drop_index(index["name"])
                    logger.info(f"Dropped index: {index['name']} from {collection_name}")

        logger.info("All indexes dropped successfully")

    except Exception as e:
        logger.error(f"Error dropping indexes: {str(e)}", exc_info=True)


def get_index_status():
    """
    Get status of all created indexes.

    Returns:
        Dictionary with index information for all collections
    """
    try:
        db = get_db()
        status = {}

        for collection_name in ["horoscopes", "compatibility_cache", "kundalis"]:
            col = db[collection_name]
            indexes = list(col.list_indexes())
            status[collection_name] = {
                "total_indexes": len(indexes),
                "indexes": [
                    {
                        "name": idx["name"],
                        "key": idx.get("key", []),
                        "unique": idx.get("unique", False),
                        "expireAfterSeconds": idx.get("expireAfterSeconds")
                    }
                    for idx in indexes
                ]
            }

        return status

    except Exception as e:
        logger.error(f"Error retrieving index status: {str(e)}", exc_info=True)
        return {}
