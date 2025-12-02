"""
Horoscope Generator Background Job
Automatically generates and caches daily horoscopes for all zodiac signs using APScheduler.
"""

import logging
from datetime import datetime, date
from typing import Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from server.services.horoscope_service import HoroscopeService, ZODIAC_SIGNS
from server.database import get_db

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler: Optional[BackgroundScheduler] = None
horoscope_service = HoroscopeService()


def generate_daily_horoscopes_batch(target_date: Optional[date] = None):
    """
    Generate horoscopes for all 12 zodiac signs for a specific date.

    Args:
        target_date: Target date for horoscope generation (defaults to today)
    """
    if target_date is None:
        target_date = date.today()

    try:
        db = get_db()
        generated_count = 0
        failed_signs = []

        logger.info(f"Starting batch horoscope generation for {target_date}")

        for sign in ZODIAC_SIGNS:
            try:
                # Generate daily horoscope
                horoscope_data = horoscope_service.generate_daily_horoscope(
                    zodiac_sign=sign,
                    target_date=target_date
                )

                # Cache in database
                cache_key = f"horoscope:{sign}:{target_date.isoformat()}"
                db["horoscopes"].update_one(
                    {"_id": cache_key},
                    {
                        "$set": {
                            "zodiac_sign": sign,
                            "date": target_date.isoformat(),
                            "type": "daily",
                            "data": horoscope_data,
                            "generated_at": datetime.utcnow(),
                            "ttl": datetime.utcnow()  # TTL index will auto-delete after 30 days
                        }
                    },
                    upsert=True
                )

                generated_count += 1
                logger.debug(f"Generated horoscope for {sign} on {target_date}")

            except Exception as e:
                logger.error(f"Failed to generate horoscope for {sign}: {str(e)}")
                failed_signs.append(sign)

        logger.info(
            f"Batch horoscope generation completed: {generated_count}/{len(ZODIAC_SIGNS)} successful. "
            f"Failed: {len(failed_signs)}. Date: {target_date}"
        )

        if failed_signs:
            logger.warning(f"Failed signs: {', '.join(failed_signs)}")

    except Exception as e:
        logger.error(f"Critical error in batch horoscope generation: {str(e)}", exc_info=True)


def generate_weekly_horoscopes_batch(week_start: Optional[date] = None):
    """
    Generate weekly horoscopes for all zodiac signs.

    Args:
        week_start: Start date of the week (defaults to current week start)
    """
    if week_start is None:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

    try:
        db = get_db()
        generated_count = 0

        logger.info(f"Starting batch weekly horoscope generation for week starting {week_start}")

        for sign in ZODIAC_SIGNS:
            try:
                # Generate weekly horoscope
                horoscope_data = horoscope_service.generate_weekly_horoscope(
                    zodiac_sign=sign,
                    week_start=week_start
                )

                # Cache in database
                cache_key = f"horoscope_weekly:{sign}:{week_start.isoformat()}"
                db["horoscopes"].update_one(
                    {"_id": cache_key},
                    {
                        "$set": {
                            "zodiac_sign": sign,
                            "week_start": week_start.isoformat(),
                            "type": "weekly",
                            "data": horoscope_data,
                            "generated_at": datetime.utcnow(),
                            "ttl": datetime.utcnow()
                        }
                    },
                    upsert=True
                )

                generated_count += 1
                logger.debug(f"Generated weekly horoscope for {sign}")

            except Exception as e:
                logger.error(f"Failed to generate weekly horoscope for {sign}: {str(e)}")

        logger.info(f"Weekly horoscope generation completed: {generated_count}/{len(ZODIAC_SIGNS)} successful")

    except Exception as e:
        logger.error(f"Critical error in weekly horoscope generation: {str(e)}", exc_info=True)


