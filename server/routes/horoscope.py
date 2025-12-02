"""
Zodiac Horoscope Routes
Daily, weekly, and monthly horoscopes for all 12 zodiac signs.

Endpoints:
1. GET /daily/{sign} - Daily horoscope
2. GET /weekly/{sign} - Weekly horoscope
3. GET /monthly/{sign} - Monthly horoscope
4. GET /all-signs/daily - All signs daily horoscope
5. GET /archive/{sign} - Historical horoscope archive
"""

import logging
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status
from dateutil.parser import parse as parse_date

from server.database import get_db
from server.services.horoscope_service import HoroscopeService, ZODIAC_SIGNS
from server.pydantic_schemas.api_response import APIResponse, success_response, error_response

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Horoscope"]
)

# Initialize horoscope service
horoscope_service = HoroscopeService()


# ========== ENDPOINT 1: Daily Horoscope ==========

@router.get("/daily/{sign}", response_model=APIResponse)
async def get_daily_horoscope(
    sign: str,
    date_str: Optional[str] = None,
    db: dict = Depends(get_db)
) -> APIResponse:
    """
    Get daily horoscope for zodiac sign.

    Args:
        sign: Zodiac sign (e.g., "aries", "taurus")
        date_str: Optional date (YYYY-MM-DD), defaults to today

    Returns:
        Daily horoscope with 9 life areas
    """
    try:
        # Normalize sign name
        sign = sign.capitalize()

        if sign not in ZODIAC_SIGNS:
            return error_response(
                code="INVALID_SIGN",
                message=f"Invalid zodiac sign. Valid signs: {', '.join(ZODIAC_SIGNS)}",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        # Parse date
        if date_str:
            try:
                target_date = parse_date(date_str).date()
            except:
                return error_response(
                    code="INVALID_DATE",
                    message="Date format should be YYYY-MM-DD",
                    http_status=status.HTTP_400_BAD_REQUEST
                )
        else:
            target_date = date.today()

        # Check cache
        cached = await _get_cached_horoscope(db, sign, "daily", target_date.isoformat())
        if cached:
            return success_response(
                data=cached,
                message="Daily horoscope (from cache)"
            )

        # Generate horoscope
        horoscope = horoscope_service.generate_daily_horoscope(sign, target_date)

        # Cache result
        await _cache_horoscope(db, sign, "daily", horoscope)

        return success_response(
            data=horoscope,
            message=f"Daily horoscope for {sign}"
        )

    except ValueError as e:
        return error_response(
            code="INVALID_REQUEST",
            message=str(e),
            http_status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error generating daily horoscope: {str(e)}", exc_info=True)
        return error_response(
            code="GENERATION_ERROR",
            message=f"Error generating horoscope: {str(e)}",
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== ENDPOINT 2: Weekly Horoscope ==========

@router.get("/weekly/{sign}", response_model=APIResponse)
async def get_weekly_horoscope(
    sign: str,
    week: Optional[str] = None,
    db: dict = Depends(get_db)
) -> APIResponse:
    """
    Get weekly horoscope for zodiac sign.

    Args:
        sign: Zodiac sign
        week: Optional week (YYYY-W{01-52}), defaults to current week

    Returns:
        Weekly horoscope with daily breakdown
    """
    try:
        sign = sign.capitalize()

        if sign not in ZODIAC_SIGNS:
            return error_response(
                code="INVALID_SIGN",
                message=f"Invalid zodiac sign",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        # Generate horoscope
        horoscope = horoscope_service.generate_weekly_horoscope(sign)

        # Cache result
        await _cache_horoscope(db, sign, "weekly", horoscope)

        return success_response(
            data=horoscope,
            message=f"Weekly horoscope for {sign}"
        )

    except Exception as e:
        logger.error(f"Error generating weekly horoscope: {str(e)}", exc_info=True)
        return error_response(
            code="GENERATION_ERROR",
            message=str(e),
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== ENDPOINT 3: Monthly Horoscope ==========

@router.get("/monthly/{sign}", response_model=APIResponse)
async def get_monthly_horoscope(
    sign: str,
    month: Optional[str] = None,
    db: dict = Depends(get_db)
) -> APIResponse:
    """
    Get monthly horoscope for zodiac sign.

    Args:
        sign: Zodiac sign
        month: Optional month (YYYY-MM), defaults to current month

    Returns:
        Monthly horoscope with week summaries
    """
    try:
        sign = sign.capitalize()

        if sign not in ZODIAC_SIGNS:
            return error_response(
                code="INVALID_SIGN",
                message=f"Invalid zodiac sign",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        # Generate horoscope
        horoscope = horoscope_service.generate_monthly_horoscope(sign, month)

        # Cache result
        await _cache_horoscope(db, sign, "monthly", horoscope)

        return success_response(
            data=horoscope,
            message=f"Monthly horoscope for {sign}"
        )

    except Exception as e:
        logger.error(f"Error generating monthly horoscope: {str(e)}", exc_info=True)
        return error_response(
            code="GENERATION_ERROR",
            message=str(e),
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== ENDPOINT 4: All Signs Daily Horoscope ==========

@router.get("/all-signs/daily", response_model=APIResponse)
async def get_all_signs_daily_horoscope(
    date_str: Optional[str] = None,
    db: dict = Depends(get_db)
) -> APIResponse:
    """
    Get daily horoscopes for all 12 zodiac signs.

    Args:
        date_str: Optional date (YYYY-MM-DD), defaults to today

    Returns:
        All 12 zodiac signs with daily horoscopes
    """
    try:
        # Parse date
        if date_str:
            try:
                target_date = parse_date(date_str).date()
            except:
                return error_response(
                    code="INVALID_DATE",
                    message="Date format should be YYYY-MM-DD",
                    http_status=status.HTTP_400_BAD_REQUEST
                )
        else:
            target_date = date.today()

        horoscopes = []

        for sign in ZODIAC_SIGNS:
            try:
                # Check cache
                cached = await _get_cached_horoscope(db, sign, "daily", target_date.isoformat())
                if cached:
                    horoscopes.append(cached)
                else:
                    # Generate horoscope
                    horo = horoscope_service.generate_daily_horoscope(sign, target_date)
                    await _cache_horoscope(db, sign, "daily", horo)
                    horoscopes.append(horo)

            except Exception as e:
                logger.warning(f"Error generating horoscope for {sign}: {str(e)}")
                continue

        return success_response(
            data={
                "date": target_date.isoformat(),
                "horoscopes": horoscopes,
                "total_signs": len(horoscopes)
            },
            message=f"Daily horoscopes for all {len(horoscopes)} signs"
        )

    except Exception as e:
        logger.error(f"Error generating all signs horoscopes: {str(e)}", exc_info=True)
        return error_response(
            code="GENERATION_ERROR",
            message=str(e),
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== ENDPOINT 5: Horoscope Archive ==========

@router.get("/archive/{sign}", response_model=APIResponse)
async def get_horoscope_archive(
    sign: str,
    horo_type: str = "daily",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    limit: int = 30,
    db: dict = Depends(get_db)
) -> APIResponse:
    """
    Get horoscope history/archive for a sign.

    Args:
        sign: Zodiac sign
        horo_type: "daily", "weekly", or "monthly"
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        limit: Max results to return (default 30)

    Returns:
        Horoscope history for the specified date range
    """
    try:
        sign = sign.capitalize()

        if sign not in ZODIAC_SIGNS:
            return error_response(
                code="INVALID_SIGN",
                message="Invalid zodiac sign",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        if horo_type not in ["daily", "weekly", "monthly"]:
            return error_response(
                code="INVALID_TYPE",
                message="Type must be: daily, weekly, or monthly",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        # Query database
        horoscopes_collection = db["horoscopes"]

        query = {
            "zodiac_sign": sign,
            "type": horo_type
        }

        # Date range filter
        if from_date or to_date:
            date_query = {}
            if from_date:
                date_query["$gte"] = from_date
            if to_date:
                date_query["$lte"] = to_date
            if date_query:
                query["date"] = date_query

        # Fetch from database
        results = list(
            horoscopes_collection.find(query)
            .sort("date", -1)
            .limit(limit)
        )

        # Convert ObjectId to string
        for horo in results:
            horo["_id"] = str(horo["_id"])

        return success_response(
            data={
                "sign": sign,
                "type": horo_type,
                "total": len(results),
                "horoscopes": results
            },
            message=f"Retrieved {len(results)} {horo_type} horoscopes for {sign}"
        )

    except Exception as e:
        logger.error(f"Error retrieving horoscope archive: {str(e)}", exc_info=True)
        return error_response(
            code="ARCHIVE_ERROR",
            message=str(e),
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ========== HELPER FUNCTIONS ==========

async def _get_cached_horoscope(db: dict, sign: str, horo_type: str, date_key: str) -> Optional[dict]:
    """Get cached horoscope from database"""
    try:
        horoscopes_collection = db["horoscopes"]

        cached = horoscopes_collection.find_one({
            "zodiac_sign": sign,
            "type": horo_type,
            "date": date_key,
            "cache_expires_at": {"$gt": datetime.utcnow().isoformat()}
        })

        if cached:
            cached["_id"] = str(cached["_id"])
            logger.info(f"Retrieved cached horoscope: {sign} {horo_type}")
            return cached

        return None
    except Exception as e:
        logger.error(f"Error retrieving cached horoscope: {str(e)}")
        return None


async def _cache_horoscope(db: dict, sign: str, horo_type: str, horoscope: dict) -> None:
    """Cache horoscope in database"""
    try:
        horoscopes_collection = db["horoscopes"]

        doc = {
            "zodiac_sign": sign,
            "type": horo_type,
            "date": horoscope.get("date") or horoscope.get("month") or horoscope.get("week"),
            **horoscope
        }

        horoscopes_collection.insert_one(doc)
        logger.info(f"Cached horoscope: {sign} {horo_type}")
    except Exception as e:
        logger.error(f"Error caching horoscope: {str(e)}")
        # Non-critical error, continue without cache
