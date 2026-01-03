"""
AI Analysis Endpoint
Provides AI-powered astrology analysis combining deterministic calculations with ML predictions.

Endpoint:
- POST /api/ai-analysis - Complete AI analysis with ML + astrology + text generation

Author: Backend AI Systems Team
"""

import logging
import time
from datetime import datetime
from typing import Optional, Dict, Any, Union

from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel, Field, ValidationError
from bson import ObjectId

from server.database import get_db
from server.models.user import User
from server.routes.auth import get_current_user
from server.pydantic_schemas.ml_response import (
    MLScoreBox,
    AIAnalysisSection,
    AnalysisMetadata,
    AIAnalysisData,
    AIAnalysisResponse,
    AIAnalysisErrorResponse,
    ResponseStatus
)
from server.pydantic_schemas.kundali_schema import KundaliRequest
from server.services.logic import generate_kundali_logic
from server.services.compatibility_service import CompatibilityCalculator
from server.ml.feature_extractor import KundaliFeatureExtractor
from server.services.llm_analysis_service import get_llm_service
from server.services.token_tracker import get_token_tracker

# Import ML predictor
try:
    from server.ml.predictor import get_predictor
    ML_AVAILABLE = True
    MODELS_LOADED = True
except ImportError:
    ML_AVAILABLE = False
    MODELS_LOADED = False
    get_predictor = None

logger = logging.getLogger(__name__)

router = APIRouter(tags=["AI Analysis"])


# ========== REQUEST MODELS ==========

class SimpleAIAnalysisRequest(BaseModel):
    """Simplified request - just context, fetch birth details from MongoDB."""
    context: str = Field(default="general", description="Analysis context: general, career, health, etc.")
    user_kundali_name: Optional[str] = Field(None, description="Name of user's kundali to fetch (optional, defaults to primary)")
    partner_kundali_name: Optional[str] = Field(None, description="Name of partner's kundali to fetch (optional, for compatibility analysis)")


class AIAnalysisRequest(BaseModel):
    """Request for AI-powered Kundali analysis."""
    user_kundali: KundaliRequest = Field(..., description="User's birth chart data")
    context: str = Field(default="general", description="Analysis context: general, career, health, etc.")


class CompatibilityAnalysisRequest(BaseModel):
    """Request for AI-powered compatibility analysis."""
    user_kundali: KundaliRequest = Field(..., description="User's birth chart data")
    partner_kundali: KundaliRequest = Field(..., description="Partner's birth chart data")
    context: str = Field(default="compatibility", description="Analysis context")


# ========== HELPER FUNCTIONS ==========

def extract_ml_predictions(kundali_response) -> Dict[str, MLScoreBox]:
    """
    Extract ML predictions from Kundali data.

    Args:
        kundali_data: Complete kundali calculation result

    Returns:
        Dict[str, MLScoreBox]: ML predictions wrapped in MLScoreBox

    Raises:
        HTTPException: If ML service unavailable or prediction fails
    """
    if not ML_AVAILABLE or not MODELS_LOADED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML service is currently unavailable"
        )

    try:
        # Convert Pydantic model to dict if needed
        if not isinstance(kundali_response, dict):
            kundali_data = kundali_response.model_dump()
        else:
            kundali_data = kundali_response

        # Extract features using KundaliFeatureExtractor
        feature_extractor = KundaliFeatureExtractor()
        features_dict, missing_features = feature_extractor.extract_features(kundali_data)

        if missing_features:
            logger.warning(f"Missing {len(missing_features)} features during extraction")

        # Use new predictor that returns Dict[str, MLScoreBox]
        predictor = get_predictor()
        ml_scores = predictor.predict(features_dict)

        # Remove metadata keys (keep only target predictions)
        ml_scores_clean = {k: v for k, v in ml_scores.items() if not k.startswith("_")}

        return ml_scores_clean

    except Exception as e:
        logger.error(f"ML prediction failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ML prediction error: {str(e)}"
        )


