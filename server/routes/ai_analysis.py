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

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, ValidationError

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

class AIAnalysisRequest(BaseModel):
    """Request for AI-powered analysis."""
    user_kundali: KundaliRequest = Field(..., description="User's birth chart data")
    partner_kundali: Optional[KundaliRequest] = Field(None, description="Partner's birth chart data (optional)")
    context: str = Field(default="general", description="Analysis context: general, compatibility, career, etc.")


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
                    strength = planet_data.get("strength_percentage", 0)
                    if strength > 0:
                        scores[f"{planet_name.lower()}_strength"] = float(strength)
                        logger.debug(f"Added {planet_name}: {strength}")

        # Calculate overall chart strength
        if scores:
            scores["overall_strength"] = float(sum(scores.values()) / len(scores))

        # Extract yoga counts
        yogas = shad_bala.get("yogas", {})
        if yogas:
            scores["total_yogas"] = int(yogas.get("total_yoga_count", 0))
            scores["benefic_yogas"] = int(yogas.get("benefic_yoga_count", 0))

    # If compatibility analysis, calculate Guna Milan
    if partner_kundali_data:
        try:
            calculator = CompatibilityCalculator()
            compatibility_result = calculator.calculate_compatibility(
                kundali_data,
                partner_kundali_data
            )

            if "guna_milan" in compatibility_result:
                guna_milan = compatibility_result["guna_milan"]
                scores["guna_milan_total"] = int(guna_milan.get("total_points", 0))

                for koota in guna_milan.get("kootas", []):
                    koota_name = koota.get("name", "unknown").lower().replace(" ", "_")
                    scores[f"koota_{koota_name}"] = float(koota.get("points_obtained", 0))

        except Exception as e:
            logger.warning(f"Compatibility calculation failed: {str(e)}")

    # Fallback only if truly no data
    if not scores:
        scores["overall_strength"] = 50.0

    return scores


def _validate_ml_scores_runtime(ml_scores: Any) -> None:
    """
    Runtime validation of ml_scores before Pydantic validation.

    Explicitly checks for dict type and MLScoreBox structure to catch
    Map<String,dynamic> vs List<dynamic> errors early with detailed logging.

    Args:
        ml_scores: ML scores to validate

    Raises:
        ValueError: If validation fails
    """
    # Check 1: Must be dict, not list
    if not isinstance(ml_scores, dict):
        error_msg = f"ml_scores must be dict, got {type(ml_scores).__name__}"
        logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
        logger.error(f"ml_scores payload: {ml_scores}")
        raise ValueError(error_msg)

    # Check 2: Must not be empty
    if not ml_scores:
        error_msg = "ml_scores cannot be empty"
        logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
        raise ValueError(error_msg)

    # Check 3: All keys must be strings
    for key in ml_scores.keys():
        if not isinstance(key, str):
            error_msg = f"ml_scores key must be string, got {type(key).__name__}: {key}"
            logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
            logger.error(f"ml_scores payload: {ml_scores}")
            raise ValueError(error_msg)

    # Check 4: All values must be MLScoreBox instances with required fields
    for key, value in ml_scores.items():
        if not isinstance(value, MLScoreBox):
            error_msg = f"ml_scores['{key}'] must be MLScoreBox, got {type(value).__name__}"
            logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
            logger.error(f"Value: {value}")
            raise ValueError(error_msg)

        # Check required fields
        if not hasattr(value, 'score') or not hasattr(value, 'confidence') or not hasattr(value, 'model_version'):
            error_msg = f"ml_scores['{key}'] missing required fields"
            logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
            logger.error(f"Value: {value}")
            raise ValueError(error_msg)

        # Check numeric types
        if not isinstance(value.score, (int, float)):
            error_msg = f"ml_scores['{key}'].score must be numeric, got {type(value.score).__name__}"
            logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
            raise ValueError(error_msg)

        if not isinstance(value.confidence, (int, float)):
            error_msg = f"ml_scores['{key}'].confidence must be numeric, got {type(value.confidence).__name__}"
            logger.error(f"RUNTIME VALIDATION FAILED: {error_msg}")
            raise ValueError(error_msg)

    logger.debug(f"Runtime validation passed for ml_scores with {len(ml_scores)} entries")


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


