from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

geolocator = Nominatim(user_agent="kundali_app")
tf = TimezoneFinder()

def geocode_location(location: str):
    """Get lat/lon/tz from location string"""
    geo = geolocator.geocode(location)
    if not geo:
        raise ValueError(f"Cannot geocode location: {location}")

    tz = tf.timezone_at(lat=geo.latitude, lng=geo.longitude)

    return {
        'latitude': geo.latitude,
        'longitude': geo.longitude,
        'timezone': tz or 'UTC'
    }