def extract_astrology_scores(kundali_response, partner_kundali_response = None) -> Dict[str, float]:
    """
    Extract deterministic astrology scores.

    Args:
        kundali_response: User's kundali calculation (KundaliResponse or dict)
        partner_kundali_response: Partner's kundali (if compatibility analysis)

    Returns:
        Dict[str, Union[int, float]]: Astrology scores
    """
    # Convert Pydantic model to dict if needed
    if not isinstance(kundali_response, dict):
        kundali_data = kundali_response.model_dump()
    else:
        kundali_data = kundali_response

    if partner_kundali_response and not isinstance(partner_kundali_response, dict):
        partner_kundali_data = partner_kundali_response.model_dump()
    else:
        partner_kundali_data = partner_kundali_response

    scores = {}

    # Extract planetary strengths from shad_bala
    if "shad_bala" in kundali_data and kundali_data["shad_bala"]:
        shad_bala = kundali_data["shad_bala"]
        logger.debug(f"shad_bala type: {type(shad_bala)}, has planetary_strengths: {'planetary_strengths' in shad_bala if isinstance(shad_bala, dict) else 'N/A'}")
        if "planetary_strengths" in shad_bala and shad_bala["planetary_strengths"]:
            planetary_strengths = shad_bala["planetary_strengths"]
            logger.debug(f"planetary_strengths count: {len(planetary_strengths)}, type: {type(planetary_strengths)}")
            for planet_name, planet_data in planetary_strengths.items():
                if isinstance(planet_data, dict) and 'error' not in planet_data:
                    # Get Shad Bala strength_percentage and ensure it's 0-100
                    strength = max(0, min(100, planet_data.get("strength_percentage", 0)))
                    if strength > 0:
                        scores[f"{planet_name.lower()}_strength"] = float(strength)
                        logger.debug(f"Added {planet_name} (Shad Bala): {strength}%")

        # Calculate overall chart strength from all planetary strengths
        if scores:
            strength_values = [v for k, v in scores.items() if k.endswith("_strength")]
            if strength_values:
                scores["overall_strength"] = float(sum(strength_values) / len(strength_values))
                logger.debug(f"Overall chart strength: {scores['overall_strength']}%")

        # Extract yoga counts
        yogas = shad_bala.get("yogas", {})
        if yogas:
            scores["total_yogas"] = int(yogas.get("total_yoga_count", 0))
            scores["benefic_yogas"] = int(yogas.get("benefic_yoga_count", 0))

    # If compatibility analysis, calculate Guna Milan
    if partner_kundali_data:
        try:
            logger.info("Starting guna milan calculation...")
            calculator = CompatibilityCalculator(kundali_data, partner_kundali_data)
            compatibility_result = calculator.calculate_final_compatibility()
            logger.info(f"Compatibility result keys: {list(compatibility_result.keys())}")

            if "component_scores" in compatibility_result and "guna" in compatibility_result["component_scores"]:
                guna_data = compatibility_result["component_scores"]["guna"]
                scores["guna_milan_total"] = int(guna_data.get("total_score", 0))
                scores["guna_milan_percentage"] = float(guna_data.get("compatibility_percentage", 0))
                logger.info(f"Guna milan score: {scores['guna_milan_total']}/36")

                for koota_name, koota_score in guna_data.get("individual_scores", {}).items():
                    scores[f"koota_{koota_name.lower().replace(' ', '_')}"] = float(koota_score)
            else:
                logger.warning("No guna data in result")
                scores["guna_milan_total"] = 0

        except Exception as e:
            logger.error(f"Compatibility calculation failed: {str(e)}", exc_info=True)
            scores["guna_milan_total"] = 0

    # Fallback only if truly no data
    if not scores:
        scores["overall_strength"] = 50.0

    return scores


def _validate_ml_scores_structure(ml_scores: Any, field_name: str = "ml_scores") -> None:
    """
    Strict runtime validation: ml_scores MUST be Dict[str, MLScoreBox].

    Validates structure before serialization to catch type errors early.

    Args:
        ml_scores: ML scores to validate
        field_name: Field name for error messages

    Raises:
        ValueError: If validation fails
    """
    # Must be dict
    if not isinstance(ml_scores, dict):
        error_msg = f"{field_name} must be dict, got {type(ml_scores).__name__}"
        logger.error(f"VALIDATION FAILED: {error_msg}")
        raise ValueError(error_msg)

    # Must not be empty
    if not ml_scores:
        error_msg = f"{field_name} cannot be empty"
        logger.error(f"VALIDATION FAILED: {error_msg}")
        raise ValueError(error_msg)

    # All entries must be string -> MLScoreBox
    for key, value in ml_scores.items():
        if not isinstance(key, str):
            error_msg = f"{field_name} key must be string, got {type(key).__name__}"
            logger.error(f"VALIDATION FAILED: {error_msg}")
            raise ValueError(error_msg)

        if not isinstance(value, MLScoreBox):
            error_msg = f"{field_name}['{key}'] must be MLScoreBox, got {type(value).__name__}"
            logger.error(f"VALIDATION FAILED: {error_msg}")
            raise ValueError(error_msg)

        # Validate MLScoreBox fields
        if not isinstance(value.score, (int, float)) or not (0.0 <= value.score <= 100.0):
            error_msg = f"{field_name}['{key}'].score must be float in [0,100], got {value.score}"
            logger.error(f"VALIDATION FAILED: {error_msg}")
            raise ValueError(error_msg)

        if not isinstance(value.confidence, (int, float)) or not (0.0 <= value.confidence <= 1.0):
            error_msg = f"{field_name}['{key}'].confidence must be float in [0,1], got {value.confidence}"
            logger.error(f"VALIDATION FAILED: {error_msg}")
            raise ValueError(error_msg)

    logger.debug(f"Validation passed: {field_name} ({len(ml_scores)} entries)")


