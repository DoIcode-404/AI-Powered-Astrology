"""
Prediction service layer for MongoDB database operations.

Handles CRUD operations for ML predictions.
"""

import logging
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime

logger = logging.getLogger(__name__)


def create_prediction(
    db: dict,
    user_id: str,
    kundali_id: str,
    career_potential: float,
    wealth_potential: float,
    marriage_happiness: float,
    children_prospects: float,
    health_status: float,
    spiritual_inclination: float,
    chart_strength: float,
    life_ease_score: float,
    interpretation: Optional[str] = None,
    model_version: str = "1.0.0",
    model_type: str = "xgboost",
    raw_output: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a new prediction for a Kundali.

    Args:
        db: Database connection dict
        user_id: User ID (as string)
        kundali_id: Associated Kundali ID (as string)
        career_potential: Career success score (0-100)
        wealth_potential: Wealth success score (0-100)
        marriage_happiness: Marriage happiness score (0-100)
        children_prospects: Children prospects score (0-100)
        health_status: Health status score (0-100)
        spiritual_inclination: Spiritual inclination score (0-100)
        chart_strength: Chart strength score (0-100)
        life_ease_score: Life ease score (0-100)
        interpretation: Optional interpretation text
        model_version: ML model version
        model_type: ML model type
        raw_output: Raw model output data

    Returns:
        Created Prediction document (with _id as string)

    Raises:
        ValueError: If Kundali not found or invalid data
    """
    try:
        # Verify Kundali exists and belongs to user
        kundalis_collection = db['kundalis']
        kundali = kundalis_collection.find_one({
            "_id": ObjectId(kundali_id),
            "user_id": user_id
        })

        if not kundali:
            raise ValueError(f"Kundali {kundali_id} not found for user {user_id}")

        # Calculate average score
        scores = [
            career_potential, wealth_potential, marriage_happiness, children_prospects,
            health_status, spiritual_inclination, chart_strength, life_ease_score
        ]
        average_score = sum(scores) / len(scores) if scores else 0

        # Create new prediction
        prediction_doc = {
            "kundali_id": kundali_id,
            "user_id": user_id,
            "career_potential": career_potential,
            "wealth_potential": wealth_potential,
            "marriage_happiness": marriage_happiness,
            "children_prospects": children_prospects,
            "health_status": health_status,
            "spiritual_inclination": spiritual_inclination,
            "chart_strength": chart_strength,
            "life_ease_score": life_ease_score,
            "average_score": average_score,
            "interpretation": interpretation,
            "model_version": model_version,
            "model_type": model_type,
            "raw_output": raw_output,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        predictions_collection = db['predictions']
        result = predictions_collection.insert_one(prediction_doc)

        prediction_doc['_id'] = str(result.inserted_id)
        logger.info(f"Prediction created: id={result.inserted_id}, kundali_id={kundali_id}")
        return prediction_doc

    except Exception as e:
        logger.error(f"Error creating prediction: {str(e)}")
        raise


def get_prediction(db: dict, prediction_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific prediction by ID, ensuring user ownership.

    Args:
        db: Database connection dict
        prediction_id: Prediction ID (as string)
        user_id: User ID (to ensure ownership, as string)

    Returns:
        Prediction document if found and owned by user, None otherwise
    """
    try:
        predictions_collection = db['predictions']
        prediction = predictions_collection.find_one({
            "_id": ObjectId(prediction_id),
            "user_id": user_id
        })

        if prediction:
            prediction['_id'] = str(prediction['_id'])
            logger.info(f"Retrieved prediction: id={prediction_id}, user_id={user_id}")
        else:
            logger.warning(f"Prediction not found: id={prediction_id}, user_id={user_id}")

        return prediction

    except Exception as e:
        logger.error(f"Error retrieving prediction: {str(e)}")
        raise


def get_predictions_for_kundali(
    db: dict,
    kundali_id: str,
    user_id: str
) -> List[Dict[str, Any]]:
    """
    Get all predictions for a specific Kundali.

    Args:
        db: Database connection dict
        kundali_id: Kundali ID (as string)
        user_id: User ID (to ensure ownership, as string)

    Returns:
        List of Prediction documents
    """
    try:
        predictions_collection = db['predictions']
        predictions = list(predictions_collection.find({
            "kundali_id": kundali_id,
            "user_id": user_id
        }).sort("created_at", -1))

        # Convert ObjectId to string
        for prediction in predictions:
            prediction['_id'] = str(prediction['_id'])

        logger.info(f"Retrieved {len(predictions)} predictions for kundali {kundali_id}")
        return predictions

    except Exception as e:
        logger.error(f"Error retrieving predictions for Kundali: {str(e)}")
        raise


def list_user_predictions(db: dict, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Get all predictions for a user with pagination.

    Args:
        db: Database connection dict
        user_id: User ID (as string)
        limit: Maximum number of results (default 100)
        offset: Number of results to skip (default 0)

    Returns:
        List of Prediction documents
    """
    try:
        predictions_collection = db['predictions']
        predictions = list(predictions_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).skip(offset).limit(limit))

        # Convert ObjectId to string
        for prediction in predictions:
            prediction['_id'] = str(prediction['_id'])

        logger.info(f"Retrieved {len(predictions)} predictions for user {user_id}")
        return predictions

    except Exception as e:
        logger.error(f"Error listing predictions: {str(e)}")
        raise


def update_prediction(
    db: dict,
    prediction_id: str,
    user_id: str,
    interpretation: Optional[str] = None,
    model_version: Optional[str] = None,
    model_type: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Update a prediction's metadata.

    Args:
        db: Database connection dict
        prediction_id: Prediction ID (as string)
        user_id: User ID (to ensure ownership, as string)
        interpretation: New interpretation (optional)
        model_version: New model version (optional)
        model_type: New model type (optional)

    Returns:
        Updated Prediction document if found, None otherwise

    Raises:
        ValueError: If trying to update non-existent prediction
    """
    try:
        predictions_collection = db['predictions']
        prediction = predictions_collection.find_one({
            "_id": ObjectId(prediction_id),
            "user_id": user_id
        })

        if not prediction:
            raise ValueError(f"Prediction {prediction_id} not found for user {user_id}")

        # Prepare update data
        update_data = {"updated_at": datetime.utcnow()}
        if interpretation is not None:
            update_data["interpretation"] = interpretation
        if model_version is not None:
            update_data["model_version"] = model_version
        if model_type is not None:
            update_data["model_type"] = model_type

        # Update document
        predictions_collection.update_one(
            {"_id": ObjectId(prediction_id)},
            {"$set": update_data}
        )

        # Fetch and return updated document
        updated_prediction = predictions_collection.find_one({"_id": ObjectId(prediction_id)})
        updated_prediction['_id'] = str(updated_prediction['_id'])

        logger.info(f"Prediction updated: id={prediction_id}, user_id={user_id}")
        return updated_prediction

    except Exception as e:
        logger.error(f"Error updating prediction: {str(e)}")
        raise


def delete_prediction(db: dict, prediction_id: str, user_id: str) -> bool:
    """
    Delete a prediction by ID, ensuring user ownership.

    Args:
        db: Database connection dict
        prediction_id: Prediction ID (as string)
        user_id: User ID (to ensure ownership, as string)

    Returns:
        True if deleted successfully

    Raises:
        ValueError: If trying to delete non-existent prediction
    """
    try:
        predictions_collection = db['predictions']
        prediction = predictions_collection.find_one({
            "_id": ObjectId(prediction_id),
            "user_id": user_id
        })

        if not prediction:
            raise ValueError(f"Prediction {prediction_id} not found for user {user_id}")

        predictions_collection.delete_one({"_id": ObjectId(prediction_id)})

        logger.info(f"Prediction deleted: id={prediction_id}, user_id={user_id}")
        return True

    except Exception as e:
        logger.error(f"Error deleting prediction: {str(e)}")
        raise


def get_prediction_count(db: dict, user_id: str) -> int:
    """
    Get the number of predictions saved by a user.

    Args:
        db: Database connection dict
        user_id: User ID (as string)

    Returns:
        Count of predictions
    """
    try:
        predictions_collection = db['predictions']
        count = predictions_collection.count_documents({"user_id": user_id})
        return count
    except Exception as e:
        logger.error(f"Error counting predictions: {str(e)}")
        return 0
