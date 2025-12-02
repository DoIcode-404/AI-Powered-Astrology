"""
Compatibility Analysis Routes
Provides relationship compatibility analysis between two birth charts.

Endpoints:
1. POST /api/compatibility/ - Quick compatibility check
2. POST /api/compatibility/detailed - Detailed compatibility analysis
3. POST /api/compatibility/batch - Bulk compatibility for multiple candidates
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId

from server.database import get_db
from server.services.compatibility_service import CompatibilityCalculator
from server.rule_engine.rules.compatibility_rules import (
    generate_strength_factors,
    generate_challenge_factors,
    generate_remedies,
    generate_relationship_timeline,
    generate_life_area_predictions,
    get_relationship_advice
)
from server.pydantic_schemas.api_response import APIResponse, success_response, error_response
from server.utils.jwt_handler import verify_token

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Compatibility"]
)


# ========== REQUEST/RESPONSE MODELS ==========

class CompatibilityRequest:
    """Compatibility analysis request"""
    def __init__(self, person_a_kundali_id: str, person_b_kundali_id: str, relationship_type: str = "romantic"):
        self.person_a_kundali_id = person_a_kundali_id
        self.person_b_kundali_id = person_b_kundali_id
        self.relationship_type = relationship_type


class BulkCompatibilityRequest:
    """Bulk compatibility request"""
    def __init__(self, person_a_kundali_id: str, candidate_kundali_ids: List[str], relationship_type: str = "romantic"):
        self.person_a_kundali_id = person_a_kundali_id
        self.candidate_kundali_ids = candidate_kundali_ids
        self.relationship_type = relationship_type


# ========== HELPER FUNCTIONS ==========

async def get_kundali_from_db(kundali_id: str, db: dict) -> dict:
    """Fetch kundali from database"""
    try:
        kundalis_collection = db["kundalis"]
        kundali = kundalis_collection.find_one({"_id": ObjectId(kundali_id)})

        if not kundali:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Kundali {kundali_id} not found"
            )

        return kundali
    except Exception as e:
        logger.error(f"Error fetching kundali: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching kundali"
        )


async def cache_compatibility_result(db: dict, result: dict, person_a_id: str, person_b_id: str, relationship_type: str) -> None:
    """Cache compatibility result in database"""
    try:
        cache_collection = db["compatibility_cache"]

        cache_doc = {
            "person_a_kundali_id": person_a_id,
            "person_b_kundali_id": person_b_id,
            "relationship_type": relationship_type,
            "compatibility_percentage": result.get("compatibility_percentage", 0),
            "compatibility_rating": result.get("compatibility_rating", ""),
            "full_result": result,
            "created_at": datetime.utcnow(),
            "cache_expires_at": datetime.utcnow() + timedelta(days=7)  # 7-day cache
        }

        cache_collection.insert_one(cache_doc)
        logger.info(f"Cached compatibility result for {person_a_id} x {person_b_id}")
    except Exception as e:
        logger.error(f"Error caching compatibility: {str(e)}")
        # Non-critical error, continue without cache


async def get_cached_compatibility(db: dict, person_a_id: str, person_b_id: str, relationship_type: str) -> Optional[dict]:
    """Get cached compatibility result if available"""
    try:
        cache_collection = db["compatibility_cache"]

        cached = cache_collection.find_one({
            "person_a_kundali_id": person_a_id,
            "person_b_kundali_id": person_b_id,
            "relationship_type": relationship_type,
            "cache_expires_at": {"$gt": datetime.utcnow()}
        })

        if cached:
            logger.info(f"Retrieved cached compatibility for {person_a_id} x {person_b_id}")
            return cached.get("full_result")

        return None
    except Exception as e:
        logger.error(f"Error retrieving cache: {str(e)}")
        return None


# ========== ENDPOINT 1: Quick Compatibility Check ==========

@router.post("/quick", response_model=APIResponse)
async def quick_compatibility_check(
    person_a_kundali_id: str,
    person_b_kundali_id: str,
    relationship_type: str = "romantic",
    db: dict = Depends(get_db)
) -> APIResponse:
    """
    Quick compatibility check between two birth charts.
    Returns compatibility percentage and rating.

    Args:
        person_a_kundali_id: ID of person A's kundali
        person_b_kundali_id: ID of person B's kundali
        relationship_type: "romantic", "business", "friendship", "family"
        db: Database connection

    Returns:
        APIResponse with compatibility percentage and rating
    """
    try:
        logger.info(f"Quick compatibility check: {person_a_kundali_id} x {person_b_kundali_id}")

        # Check cache first
        cached_result = await get_cached_compatibility(db, person_a_kundali_id, person_b_kundali_id, relationship_type)
        if cached_result:
            return success_response(
                data={
                    "compatibility_percentage": cached_result.get("compatibility_percentage"),
                    "compatibility_rating": cached_result.get("compatibility_rating"),
                    "from_cache": True
                },
                message="Compatibility check completed (from cache)"
            )

        # Fetch both kundalis
        kundali_a = await get_kundali_from_db(person_a_kundali_id, db)
        kundali_b = await get_kundali_from_db(person_b_kundali_id, db)

        # Extract kundali data
        chart_a = kundali_a.get("kundali_data", {})
        chart_b = kundali_b.get("kundali_data", {})

        # Calculate compatibility
        calc = CompatibilityCalculator(chart_a, chart_b, relationship_type)

        if not calc.validate_charts():
            return error_response(
                code="INVALID_CHARTS",
                message="One or both charts are incomplete or invalid",
                http_status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        start_time = datetime.utcnow()
        result = calc.calculate_final_compatibility()
        calc_time = (datetime.utcnow() - start_time).total_seconds() * 1000

        # Prepare response
        response_data = {
            "compatibility_percentage": round(result.get("compatibility_percentage", 0), 2),
            "compatibility_rating": result.get("compatibility_rating", ""),
            "person_a_id": person_a_kundali_id,
            "person_b_id": person_b_kundali_id,
            "relationship_type": relationship_type,
            "calculation_time_ms": round(calc_time, 2)
        }

        # Cache result
        await cache_compatibility_result(
            db, result, person_a_kundali_id, person_b_kundali_id, relationship_type
        )

        return success_response(
            data=response_data,
            message=f"Compatibility check completed: {result.get('compatibility_rating')} match"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in quick compatibility check: {str(e)}", exc_info=True)
        return error_response(
            code="COMPATIBILITY_CALCULATION_ERROR",
            message=f"Error calculating compatibility: {str(e)}",
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== ENDPOINT 2: Detailed Compatibility Analysis ==========

@router.post("/detailed", response_model=APIResponse)
async def detailed_compatibility_analysis(
    person_a_kundali_id: str,
    person_b_kundali_id: str,
    relationship_type: str = "romantic",
    db: dict = Depends(get_db)
) -> APIResponse:
    """
    Detailed compatibility analysis with strengths, challenges, and remedies.

    Returns comprehensive analysis including:
    - Component scores (overlay, house, aspect, d9, guna)
    - Top 5 strength factors
    - Top 5 challenge factors
    - Remedial suggestions
    - Relationship timeline
    - Life area predictions
    """
    try:
        logger.info(f"Detailed compatibility analysis: {person_a_kundali_id} x {person_b_kundali_id}")

        # Fetch both kundalis
        kundali_a = await get_kundali_from_db(person_a_kundali_id, db)
        kundali_b = await get_kundali_from_db(person_b_kundali_id, db)

        # Extract kundali data
        chart_a = kundali_a.get("kundali_data", {})
        chart_b = kundali_b.get("kundali_data", {})

        # Calculate compatibility
        calc = CompatibilityCalculator(chart_a, chart_b, relationship_type)

        if not calc.validate_charts():
            return error_response(
                code="INVALID_CHARTS",
                message="One or both charts are incomplete or invalid",
                http_status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        start_time = datetime.utcnow()
        result = calc.calculate_final_compatibility()

        # Generate detailed analysis
        strengths = generate_strength_factors(result)
        challenges = generate_challenge_factors(result)
        remedies = generate_remedies(result, relationship_type)
        timeline = generate_relationship_timeline(result)
        life_predictions = generate_life_area_predictions(result, relationship_type)
        relationship_advice = get_relationship_advice(relationship_type)

        calc_time = (datetime.utcnow() - start_time).total_seconds() * 1000

        # Prepare comprehensive response
        response_data = {
            "compatibility_percentage": round(result.get("compatibility_percentage", 0), 2),
            "compatibility_rating": result.get("compatibility_rating", ""),
            "person_a_id": person_a_kundali_id,
            "person_b_id": person_b_kundali_id,
            "relationship_type": relationship_type,

            # Component scores
            "component_scores": {
                "overlay": round(result.get("overlay_score", 0), 2),
                "house": round(result.get("house_score", 0), 2),
                "aspect": round(result.get("aspect_score", 0), 2),
                "d9": round(result.get("d9_score", 0), 2),
                "guna": round(result.get("component_scores", {}).get("guna", {}).get("compatibility_percentage", 0), 2),
            },

            # Detailed analysis
            "strengths": strengths,
            "challenges": challenges,
            "remedies": remedies,

            # Timeline and predictions
            "timeline": timeline,
            "life_area_predictions": life_predictions,
            "relationship_advice": relationship_advice,

            # Metadata
            "calculation_time_ms": round(calc_time, 2)
        }

        # Cache result
        await cache_compatibility_result(
            db, result, person_a_kundali_id, person_b_kundali_id, relationship_type
        )

        return success_response(
            data=response_data,
            message="Detailed compatibility analysis completed"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in detailed compatibility analysis: {str(e)}", exc_info=True)
        return error_response(
            code="ANALYSIS_ERROR",
            message=f"Error analyzing compatibility: {str(e)}",
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== ENDPOINT 3: Bulk Compatibility Analysis ==========

@router.post("/batch", response_model=APIResponse)
async def bulk_compatibility_analysis(
    person_a_kundali_id: str,
    candidate_kundali_ids: List[str],
    relationship_type: str = "romantic",
    db: dict = Depends(get_db)
) -> APIResponse:
    """
    Compare one person against multiple candidates.
    Returns ranked list of matches by compatibility score.

    Useful for:
    - Dating app matching
    - Finding compatible business partners
    - Identifying best team matches
    """
    try:
        logger.info(f"Bulk compatibility analysis: {person_a_kundali_id} vs {len(candidate_kundali_ids)} candidates")

        # Validate candidate list
        if len(candidate_kundali_ids) == 0:
            return error_response(
                code="INVALID_REQUEST",
                message="No candidates provided",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        if len(candidate_kundali_ids) > 50:
            return error_response(
                code="TOO_MANY_CANDIDATES",
                message="Maximum 50 candidates allowed per batch",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch person A's kundali
        kundali_a = await get_kundali_from_db(person_a_kundali_id, db)
        chart_a = kundali_a.get("kundali_data", {})

        # Analyze against each candidate
        results = []

        for candidate_id in candidate_kundali_ids:
            try:
                # Fetch candidate kundali
                kundali_b = await get_kundali_from_db(candidate_id, db)
                chart_b = kundali_b.get("kundali_data", {})

                # Calculate compatibility
                calc = CompatibilityCalculator(chart_a, chart_b, relationship_type)

                if calc.validate_charts():
                    result = calc.calculate_final_compatibility()

                    results.append({
                        "candidate_kundali_id": candidate_id,
                        "candidate_name": kundali_b.get("name", "Unknown"),
                        "compatibility_percentage": round(result.get("compatibility_percentage", 0), 2),
                        "compatibility_rating": result.get("compatibility_rating", ""),
                    })

                    # Cache result
                    await cache_compatibility_result(
                        db, result, person_a_kundali_id, candidate_id, relationship_type
                    )
                else:
                    logger.warning(f"Invalid chart for candidate {candidate_id}")

            except HTTPException:
                logger.warning(f"Could not fetch candidate {candidate_id}")
                continue
            except Exception as e:
                logger.warning(f"Error analyzing candidate {candidate_id}: {str(e)}")
                continue

        # Sort by compatibility score (descending)
        results.sort(key=lambda x: x["compatibility_percentage"], reverse=True)

        response_data = {
            "person_a_kundali_id": person_a_kundali_id,
            "total_candidates_analyzed": len(results),
            "relationship_type": relationship_type,
            "ranked_matches": results,
            "top_match": results[0] if results else None,
            "average_compatibility": round(
                sum(r["compatibility_percentage"] for r in results) / len(results) if results else 0, 2
            )
        }

        return success_response(
            data=response_data,
            message=f"Analyzed {len(results)} candidates"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in bulk compatibility analysis: {str(e)}", exc_info=True)
        return error_response(
            code="BATCH_ANALYSIS_ERROR",
            message=f"Error in batch analysis: {str(e)}",
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