def _validate_ml_scores_runtime(ml_scores: Any) -> None:
    """Runtime validation of ml_scores before Pydantic validation."""
    _validate_ml_scores_structure(ml_scores, "ml_scores")


def _validate_astrology_scores_runtime(astrology_scores: Any) -> None:
    """
    Runtime validation of astrology_scores before Pydantic validation.

    Args:
        astrology_scores: Astrology scores to validate

    Raises:
        ValueError: If validation fails
    """
    # Check 1: Must be dict, not list
    if not isinstance(astrology_scores, dict):
        error_msg = f"astrology_scores must be dict, got {type(astrology_scores).__name__}"
        logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
        logger.error(f"astrology_scores payload: {astrology_scores}")
        raise ValueError(error_msg)

    # Check 2: Must not be empty
    if not astrology_scores:
        error_msg = "astrology_scores cannot be empty"
        logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
        raise ValueError(error_msg)

    # Check 3: All keys must be strings, values must be numeric
    for key, value in astrology_scores.items():
        if not isinstance(key, str):
            error_msg = f"astrology_scores key must be string, got {type(key).__name__}"
            logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
            logger.error(f"astrology_scores payload: {astrology_scores}")
            raise ValueError(error_msg)

        if not isinstance(value, (int, float)):
            error_msg = f"astrology_scores['{key}'] must be numeric, got {type(value).__name__}: {value}"
            logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
            raise ValueError(error_msg)

    logger.debug(f"Runtime validation passed for astrology_scores with {len(astrology_scores)} entries")


# ========== HELPER FUNCTIONS FOR SIMPLIFIED ENDPOINT ==========

def get_user_birth_details(user_id: str, db: dict) -> Optional[Dict[str, Any]]:
    """
    Fetch user's birth details from MongoDB kundalis collection.
    
    Args:
        user_id: User's MongoDB _id as string
        db: Database connection dict
        
    Returns:
        Dict with birth details if found, None otherwise
        Structure: {
            'birth_date': 'YYYY-MM-DD',
            'birth_time': 'HH:MM:SS',
            'latitude': float,
            'longitude': float,
            'timezone': str
        }
    """
    try:
        kundalis_collection = db['kundalis']
        
        # Try to convert user_id to ObjectId for MongoDB query
        try:
            user_obj_id = ObjectId(user_id)
        except:
            user_obj_id = user_id  # Use as string if conversion fails
        
        # Find user's primary kundali
        kundali_doc = kundalis_collection.find_one({
            "user_id": user_id,
            "is_primary": True
        })
        
        # If no primary, get any kundali
        if not kundali_doc:
            kundali_doc = kundalis_collection.find_one({"user_id": user_id})
        
        if not kundali_doc:
            logger.warning(f"No kundali found for user_id: {user_id}")
            return None
        
        # Extract birth details
        birth_details = {
            'birth_date': kundali_doc.get('birth_date'),
            'birth_time': kundali_doc.get('birth_time'),
            'latitude': float(kundali_doc.get('latitude', 0)),
            'longitude': float(kundali_doc.get('longitude', 0)),
            'timezone': kundali_doc.get('timezone', 'UTC')
        }
        
        # Validate all required fields are present
        if not all(birth_details.values()):
            logger.error(f"Incomplete birth details for user {user_id}: {birth_details}")
            return None
        
        logger.info(f"Successfully fetched birth details for user {user_id}")
        return birth_details
        
    except Exception as e:
        logger.error(f"Error fetching birth details: {str(e)}", exc_info=True)
        return None


def _compute_harmony_score(
    ml_scores: Dict[str, MLScoreBox],
    partner_ml_scores: Optional[Dict[str, MLScoreBox]] = None
) -> float:
    """
    Compute harmony score from ML scores and partner ML scores for compatibility.

    Rules:
    - Use only numeric ML outputs (0–100)
    - Compute pairwise average per category
    - Final harmony score = average of all categories
    - Round to 1 decimal place

    Args:
        ml_scores: User's ML predictions
        partner_ml_scores: Partner's ML predictions (for compatibility)

    Returns:
        Harmony score (0-100, rounded to 1 decimal place)
    """
    if not ml_scores:
        return 50.0

    if partner_ml_scores:
        # Compatibility: compute pairwise averages
        category_harmonies = []
        for category, user_box in ml_scores.items():
            if category in partner_ml_scores:
                partner_box = partner_ml_scores[category]
                # Pairwise average for this category
                pairwise_avg = (user_box.score + partner_box.score) / 2.0
                category_harmonies.append(pairwise_avg)

        if category_harmonies:
            harmony = sum(category_harmonies) / len(category_harmonies)
            return round(harmony, 1)
        return 50.0
    else:
        # Single person: average all categories
        avg = sum(box.score for box in ml_scores.values()) / len(ml_scores)
        return round(avg, 1)


