"""
Kundali service layer for MongoDB database operations.

Handles CRUD operations for Kundali charts.
"""

import logging
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime

logger = logging.getLogger(__name__)


def save_kundali(
    db: dict,
    user_id: str,
    name: str,
    birth_date: str,
    birth_time: str,
    latitude: str,
    longitude: str,
    timezone: str,
    kundali_data: Dict[str, Any],
    ml_features: Optional[Dict[str, Any]] = None,
    is_primary: bool = False
) -> Dict[str, Any]:
    """
    Save a new Kundali for a user.

    Args:
        db: Database connection dict
        user_id: User ID (MongoDB ObjectId as string)
        name: Kundali name
        birth_date: Birth date (YYYY-MM-DD)
        birth_time: Birth time (HH:MM:SS)
        latitude: Birth location latitude
        longitude: Birth location longitude
        timezone: Birth location timezone
        kundali_data: Complete Kundali analysis data
        ml_features: Optional ML features dictionary
        is_primary: Whether this is the user's primary kundali (default False)

    Returns:
        Saved Kundali document (with _id as string)

    Raises:
        ValueError: If user not found or invalid data
    """
    try:
        # Verify user exists
        users_collection = db['users']
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        # If this is primary, unset any existing primary kundali
        if is_primary:
            kundalis_collection = db['kundalis']
            kundalis_collection.update_many(
                {"user_id": user_id, "is_primary": True},
                {"$set": {"is_primary": False}}
            )

        # Create new Kundali
        kundali_doc = {
            "user_id": user_id,
            "name": name,
            "birth_date": birth_date,
            "birth_time": birth_time,
            "latitude": str(latitude),
            "longitude": str(longitude),
            "timezone": timezone,
            "kundali_data": kundali_data,
            "ml_features": ml_features,
            "is_primary": is_primary,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        kundalis_collection = db['kundalis']
        result = kundalis_collection.insert_one(kundali_doc)

        kundali_doc['_id'] = str(result.inserted_id)
        logger.info(f"Kundali saved: id={result.inserted_id}, user_id={user_id}, name={name}, is_primary={is_primary}")
        return kundali_doc

    except Exception as e:
        logger.error(f"Error saving Kundali: {str(e)}")
        raise


def get_kundali(db: dict, kundali_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific Kundali by ID, ensuring ownership.

    Args:
        db: Database connection dict
        kundali_id: Kundali ID (MongoDB ObjectId as string)
        user_id: User ID (to ensure ownership, as string)

    Returns:
        Kundali document if found and owned by user, None otherwise
    """
    try:
        # Validate kundali_id is a valid ObjectId
        try:
            object_id = ObjectId(kundali_id)
        except Exception:
            logger.warning(f"Invalid Kundali ID format: {kundali_id}")
            return None

        kundalis_collection = db['kundalis']
        kundali = kundalis_collection.find_one({
            "_id": object_id,
            "user_id": user_id
        })

        if kundali:
            kundali['_id'] = str(kundali['_id'])
            logger.info(f"Retrieved Kundali: id={kundali_id}, user_id={user_id}")
        else:
            logger.warning(f"Kundali not found: id={kundali_id}, user_id={user_id}")

        return kundali

    except Exception as e:
        logger.error(f"Error retrieving Kundali: {str(e)}")
        raise


def list_user_kundalis(db: dict, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Get all Kundalis for a specific user with pagination.

    Args:
        db: Database connection dict
        user_id: User ID (as string)
        limit: Maximum number of results (default 100)
        offset: Number of results to skip (default 0)

    Returns:
        List of Kundali documents
    """
    try:
        kundalis_collection = db['kundalis']
        kundalis = list(kundalis_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).skip(offset).limit(limit))

        # Convert ObjectId to string
        for kundali in kundalis:
            kundali['_id'] = str(kundali['_id'])

        logger.info(f"Retrieved {len(kundalis)} Kundalis for user {user_id}")
        return kundalis

    except Exception as e:
        logger.error(f"Error listing Kundalis: {str(e)}")
        raise


def update_kundali(
    db: dict,
    kundali_id: str,
    user_id: str,
    name: Optional[str] = None,
    ml_features: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Update a Kundali's name and/or ML features.

    Args:
        db: Database connection dict
        kundali_id: Kundali ID (as string)
        user_id: User ID (to ensure ownership, as string)
        name: New name (optional)
        ml_features: Updated ML features (optional)

    Returns:
        Updated Kundali document if found, None otherwise

    Raises:
        ValueError: If trying to update non-existent Kundali
    """
    try:
        # Validate kundali_id is a valid ObjectId
        try:
            object_id = ObjectId(kundali_id)
        except Exception:
            raise ValueError(f"Invalid Kundali ID format: {kundali_id}")

        kundalis_collection = db['kundalis']
        kundali = kundalis_collection.find_one({
            "_id": object_id,
            "user_id": user_id
        })

        if not kundali:
            raise ValueError(f"Kundali {kundali_id} not found for user {user_id}")

        # Prepare update data
        update_data = {"updated_at": datetime.utcnow()}
        if name is not None:
            update_data["name"] = name
        if ml_features is not None:
            update_data["ml_features"] = ml_features

        # Update document
        kundalis_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )

        # Fetch and return updated document
        updated_kundali = kundalis_collection.find_one({"_id": object_id})
        updated_kundali['_id'] = str(updated_kundali['_id'])

        logger.info(f"Kundali updated: id={kundali_id}, user_id={user_id}")
        return updated_kundali

    except Exception as e:
        logger.error(f"Error updating Kundali: {str(e)}")
        raise


def delete_kundali(db: dict, kundali_id: str, user_id: str) -> bool:
    """
    Delete a Kundali by ID, ensuring ownership.

    Args:
        db: Database connection dict
        kundali_id: Kundali ID (as string)
        user_id: User ID (to ensure ownership, as string)

    Returns:
        True if deleted successfully

    Raises:
        ValueError: If trying to delete non-existent Kundali
    """
    try:
        # Validate kundali_id is a valid ObjectId
        try:
            object_id = ObjectId(kundali_id)
        except Exception:
            raise ValueError(f"Invalid Kundali ID format: {kundali_id}")

        kundalis_collection = db['kundalis']
        kundali = kundalis_collection.find_one({
            "_id": object_id,
            "user_id": user_id
        })

        if not kundali:
            raise ValueError(f"Kundali {kundali_id} not found for user {user_id}")

        kundalis_collection.delete_one({"_id": object_id})

        logger.info(f"Kundali deleted: id={kundali_id}, user_id={user_id}")
        return True

    except Exception as e:
        logger.error(f"Error deleting Kundali: {str(e)}")
        raise


def get_kundali_count(db: dict, user_id: str) -> int:
    """
    Get the number of Kundalis saved by a user.

    Args:
        db: Database connection dict
        user_id: User ID (as string)

    Returns:
        Count of Kundalis
    """
    try:
        kundalis_collection = db['kundalis']
        count = kundalis_collection.count_documents({"user_id": user_id})
        return count
    except Exception as e:
        logger.error(f"Error counting Kundalis: {str(e)}")
        return 0


def get_primary_kundali(db: dict, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get the user's primary/default kundali.

    Args:
        db: Database connection dict
        user_id: User ID (as string)

    Returns:
        Primary Kundali document if found, None otherwise
    """
    try:
        kundalis_collection = db['kundalis']
        kundali = kundalis_collection.find_one({
            "user_id": user_id,
            "is_primary": True
        })

        if kundali:
            kundali['_id'] = str(kundali['_id'])
            logger.info(f"Retrieved primary Kundali for user {user_id}")
        else:
            logger.warning(f"No primary Kundali found for user {user_id}")

        return kundali

    except Exception as e:
        logger.error(f"Error retrieving primary Kundali: {str(e)}")
        raise
