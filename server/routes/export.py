"""
Export Routes
Handles Kundali export to various formats (CSV, JSON, PDF).

All responses follow standardized APIResponse format.

Author: Backend API Team
"""

from fastapi import APIRouter, HTTPException
import logging

from server.pydantic_schemas.api_response import APIResponse

# Note: ML exporter imports removed - pandas/ML dependencies not available in production
# ML features are only available in development with requirements-ml.txt

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/kundali-csv', response_model=APIResponse, tags=["Export"])
async def export_kundali_csv() -> APIResponse:
    """
    Generate Kundali and export to CSV format.

    Args:
        request: Birth details for Kundali generation

    Returns:
        APIResponse with error message (CSV export not available in production)
    """
    logger.warning("CSV export endpoint called - feature not available in production")
    raise HTTPException(
        status_code=503,
        detail="CSV export is only available in development mode. Install requirements-ml.txt for ML features."
    )


@router.post('/kundali-json', response_model=APIResponse, tags=["Export"])
async def export_kundali_json() -> APIResponse:
    """
    Generate Kundali and export to JSON format.

    Returns:
        APIResponse with error message (JSON export not available in production)
    """
    logger.warning("JSON export endpoint called - feature not available in production")
    raise HTTPException(
        status_code=503,
        detail="JSON export is only available in development mode. Install requirements-ml.txt for ML features."
    )


@router.post('/batch-kundali-csv', response_model=APIResponse, tags=["Export"])
async def export_batch_kundali_csv() -> APIResponse:
    """
    Batch CSV export endpoint.

    Returns:
        APIResponse with error message (batch CSV export not available in production)
    """
    logger.warning("Batch CSV export endpoint called - feature not available in production")
    raise HTTPException(
        status_code=503,
        detail="Batch CSV export is only available in development mode. Install requirements-ml.txt for ML features."
    )


@router.post('/batch-kundali-json', response_model=APIResponse, tags=["Export"])
async def export_batch_kundali_json() -> APIResponse:
    """
    Batch JSON export endpoint.

    Returns:
        APIResponse with error message (batch JSON export not available in production)
    """
    logger.warning("Batch JSON export endpoint called - feature not available in production")
    raise HTTPException(
        status_code=503,
        detail="Batch JSON export is only available in development mode. Install requirements-ml.txt for ML features."
    )