def generate_ai_analysis(
    ml_scores: Dict[str, MLScoreBox],
    astrology_scores: Dict[str, float],
    context: str,
    partner_ml_scores: Optional[Dict[str, MLScoreBox]] = None
) -> tuple[AIAnalysisSection, Dict[str, Any]]:
    """
    Generate AI-powered textual analysis using an optional external LLM.

    Uses LLM service (if configured) with token tracking and caching for minimal token usage.
    Falls back to rule-based analysis if no LLM is configured or the LLM call fails.

    Returns:
        Tuple of (AIAnalysisSection, metadata_dict)
        metadata_dict contains LLM token usage and cost info
    """
    llm_service = get_llm_service()

    # Generate AI analysis using external LLM service (optional)
    analysis_section, llm_metadata = llm_service.generate_analysis(
        ml_scores=ml_scores,
        astrology_scores=astrology_scores,
        context=context,
        partner_ml_scores=partner_ml_scores
    )

    return analysis_section, llm_metadata


# ========== ENDPOINTS ==========

@router.post(
    "/api/ai-analysis",
    response_model=AIAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Unauthorized - Invalid or missing JWT token"},
        404: {"description": "User's birth details not found in database"},
        422: {"description": "Validation error"},
        503: {"model": AIAnalysisErrorResponse, "description": "ML service unavailable"},
        500: {"model": AIAnalysisErrorResponse, "description": "Server error"}
    }
)
async def ai_analysis_endpoint(
    request: SimpleAIAnalysisRequest,
    user: User = Depends(get_current_user),
    db: dict = Depends(get_db)
):
    """
    Simplified AI-powered astrology analysis endpoint.
    
    This endpoint:
    1. Extracts user_id from JWT token (authenticated)
    2. Fetches user's birth details from MongoDB
    3. Generates Kundali from birth data
    4. Extracts ML predictions
    5. Calculates astrology scores
    6. Generates AI analysis (LLM optional; rule-based fallback available)
    7. Returns complete analysis response
    
    Request:
        - context: str (default "general") - Analysis context
    
    Response:
        AIAnalysisResponse with ML scores, astrology scores, and AI insights
    """
    start_time = time.time()
    
    try:
        logger.info(f"AI Analysis request from user: {user.id}, context: {request.context}")
        
        # 1. Fetch user's birth details from MongoDB
        birth_details = get_user_birth_details(str(user.id), db)
        if not birth_details:
            logger.error(f"Birth details not found for user {user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Your birth details not found. Please create a kundali first."
            )
        
        logger.debug(f"Birth details fetched: {birth_details}")
        
        # 2. Create KundaliRequest from birth details
        kundali_request = KundaliRequest(
            birthDate=birth_details['birth_date'],
            birthTime=birth_details['birth_time'],
            latitude=birth_details['latitude'],
            longitude=birth_details['longitude'],
            timezone=birth_details['timezone']
        )
        
        logger.debug(f"KundaliRequest created: {kundali_request}")
        
        # 3. Generate user kundali
        astro_start = time.time()
        user_kundali = await generate_kundali_logic(kundali_request)
        astro_calc_time = (time.time() - astro_start) * 1000
        
        logger.debug(f"Kundali generated in {astro_calc_time:.2f}ms")
        
        # 4. Extract ML predictions
        ml_start = time.time()
        ml_scores = extract_ml_predictions(user_kundali)
        ml_inference_time_ms = (time.time() - ml_start) * 1000
        
        logger.debug(f"ML predictions extracted in {ml_inference_time_ms:.2f}ms: {list(ml_scores.keys())}")
        
        # 5. Extract astrology scores
        astro_start = time.time()
        astrology_scores = extract_astrology_scores(user_kundali, None)
        astro_calc_time += (time.time() - astro_start) * 1000
        
        logger.debug(f"Astrology scores extracted: {list(astrology_scores.keys())}")
        
        # 6. Validate scores
        _validate_ml_scores_runtime(ml_scores)
        _validate_astrology_scores_runtime(astrology_scores)
        
        # 7. Generate AI analysis with LLM
        ai_analysis, llm_metadata = generate_ai_analysis(ml_scores, astrology_scores, request.context)
        
        # 8. Build response metadata
        total_time = (time.time() - start_time) * 1000
        metadata = AnalysisMetadata(
            calculation_timestamp=datetime.utcnow(),
            ml_inference_time_ms=ml_inference_time_ms,
            astro_calc_time_ms=astro_calc_time,
            total_time_ms=total_time,
            llm_input_tokens=llm_metadata.get("input_tokens"),
            llm_output_tokens=llm_metadata.get("output_tokens"),
            llm_cost_usd=llm_metadata.get("cost_usd"),
            llm_request_duration_ms=llm_metadata.get("request_duration_ms"),
            llm_cache_hit=llm_metadata.get("cache_hit"),
            llm_model=llm_metadata.get("model"),
            llm_fallback=llm_metadata.get("fallback")
        )
        
        # 9. Build kundali summary
        kundali_dict = user_kundali.model_dump() if hasattr(user_kundali, 'model_dump') else user_kundali
        kundali_summary = {
            'planets': kundali_dict.get('planets', {}),
            'houses': kundali_dict.get('houses', {}),
            'ascendant': kundali_dict.get('ascendant', {}),
            'zodiac_sign': kundali_dict.get('zodiac_sign', 'Unknown')
        }
        
        # 10. Construct response
        response = AIAnalysisResponse(
            status=ResponseStatus.SUCCESS,
            success=True,
            data=AIAnalysisData(
                ml_scores=ml_scores,
                astrology_scores=astrology_scores,
                ai_analysis=ai_analysis,
                kundali_data=kundali_summary,
                metadata=metadata
            ),
            timestamp=datetime.utcnow(),
            error_message=None
        )
        
        logger.info(f"AI analysis completed successfully for user {user.id} in {total_time:.2f}ms")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI analysis failed: {str(e)}", exc_info=True)
        return AIAnalysisErrorResponse(
            status=ResponseStatus.ERROR,
            success=False,
            error_message=f"Analysis failed: {str(e)}",
            error_code="ANALYSIS_FAILED",
            timestamp=datetime.utcnow(),
            details=None
        )


