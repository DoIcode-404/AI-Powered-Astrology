"""
Background Jobs Module
Handles scheduled tasks like horoscope generation.
"""

from server.background_jobs.horoscope_generator import (
    start_horoscope_scheduler,
    stop_horoscope_scheduler,
    get_scheduler_status
)

__all__ = [
    "start_horoscope_scheduler",
    "stop_horoscope_scheduler",
    "get_scheduler_status"
]