def generate_ai_analysis(
    ml_scores: Dict[str, MLScoreBox],
    astrology_scores: Dict[str, float],
    context: str
) -> AIAnalysisSection:
    """Generate AI-powered textual analysis."""
    # Calculate average ML score (0-100 scale)
    avg_ml_score = sum(box.score for box in ml_scores.values()) / len(ml_scores) if ml_scores else 50.0
    avg_astro_score = sum(astrology_scores.values()) / len(astrology_scores) if astrology_scores else 50.0

    # Generate summary
    if context == "compatibility":
        guna_milan = astrology_scores.get("guna_milan_total", 0)
        summary = f"Compatibility: {guna_milan}/36 points. ML predicts {avg_ml_score:.1f}/100 harmony."
    else:
        summary = f"Chart strength: {avg_astro_score:.1f}/100. ML predictions average {avg_ml_score:.1f}/100."

    # Generate insights
    insights = []
    for score_name, score_box in ml_scores.items():
        if score_box.score > 75:
            insights.append(f"Strong {score_name}: {score_box.score:.1f}/100")
        elif score_box.score < 50:
            insights.append(f"Attention needed in {score_name}: {score_box.score:.1f}/100")

    # Astrology insights
    if astrology_scores.get("overall_strength", 0) > 70:
        insights.append(f"Strong planetary positions: {astrology_scores['overall_strength']:.1f}/100")

    # Generate recommendations
    recommendations = []
    if avg_ml_score < 60:
        recommendations.append("Focus on areas scoring below 60 through targeted remedies")
    if context == "compatibility" and astrology_scores.get("guna_milan_total", 0) < 18:
        recommendations.append("Guna Milan below 18 - consider astrological consultation")
    if not recommendations:
        recommendations.append("Maintain current positive trajectory")

    return AIAnalysisSection(
        summary=summary,
        detailed_insights=insights if insights else ["Analysis complete"],
        recommendations=recommendations
    )


# ========== ENDPOINTS ==========

@router.post(
    "/api/ai-analysis",
    response_model=AIAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        503: {"model": AIAnalysisErrorResponse, "description": "ML service unavailable"},
        500: {"model": AIAnalysisErrorResponse, "description": "Server error"}
    }
)
async def ai_analysis_endpoint(request: AIAnalysisRequest):
    """
    Perform AI-powered astrology analysis combining ML predictions with deterministic calculations.

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
    ml_inference_time = 0

    try:
        # 1. Generate user kundali
        astro_start = time.time()
        user_kundali = await generate_kundali_logic(request.user_kundali)
        astro_calc_time += (time.time() - astro_start) * 1000

        # 2. Generate partner kundali if provided
        partner_kundali = None
        if request.partner_kundali:
            astro_start = time.time()
            partner_kundali = await generate_kundali_logic(request.partner_kundali)
            astro_calc_time += (time.time() - astro_start) * 1000

        # 3. Extract ML predictions
        ml_start = time.time()
        ml_scores = extract_ml_predictions(user_kundali)
        ml_inference_time = (time.time() - ml_start) * 1000

        # 4. Extract astrology scores
        astro_start = time.time()
        astrology_scores = extract_astrology_scores(user_kundali, partner_kundali)
        astro_calc_time += (time.time() - astro_start) * 1000

        # 5. Runtime validation of ml_scores (before Pydantic)
        _validate_ml_scores_runtime(ml_scores)
        _validate_astrology_scores_runtime(astrology_scores)

        # 6. Generate AI analysis
        ai_analysis = generate_ai_analysis(ml_scores, astrology_scores, request.context)

        # 8. Construct metadata
        total_time = (time.time() - start_time) * 1000
        metadata = AnalysisMetadata(
            calculation_timestamp=datetime.utcnow(),
            ml_inference_time_ms=ml_inference_time,
            astro_calc_time_ms=astro_calc_time,
            total_time_ms=total_time
        )

        # 9. Construct response data
        analysis_data = AIAnalysisData(
            ml_scores=ml_scores,
            astrology_scores=astrology_scores,
            ai_analysis=ai_analysis,
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
        logger.info(f"AI analysis completed in {total_time:.2f}ms (ML: {ml_inference_time:.2f}ms, Astro: {astro_calc_time:.2f}ms)")

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