@router.post(
    "/api/ai-analysis/full",
    response_model=AIAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        503: {"model": AIAnalysisErrorResponse, "description": "ML service unavailable"},
        500: {"model": AIAnalysisErrorResponse, "description": "Server error"}
    }
)
async def ai_analysis_full_endpoint(request: AIAnalysisRequest):
    """
    Full AI-powered astrology analysis endpoint (with explicit birth data).
    
    DEPRECATED: Use POST /api/ai-analysis (simplified version) instead.
    
    This endpoint accepts explicit birth details and is kept for backward compatibility.

    This endpoint:
    1. Generates Kundali from birth data
    2. Extracts ML predictions (numeric scores)
    3. Calculates deterministic astrology scores
    4. Generates AI textual analysis
    5. Returns fixed-schema response

    Args:
        request: AIAnalysisRequest with user/partner kundali data

    Returns:
        AIAnalysisResponse: Complete analysis with ML scores, astrology scores, and AI insights
    """
    start_time = time.time()
    astro_calc_time = 0
    ml_inference_time_ms: Optional[float] = None

    try:
        # 1. Generate user kundali
        astro_start = time.time()
        user_kundali = await generate_kundali_logic(request.user_kundali)
        astro_calc_time += (time.time() - astro_start) * 1000

        # 2. Extract ML predictions (measure actual execution)
        ml_start = time.time()
        ml_scores = extract_ml_predictions(user_kundali)
        ml_inference_time_ms = (time.time() - ml_start) * 1000

        # 3. Extract astrology scores
        astro_start = time.time()
        astrology_scores = extract_astrology_scores(user_kundali, None)
        astro_calc_time += (time.time() - astro_start) * 1000

        # 5. Runtime validation of ml_scores (before Pydantic)
        _validate_ml_scores_runtime(ml_scores)
        _validate_astrology_scores_runtime(astrology_scores)

        # 6. Generate AI analysis with LLM
        ai_analysis, llm_metadata = generate_ai_analysis(ml_scores, astrology_scores, request.context)

        # 8. Construct metadata (with LLM tracking)
        total_time = (time.time() - start_time) * 1000
        metadata = AnalysisMetadata(
            calculation_timestamp=datetime.utcnow(),
            ml_inference_time_ms=ml_inference_time_ms,
            astro_calc_time_ms=astro_calc_time,
            total_time_ms=total_time,
            llm_input_tokens=llm_metadata.get("input_tokens"),
            llm_output_tokens=llm_metadata.get("output_tokens"),
            llm_cost_usd=llm_metadata.get("cost_usd"),
            llm_request_duration_ms=llm_metadata.get("request_duration_ms"),
            llm_cache_hit=llm_metadata.get("cache_hit"),
            llm_model=llm_metadata.get("model"),
            llm_fallback=llm_metadata.get("fallback")
        )

        # 9. Construct response data
        kundali_dict = user_kundali.model_dump() if hasattr(user_kundali, 'model_dump') else user_kundali
        kundali_summary = {
            'planets': kundali_dict.get('planets', {}),
            'houses': kundali_dict.get('houses', {}),
            'ascendant': kundali_dict.get('ascendant', {}),
            'nakshatra': kundali_dict.get('nakshatra', {})
        }

        analysis_data = AIAnalysisData(
            ml_scores=ml_scores,
            astrology_scores=astrology_scores,
            ai_analysis=ai_analysis,
            kundali_data=kundali_summary,
            metadata=metadata
        )

        # 10. Validate and return response
        response = AIAnalysisResponse(
            status=ResponseStatus.SUCCESS,
            success=True,
            data=analysis_data,
            timestamp=datetime.utcnow(),
            error_message=None
        )

        # Log successful analysis
        ml_log = f"{ml_inference_time_ms:.2f}ms" if ml_inference_time_ms is not None else "not measured"
        logger.info(f"AI analysis completed in {total_time:.2f}ms (ML: {ml_log}, Astro: {astro_calc_time:.2f}ms)")

        return response

    except HTTPException:
        # Re-raise HTTP exceptions (503, etc.)
        raise

    except ValidationError as e:
        # Schema validation error - log and return 500
        logger.error(f"Schema validation failed: {str(e)}")
        logger.error(f"Validation details: {e.errors()}")

        return AIAnalysisErrorResponse(
            status=ResponseStatus.ERROR,
            success=False,
            error_message="Response schema validation failed",
            error_code="SCHEMA_VALIDATION_ERROR",
            timestamp=datetime.utcnow(),
            details={"validation_errors": e.errors()}
        )

    except Exception as e:
        # Unexpected error
        logger.error(f"AI analysis failed: {str(e)}", exc_info=True)

        return AIAnalysisErrorResponse(
            status=ResponseStatus.ERROR,
            success=False,
            error_message=f"Analysis failed: {str(e)}",
            error_code="INTERNAL_ERROR",
            timestamp=datetime.utcnow(),
            details=None
        )