def generate_monthly_horoscopes_batch(year_month: Optional[str] = None):
    """
    Generate monthly horoscopes for all zodiac signs.

    Args:
        year_month: Year-month string (YYYY-MM), defaults to current month
    """
    if year_month is None:
        today = date.today()
        year_month = f"{today.year}-{today.month:02d}"

    try:
        db = get_db()
        generated_count = 0

        logger.info(f"Starting batch monthly horoscope generation for {year_month}")

        for sign in ZODIAC_SIGNS:
            try:
                # Generate monthly horoscope
                horoscope_data = horoscope_service.generate_monthly_horoscope(
                    zodiac_sign=sign,
                    year_month=year_month
                )

                # Cache in database
                cache_key = f"horoscope_monthly:{sign}:{year_month}"
                db["horoscopes"].update_one(
                    {"_id": cache_key},
                    {
                        "$set": {
                            "zodiac_sign": sign,
                            "year_month": year_month,
                            "type": "monthly",
                            "data": horoscope_data,
                            "generated_at": datetime.utcnow(),
                            "ttl": datetime.utcnow()
                        }
                    },
                    upsert=True
                )

                generated_count += 1
                logger.debug(f"Generated monthly horoscope for {sign}")

            except Exception as e:
                logger.error(f"Failed to generate monthly horoscope for {sign}: {str(e)}")

        logger.info(f"Monthly horoscope generation completed: {generated_count}/{len(ZODIAC_SIGNS)} successful")

    except Exception as e:
        logger.error(f"Critical error in monthly horoscope generation: {str(e)}", exc_info=True)


def start_horoscope_scheduler():
    """
    Initialize and start the background horoscope generation scheduler.
    Called during application startup.
    """
    global scheduler

    try:
        if scheduler is not None:
            logger.warning("Horoscope scheduler already running")
            return

        # Create scheduler
        scheduler = BackgroundScheduler()

        # Job 1: Generate daily horoscopes every day at 00:30 UTC
        scheduler.add_job(
            generate_daily_horoscopes_batch,
            trigger=CronTrigger(hour=0, minute=30, timezone='UTC'),
            id='daily_horoscope_generation',
            name='Daily horoscope generation for all zodiac signs',
            replace_existing=True,
            misfire_grace_time=300  # 5 minutes grace period
        )

        # Job 2: Generate weekly horoscopes every Monday at 01:00 UTC
        scheduler.add_job(
            generate_weekly_horoscopes_batch,
            trigger=CronTrigger(day_of_week='0', hour=1, minute=0, timezone='UTC'),  # Monday
            id='weekly_horoscope_generation',
            name='Weekly horoscope generation for all zodiac signs',
            replace_existing=True,
            misfire_grace_time=300
        )

        # Job 3: Generate monthly horoscopes on 1st of each month at 01:30 UTC
        scheduler.add_job(
            generate_monthly_horoscopes_batch,
            trigger=CronTrigger(day=1, hour=1, minute=30, timezone='UTC'),
            id='monthly_horoscope_generation',
            name='Monthly horoscope generation for all zodiac signs',
            replace_existing=True,
            misfire_grace_time=300
        )

        # Start the scheduler
        scheduler.start()
        logger.info("Horoscope scheduler started successfully with 3 jobs:")
        logger.info("  - Daily generation: Every day at 00:30 UTC")
        logger.info("  - Weekly generation: Every Monday at 01:00 UTC")
        logger.info("  - Monthly generation: 1st of each month at 01:30 UTC")

    except Exception as e:
        logger.error(f"Failed to start horoscope scheduler: {str(e)}", exc_info=True)


def stop_horoscope_scheduler():
    """
    Gracefully shutdown the background horoscope generation scheduler.
    Called during application shutdown.
    """
    global scheduler

    try:
        if scheduler is not None:
            scheduler.shutdown(wait=True)
            scheduler = None
            logger.info("Horoscope scheduler stopped successfully")
        else:
            logger.warning("Horoscope scheduler is not running")
    except Exception as e:
        logger.error(f"Error stopping horoscope scheduler: {str(e)}", exc_info=True)


def get_scheduler_status() -> dict:
    """
    Get the current status of the horoscope scheduler.

    Returns:
        Status dictionary with running jobs and next run times
    """
    global scheduler

    if scheduler is None or not scheduler.running:
        return {
            "status": "stopped",
            "running": False,
            "jobs": []
        }

    jobs_info = []
    for job in scheduler.get_jobs():
        jobs_info.append({
            "id": job.id,
            "name": job.name,
            "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger)
        })

    return {
        "status": "running",
        "running": scheduler.running,
        "jobs": jobs_info
    }


# Import at module level to avoid circular imports
from datetime import timedelta
