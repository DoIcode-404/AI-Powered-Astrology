from typing import Dict, Any

class KundaliFeatureEngineer:
    """
    Advanced feature engineering for ML model training.
    """
    
    @staticmethod
    def create_interaction_features(ml_features: Dict[str, Any]) -> Dict[str, Any]:
        """Create interaction features between planets and houses."""
        interactions = {}
        
        # Planet-House interactions
        for planet in ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]:
            planet_house = ml_features["planets"].get(f"{planet}_house", 1)
            planet_sign = ml_features["planets"].get(f"{planet}_sign_number", 1)
            
            interactions[f"{planet}_house_sign_interaction"] = planet_house * planet_sign
            interactions[f"{planet}_angular_house"] = 1 if planet_house in [1, 4, 7, 10] else 0
            interactions[f"{planet}_succedent_house"] = 1 if planet_house in [2, 5, 8, 11] else 0
            interactions[f"{planet}_cadent_house"] = 1 if planet_house in [3, 6, 9, 12] else 0
        
        # Moon-Sun relationship (important for personality)
        sun_sign = ml_features["planets"].get("sun_sign_number", 1)
        moon_sign = ml_features["planets"].get("moon_sign_number", 1)
        interactions["sun_moon_sign_difference"] = abs(sun_sign - moon_sign)
        interactions["sun_moon_same_element"] = KundaliFeatureEngineer.same_element(sun_sign, moon_sign)
        
        # Benefic-Malefic ratios
        benefic_houses = 0
        malefic_houses = 0
        
        for planet in ["jupiter", "venus", "moon"]:  # Natural benefics
            if f"{planet}_house" in ml_features["planets"]:
                house = ml_features["planets"][f"{planet}_house"]
                if house in [1, 4, 7, 10]:  # Angular houses
                    benefic_houses += 2
                elif house in [2, 5, 8, 11]:  # Succedent
                    benefic_houses += 1
        
        for planet in ["sun", "mars", "saturn"]:  # Natural malefics
            if f"{planet}_house" in ml_features["planets"]:
                house = ml_features["planets"][f"{planet}_house"]
                if house in [1, 4, 7, 10]:
                    malefic_houses += 2
                elif house in [2, 5, 8, 11]:
                    malefic_houses += 1
        
        interactions["benefic_malefic_ratio"] = benefic_houses / max(malefic_houses, 1)
        
        return interactions
    
    @staticmethod
    def same_element(sign1: int, sign2: int) -> int:
        """Check if two signs belong to same element."""
        elements = {
            1: 1, 5: 1, 9: 1,    # Fire: Aries, Leo, Sagittarius
            2: 2, 6: 2, 10: 2,   # Earth: Taurus, Virgo, Capricorn
            3: 3, 7: 3, 11: 3,   # Air: Gemini, Libra, Aquarius
            4: 4, 8: 4, 12: 4    # Water: Cancer, Scorpio, Pisces
        }
        return 1 if elements.get(sign1) == elements.get(sign2) else 0
    
    @staticmethod
    def create_temporal_features(birth_details: Dict[str, Any]) -> Dict[str, Any]:
        """Create time-based features for ML training."""
        temporal_features = {}
        
        # Birth year features
        birth_year = birth_details.get("birth_year", 2000)
        temporal_features["birth_decade"] = birth_year // 10
        temporal_features["birth_century"] = birth_year // 100
        temporal_features["is_leap_year"] = 1 if birth_year % 4 == 0 else 0
        
        # Birth month features
        birth_month = birth_details.get("birth_month", 1)
        temporal_features["birth_season"] = (birth_month - 1) // 3 + 1  # 1=Spring, 2=Summer, etc.
        temporal_features["birth_quarter"] = (birth_month - 1) // 3 + 1
        
        # Birth hour features
        birth_hour = birth_details.get("birth_hour", 12)
        temporal_features["birth_time_of_day"] = KundaliFeatureEngineer.get_time_period(birth_hour)
        temporal_features["is_day_birth"] = 1 if 6 <= birth_hour <= 18 else 0
        temporal_features["is_night_birth"] = 1 if birth_hour < 6 or birth_hour > 18 else 0
        
        return temporal_features
    
    @staticmethod
    def get_time_period(hour: int) -> int:
        """Classify birth hour into periods."""
        if 5 <= hour < 9:
            return 1  # Early morning
        elif 9 <= hour < 12:
            return 2  # Late morning
        elif 12 <= hour < 17:
            return 3  # Afternoon
        elif 17 <= hour < 21:
            return 4  # Evening
        else:
            return 5  # Night
    
    @staticmethod
    def create_geographical_features(birth_details: Dict[str, Any]) -> Dict[str, Any]:
        """Create location-based features."""
        geo_features = {}
        
        lat = birth_details.get("latitude", 0)
        lon = birth_details.get("longitude", 0)
        
        # Hemisphere features
        geo_features["northern_hemisphere"] = 1 if lat > 0 else 0
        geo_features["southern_hemisphere"] = 1 if lat < 0 else 0
        geo_features["eastern_hemisphere"] = 1 if lon > 0 else 0
        geo_features["western_hemisphere"] = 1 if lon < 0 else 0
        
        # Latitude bands
        abs_lat = abs(lat)
        if abs_lat < 23.5:
            geo_features["latitude_band"] = 1  # Tropical
        elif abs_lat < 66.5:
            geo_features["latitude_band"] = 2  # Temperate
        else:
            geo_features["latitude_band"] = 3  # Polar
        
        # Distance from equator and prime meridian
        geo_features["distance_from_equator"] = abs_lat
        geo_features["distance_from_prime_meridian"] = abs(lon)
        
        return geo_features

