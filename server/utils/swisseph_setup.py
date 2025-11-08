import swisseph as swe
import os
import logging

logger = logging.getLogger(__name__)

# Set the ephemeris path
def setup_ephemeris():
    ephe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "swisseph_data"))
    if os.path.exists(ephe_path):
        swe.set_ephe_path(ephe_path)
        logger.info(f"[OK] Swiss Ephemeris path set to: {ephe_path}")
    else:
        logger.warning(f"[WARN] Ephemeris folder not found at: {ephe_path}. Using system default ephemeris data.")
        # Don't crash - swe will use its default ephemeris data