@router.post("/api/ai-analysis/compatibility")
async def compatibility_ai_analysis_simplified(
    request: SimpleAIAnalysisRequest,
    user: User = Depends(get_current_user),
    db: dict = Depends(get_db)
):
    """
    Simplified AI-powered compatibility analysis endpoint.
    
    This endpoint:
    1. Extracts user_id from JWT token
    2. Fetches user's and partner's birth details from MongoDB
    3. Generates both Kundalis
    4. Extracts ML predictions for both
    5. Calculates compatibility astrology scores
    6. Generates AI compatibility analysis
    7. Returns complete response
    
    Note: Partner kundali must be fetched by partner_id (from request or stored in user profile).
    For now, uses user's kundali twice (self-compatibility) - modify as needed.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Compatibility analysis request from user: {user.id}")
        
        # 1. Fetch user's birth details
        # If user_kundali_name is provided, fetch that specific kundali
        # Otherwise, fetch the primary kundali (default)
        user_birth_details = None
        
        if request.user_kundali_name:
            try:
                # Try to fetch specific user kundali by name
                user_kundali_doc = db["kundalis"].find_one({
                    "user_id": str(user.id),
                    "name": request.user_kundali_name
                })
                if user_kundali_doc:
                    user_birth_details = {
                        'birth_date': user_kundali_doc.get('birth_date'),
                        'birth_time': user_kundali_doc.get('birth_time'),
                        'latitude': user_kundali_doc.get('latitude'),
                        'longitude': user_kundali_doc.get('longitude'),
                        'timezone': user_kundali_doc.get('timezone')
                    }
                    logger.info(f"Fetched user kundali: {request.user_kundali_name}")
            except Exception as e:
                logger.warning(f"Could not fetch user kundali '{request.user_kundali_name}': {str(e)}")
        
        # If no user kundali found by name, fetch the primary kundali
        if not user_birth_details:
            user_birth_details = get_user_birth_details(str(user.id), db)
            if not user_birth_details:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Your birth details not found. Please create a kundali first."
                )
        
        # 2. Fetch partner's birth details
        # If partner_kundali_name is provided, fetch that specific kundali
        # Otherwise, fetch the first non-primary kundali for the user
        # If none exist, use user's own kundali (for testing/self-analysis)
        partner_birth_details = None
        
        if request.partner_kundali_name:
            try:
                # Try to fetch specific partner kundali by name
                partner_kundali = db["kundalis"].find_one({
                    "user_id": str(user.id),
                    "name": request.partner_kundali_name
                })
                if partner_kundali:
                    partner_birth_details = {
                        'birth_date': partner_kundali.get('birth_date'),
                        'birth_time': partner_kundali.get('birth_time'),
                        'latitude': partner_kundali.get('latitude'),
                        'longitude': partner_kundali.get('longitude'),
                        'timezone': partner_kundali.get('timezone')
                    }
                    logger.info(f"Fetched partner kundali: {request.partner_kundali_name}")
            except Exception as e:
                logger.warning(f"Could not fetch partner kundali '{request.partner_kundali_name}': {str(e)}")
        
        # If no partner kundali found, try to fetch any non-primary kundali
        if not partner_birth_details:
            try:
                non_primary = db["kundalis"].find_one({
                    "user_id": str(user.id),
                    "is_primary": {"$ne": True}
                })
                if non_primary:
                    partner_birth_details = {
                        'birth_date': non_primary.get('birth_date'),
                        'birth_time': non_primary.get('birth_time'),
                        'latitude': non_primary.get('latitude'),
                        'longitude': non_primary.get('longitude'),
                        'timezone': non_primary.get('timezone')
                    }
                    logger.info("Using non-primary kundali as partner kundali")
            except Exception as e:
                logger.warning(f"Could not fetch non-primary kundali: {str(e)}")
        
        # If still no partner data, use user's own kundali (self-compatibility)
        if not partner_birth_details:
            partner_birth_details = user_birth_details
            logger.info("Using user's own kundali for partner (self-compatibility analysis)")
        
        # 2. Create KundaliRequests
        user_kundali_request = KundaliRequest(
            birthDate=user_birth_details['birth_date'],
            birthTime=user_birth_details['birth_time'],
            latitude=user_birth_details['latitude'],
            longitude=user_birth_details['longitude'],
            timezone=user_birth_details['timezone']
        )
        
        partner_kundali_request = KundaliRequest(
            birthDate=partner_birth_details['birth_date'],
            birthTime=partner_birth_details['birth_time'],
            latitude=partner_birth_details['latitude'],
            longitude=partner_birth_details['longitude'],
            timezone=partner_birth_details['timezone']
        )
        
        # 3. Generate both kundalis
        astro_start = time.time()
        user_kundali = await generate_kundali_logic(user_kundali_request)
        partner_kundali = await generate_kundali_logic(partner_kundali_request)
        astro_calc_time = (time.time() - astro_start) * 1000
        
        # 4. Extract scores with ML timing
        ml_start = time.time()
        ml_scores = extract_ml_predictions(user_kundali)
        partner_ml_scores = extract_ml_predictions(partner_kundali)
        ml_inference_time_ms = (time.time() - ml_start) * 1000
        
        # 5. Extract compatibility astrology scores
        astro_start = time.time()
        astrology_scores = extract_astrology_scores(user_kundali, partner_kundali)
        astro_calc_time += (time.time() - astro_start) * 1000
        
        # 6. Validate
        _validate_ml_scores_runtime(ml_scores)
        _validate_astrology_scores_runtime(astrology_scores)
        if partner_ml_scores is not None:
            _validate_ml_scores_structure(partner_ml_scores, "partner_ml_scores")
        
        # 7. Generate AI analysis with LLM
        ai_analysis, llm_metadata = generate_ai_analysis(
            ml_scores, 
            astrology_scores, 
            "compatibility", 
            partner_ml_scores
        )
        
        # 8. Build response
        total_time = (time.time() - start_time) * 1000
        metadata = AnalysisMetadata(
            calculation_timestamp=datetime.utcnow(),
            ml_inference_time_ms=ml_inference_time_ms,
            astro_calc_time_ms=astro_calc_time,
            total_time_ms=total_time,
            llm_input_tokens=llm_metadata.get("input_tokens"),
            llm_output_tokens=llm_metadata.get("output_tokens"),
            llm_cost_usd=llm_metadata.get("cost_usd"),
            llm_request_duration_ms=llm_metadata.get("request_duration_ms"),
            llm_cache_hit=llm_metadata.get("cache_hit"),
            llm_model=llm_metadata.get("model"),
            llm_fallback=llm_metadata.get("fallback")
        )
        
        logger.info(f"Compatibility analysis completed in {total_time:.2f}ms")
        
        return AIAnalysisResponse(
            status=ResponseStatus.SUCCESS,
            success=True,
            data=AIAnalysisData(
                ml_scores=ml_scores,
                partner_ml_scores=partner_ml_scores,
                astrology_scores=astrology_scores,
                ai_analysis=ai_analysis,
                metadata=metadata
            ),
            timestamp=datetime.utcnow(),
            error_message=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Compatibility analysis failed: {str(e)}", exc_info=True)
        return AIAnalysisErrorResponse(
            status=ResponseStatus.ERROR,
            success=False,
            error_message=f"Compatibility analysis failed: {str(e)}",
            error_code="COMPATIBILITY_ANALYSIS_FAILED",
            timestamp=datetime.utcnow(),
            details=None
        )


@router.post("/api/ai-analysis/compatibility/full")
async def compatibility_ai_analysis(request: CompatibilityAnalysisRequest):
    """
    Full AI-powered compatibility analysis endpoint (with explicit birth data).
    
    DEPRECATED: Use POST /api/ai-analysis/compatibility (simplified version) instead.
    
    This is kept for backward compatibility.
    """
    start_time = time.time()
    astro_calc_time = 0
    ml_inference_time_ms: Optional[float] = None

    try:
        # Generate both kundalis
        astro_start = time.time()
        user_kundali = await generate_kundali_logic(request.user_kundali)
        partner_kundali = await generate_kundali_logic(request.partner_kundali)
        astro_calc_time += (time.time() - astro_start) * 1000

        # Extract scores with ML timing
        ml_start = time.time()
        ml_scores = extract_ml_predictions(user_kundali)
        partner_ml_scores = extract_ml_predictions(partner_kundali)
        ml_inference_time_ms = (time.time() - ml_start) * 1000

        astro_start = time.time()
        astrology_scores = extract_astrology_scores(user_kundali, partner_kundali)
        astro_calc_time += (time.time() - astro_start) * 1000

        # Validate
        _validate_ml_scores_runtime(ml_scores)
        _validate_astrology_scores_runtime(astrology_scores)

        # Validate partner_ml_scores if present (must be Dict[str, MLScoreBox] or None)
        if partner_ml_scores is not None:
            _validate_ml_scores_structure(partner_ml_scores, "partner_ml_scores")

        # Generate analysis with LLM
        ai_analysis, llm_metadata = generate_ai_analysis(ml_scores, astrology_scores, "compatibility", partner_ml_scores)

        # Build response with LLM metadata
        total_time = (time.time() - start_time) * 1000
        metadata = AnalysisMetadata(
            calculation_timestamp=datetime.utcnow(),
            ml_inference_time_ms=ml_inference_time_ms,
            astro_calc_time_ms=astro_calc_time,
            total_time_ms=total_time,
            llm_input_tokens=llm_metadata.get("input_tokens"),
            llm_output_tokens=llm_metadata.get("output_tokens"),
            llm_cost_usd=llm_metadata.get("cost_usd"),
            llm_request_duration_ms=llm_metadata.get("request_duration_ms"),
            llm_cache_hit=llm_metadata.get("cache_hit"),
            llm_model=llm_metadata.get("model"),
            llm_fallback=llm_metadata.get("fallback")
        )

        return AIAnalysisResponse(
            status=ResponseStatus.SUCCESS,
            success=True,
            data=AIAnalysisData(
                ml_scores=ml_scores,
                partner_ml_scores=partner_ml_scores,
                astrology_scores=astrology_scores,
                ai_analysis=ai_analysis,
                metadata=metadata
            ),
            timestamp=datetime.utcnow(),
            error_message=None
        )

    except Exception as e:
        logger.error(f"Compatibility analysis failed: {str(e)}")
        return AIAnalysisErrorResponse(
            status=ResponseStatus.ERROR,
            success=False,
            error_message=str(e),
            error_code="COMPATIBILITY_ANALYSIS_FAILED",
            timestamp=datetime.utcnow(),
            details=None
        )


@router.get("/api/ai-analysis/health", status_code=status.HTTP_200_OK)
async def ai_analysis_health():
    """
    Health check for AI analysis service.

    Returns:
        Dict with service status and component availability
    """
    return {
        "status": "healthy",
        "ml_available": ML_AVAILABLE and MODELS_LOADED,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/api/ai-analysis/token-usage", status_code=status.HTTP_200_OK)
async def token_usage_metrics():
    """
    Get LLM token usage metrics and cost tracking.

    Returns:
        Token usage summary with:
        - Total tokens used (input + output)
        - Total cost in USD
        - Per-endpoint breakdown
        - Cache hit rate
        - Cost estimates for projected usage
    """
    try:
        tracker = get_token_tracker()
        summary = tracker.get_summary()

        return {
            "status": "success",
            "data": summary,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get token usage metrics: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/api/ai-analysis/cost-estimate", status_code=status.HTTP_200_OK)
async def cost_estimate(projected_requests: int = 1000):
    """
    Get cost estimate for projected number of API requests.

    Args:
        projected_requests: Number of requests to project (default: 1000)

    Returns:
        Cost estimate based on historical token usage patterns
    """
    try:
        if projected_requests < 1:
            return {
                "status": "error",
                "error": "projected_requests must be >= 1",
                "timestamp": datetime.utcnow().isoformat()
            }

        tracker = get_token_tracker()
        estimate = tracker.get_cost_estimate(projected_requests)

        return {
            "status": "success",
            "data": estimate,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to estimate cost: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
