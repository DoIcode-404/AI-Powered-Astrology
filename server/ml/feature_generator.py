from typing import Dict, List, Any
from server.pydantic_schemas.kundali_schema import KundaliRequest
from server.utils.astro_utils import get_planetary_dignities ,get_ruling_planet, get_zodiac_sign, get_nakshatra

class KundaliMLDataGenerator:
    """
    Enhanced Kundali generator optimized for ML model training data preparation.
    """
    
    def __init__(self):
        self.sign_numbers = {
            "Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4,
            "Leo": 5, "Virgo": 6, "Libra": 7, "Scorpio": 8,
            "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12
        }
        
        self.planet_natural_significances = {
            "Sun": ["soul", "father", "government", "authority", "self", "vitality"],
            "Moon": ["mind", "mother", "emotions", "public", "water", "nurturing"],
            "Mars": ["energy", "courage", "siblings", "property", "surgery", "sports"],
            "Mercury": ["communication", "intelligence", "business", "education", "writing"],
            "Jupiter": ["wisdom", "teacher", "children", "spirituality", "expansion", "luck"],
            "Venus": ["love", "beauty", "arts", "luxury", "relationships", "creativity"],
            "Saturn": ["discipline", "delays", "karma", "hardwork", "service", "longevity"],
            "Rahu": ["illusion", "foreign", "technology", "sudden events", "material desires"],
            "Ketu": ["spirituality", "detachment", "past life", "moksha", "mysticism"]
        }
        
        self.house_significances = {
            1: ["self", "personality", "appearance", "health", "first_impressions"],
            2: ["wealth", "family", "speech", "food", "values", "possessions"],
            3: ["siblings", "communication", "short_travels", "courage", "hobbies"],
            4: ["home", "mother", "property", "education", "happiness", "vehicles"],
            5: ["children", "creativity", "romance", "education", "speculation"],
            6: ["enemies", "diseases", "service", "debts", "daily_routine", "pets"],
            7: ["marriage", "partnership", "public", "business", "spouse", "relationships"],
            8: ["transformation", "occult", "longevity", "inheritance", "mysteries"],
            9: ["luck", "dharma", "higher_education", "spirituality", "long_travels", "father"],
            10: ["career", "reputation", "authority", "social_status", "government"],
            11: ["gains", "friends", "aspirations", "elder_siblings", "income"],
            12: ["losses", "spirituality", "foreign", "isolation", "moksha", "expenses"]
        }

    def calculate_planetary_aspects(self, planet_positions: Dict[str, float]) -> Dict[str, List[Dict]]:
        """
        Calculate planetary aspects for ML training features.
        """
        aspects = {}
        aspect_degrees = [0, 60, 90, 120, 180]  # Conjunction, Sextile, Square, Trine, Opposition
        aspect_names = ["Conjunction", "Sextile", "Square", "Trine", "Opposition"]
        orb = 8  # 8-degree orb for aspects
        
        planets = list(planet_positions.keys())
        
        for i, planet1 in enumerate(planets):
            aspects[planet1] = []
            for j, planet2 in enumerate(planets):
                if i >= j:  # Avoid duplicate aspects
                    continue
                    
                pos1 = planet_positions[planet1]
                pos2 = planet_positions[planet2]
                
                # Calculate the shortest angular distance
                diff = abs(pos1 - pos2)
                if diff > 180:
                    diff = 360 - diff
                
                # Check for aspects
                for k, aspect_degree in enumerate(aspect_degrees):
                    if abs(diff - aspect_degree) <= orb:
                        aspects[planet1].append({
                            "aspected_planet": planet2,
                            "aspect_type": aspect_names[k],
                            "orb": abs(diff - aspect_degree),
                            "exact_degree_difference": diff,
                            "is_applying": pos1 < pos2,  # Simplified applying/separating logic
                            "strength": max(0, (orb - abs(diff - aspect_degree)) / orb)
                        })
        
        return aspects

    def calculate_planetary_strengths(self, planet_positions: Dict[str, float], 
                                    houses: Dict[int, List[str]], jd: float) -> Dict[str, Dict]:
        """
        Calculate various planetary strength indicators for ML features.
        """
        strengths = {}
        dignities = get_planetary_dignities(planet_positions)
        
        for planet, position in planet_positions.items():
            if planet in ["Rahu", "Ketu"]:
                continue
                
            sign = get_zodiac_sign(position)
            house = next((h for h, planets in houses.items() if planet in planets), 1)
            
            # Basic strength factors
            strength_data = {
                "dignity": dignities.get(planet, "Neutral"),
                "house_position": house,
                "sign_position": self.sign_numbers.get(sign, 1),
                "degree_in_sign": position % 30,
                "is_combust": self.is_combust(planet, planet_positions),
                "is_retrograde": self.is_retrograde(planet, jd),
                "house_lordship": self.get_house_lordships(planet),
                "positional_strength": self.calculate_positional_strength(planet, position),
                "directional_strength": self.calculate_directional_strength(planet, house),
                "temporal_strength": self.calculate_temporal_strength(planet, jd)
            }
            
            strengths[planet] = strength_data
        
        return strengths

    def is_combust(self, planet: str, planet_positions: Dict[str, float]) -> bool:
        """Check if planet is combust (too close to Sun)."""
        if planet == "Sun":
            return False
        
        combustion_degrees = {
            "Moon": 12, "Mars": 17, "Mercury": 14, 
            "Jupiter": 11, "Venus": 10, "Saturn": 15
        }
        
        if planet not in combustion_degrees:
            return False
        
        sun_pos = planet_positions.get("Sun", 0)
        planet_pos = planet_positions.get(planet, 0)
        
        diff = abs(sun_pos - planet_pos)
        if diff > 180:
            diff = 360 - diff
        
        return diff <= combustion_degrees[planet]

    def is_retrograde(self, planet: str, jd: float) -> bool:
        """Check if planet is retrograde (simplified)."""
        # This is a placeholder - you'd need to get speed from Swiss Ephemeris
        # For now, we'll use statistical probability
        retrograde_probabilities = {
            "Mercury": 0.19, "Venus": 0.07, "Mars": 0.09,
            "Jupiter": 0.32, "Saturn": 0.36
        }
        import random
        return random.random() < retrograde_probabilities.get(planet, 0)

    def get_house_lordships(self, planet: str) -> List[int]:
        """Get houses ruled by the planet."""
        lordships = {
            "Sun": [5], "Moon": [4], "Mars": [1, 8], "Mercury": [3, 6],
            "Jupiter": [9, 12], "Venus": [2, 7], "Saturn": [10, 11]
        }
        return lordships.get(planet, [])

    def calculate_positional_strength(self, planet: str, position: float) -> float:
        """Calculate positional strength (0-100)."""
        # Simplified positional strength based on sign and degree
        sign_strength = {
            "Sun": {"Aries": 100, "Leo": 100, "Libra": 0},
            "Moon": {"Taurus": 100, "Cancer": 100, "Scorpio": 0},
            # Add more sign strengths as needed
        }
        
        base_strength = 50  # Default neutral strength
        degree_in_sign = position % 30
        
        # Deep exaltation/debilitation points
        if degree_in_sign < 10:
            base_strength += 10
        elif degree_in_sign > 20:
            base_strength -= 5
        
        return min(100, max(0, base_strength))

    def calculate_directional_strength(self, planet: str, house: int) -> float:
        """Calculate directional strength (Dig Bala)."""
        directional_strength = {
            "Sun": {10: 100}, "Moon": {4: 100}, "Mars": {10: 100},
            "Mercury": {1: 100}, "Jupiter": {1: 100}, "Venus": {4: 100}, "Saturn": {7: 100}
        }
        
        return directional_strength.get(planet, {}).get(house, 50)

    def calculate_temporal_strength(self, planet: str, jd: float) -> float:
        """Calculate temporal strength (time-based)."""
        # This would involve complex calculations based on weekday, hora, etc.
        # For now, return a placeholder value
        return 50.0

    def generate_yogas(self, planet_positions: Dict[str, float], 
                      houses: Dict[int, List[str]], ascendant: float) -> List[Dict]:
        """
        Identify important yogas for ML training features.
        """
        yogas = []
        
        # Example: Raj Yoga (lords of kendra and trikona together)
        kendra_houses = [1, 4, 7, 10]
        trikona_houses = [1, 5, 9]
        
        # Check for planets in same houses
        for house, planets in houses.items():
            if len(planets) >= 2:
                yogas.append({
                    "yoga_name": "Conjunction",
                    "house": house,
                    "planets": planets,
                    "strength": len(planets) * 10,
                    "benefic": self.is_benefic_combination(planets)
                })
        
        # Add more yoga calculations here
        return yogas

    def is_benefic_combination(self, planets: List[str]) -> bool:
        """Check if planet combination is benefic."""
        benefic_planets = ["Jupiter", "Venus", "Moon", "Mercury"]
        malefic_planets = ["Sun", "Mars", "Saturn", "Rahu", "Ketu"]
        
        benefic_count = sum(1 for p in planets if p in benefic_planets)
        malefic_count = sum(1 for p in planets if p in malefic_planets)
        
        return benefic_count > malefic_count

    def generate_comprehensive_features(self, birth_details: KundaliRequest, 
                                      planet_positions: Dict[str, float],
                                      houses: Dict[int, List[str]], 
                                      ascendant: float, jd: float) -> Dict[str, Any]:
        """
        Generate comprehensive features for ML model training.
        """
        aspects = self.calculate_planetary_aspects(planet_positions)
        strengths = self.calculate_planetary_strengths(planet_positions, houses, jd)
        yogas = self.generate_yogas(planet_positions, houses, ascendant)
        
        # Birth details features
        birth_features = {
            "birth_year": int(birth_details.birthDate.split('-')[0]),
            "birth_month": int(birth_details.birthDate.split('-')[1]),
            "birth_day": int(birth_details.birthDate.split('-')[2]),
            "birth_hour": int(birth_details.birthTime.split(':')[0]),
            "birth_minute": int(birth_details.birthTime.split(':')[1]),
            "latitude": birth_details.latitude,
            "longitude": birth_details.longitude,
            "timezone": birth_details.timezone,
            "julian_day": jd
        }
        
        # Ascendant features
        asc_sign = get_zodiac_sign(ascendant)
        asc_nakshatra, asc_pada = get_nakshatra(ascendant)
        
        ascendant_features = {
            "ascendant_degree": ascendant,
            "ascendant_sign": asc_sign,
            "ascendant_sign_number": self.sign_numbers.get(asc_sign, 1),
            "ascendant_nakshatra": asc_nakshatra,
            "ascendant_pada": asc_pada,
            "ascendant_lord": self.get_sign_lord(asc_sign)
        }
        
        # Planet features with detailed information
        planet_features = {}
        for planet, position in planet_positions.items():
            sign = get_zodiac_sign(position)
            nakshatra, pada = get_nakshatra(position)
            house = next((h for h, planets in houses.items() if planet in planets), 1)
            
            planet_features[f"{planet.lower()}_longitude"] = position
            planet_features[f"{planet.lower()}_sign"] = sign
            planet_features[f"{planet.lower()}_sign_number"] = self.sign_numbers.get(sign, 1)
            planet_features[f"{planet.lower()}_house"] = house
            planet_features[f"{planet.lower()}_nakshatra"] = nakshatra
            planet_features[f"{planet.lower()}_pada"] = pada
            planet_features[f"{planet.lower()}_degree_in_sign"] = position % 30
            
            if planet in strengths:
                planet_features[f"{planet.lower()}_dignity"] = strengths[planet]["dignity"]
                planet_features[f"{planet.lower()}_is_combust"] = strengths[planet]["is_combust"]
                planet_features[f"{planet.lower()}_is_retrograde"] = strengths[planet]["is_retrograde"]
        
        # House features
        house_features = {}
        for house_num in range(1, 13):
            planets_in_house = houses.get(house_num, [])
            house_sign = self.get_house_sign(house_num, ascendant)
            
            house_features[f"house_{house_num}_sign"] = house_sign
            house_features[f"house_{house_num}_sign_number"] = self.sign_numbers.get(house_sign, 1)
            house_features[f"house_{house_num}_planets"] = planets_in_house
            house_features[f"house_{house_num}_planet_count"] = len(planets_in_house)
            house_features[f"house_{house_num}_is_empty"] = len(planets_in_house) == 0
            house_features[f"house_{house_num}_lord"] = self.get_sign_lord(house_sign)
        
        # Aspect features (flattened for ML)
        aspect_features = {}
        for planet, planet_aspects in aspects.items():
            aspect_features[f"{planet.lower()}_aspect_count"] = len(planet_aspects)
            for i, aspect in enumerate(planet_aspects):
                if i < 5:  # Limit to top 5 aspects per planet
                    prefix = f"{planet.lower()}_aspect_{i+1}"
                    aspect_features[f"{prefix}_planet"] = aspect["aspected_planet"]
                    aspect_features[f"{prefix}_type"] = aspect["aspect_type"]
                    aspect_features[f"{prefix}_strength"] = aspect["strength"]
        
        # Yoga features
        yoga_features = {
            "total_yogas": len(yogas),
            "benefic_yogas": sum(1 for y in yogas if y["benefic"]),
            "malefic_yogas": sum(1 for y in yogas if not y["benefic"])
        }
        
        # Special combinations
        special_features = {
            "moon_sign": get_zodiac_sign(planet_positions["Moon"]),
            "sun_sign": get_zodiac_sign(planet_positions["Sun"]),
            "ruling_planet": get_ruling_planet(get_zodiac_sign(planet_positions["Moon"])),
            "chart_pattern": self.identify_chart_pattern(planet_positions, houses),
            "dominant_element": self.get_dominant_element(planet_positions),
            "dominant_quality": self.get_dominant_quality(planet_positions),
            "hemisphere_emphasis": self.get_hemisphere_emphasis(planet_positions)
        }
        
        return {
            "birth_details": birth_features,
            "ascendant": ascendant_features,
            "planets": planet_features,
            "houses": house_features,
            "aspects": aspect_features,
            "yogas": yoga_features,
            "special_features": special_features,
            "raw_aspects": aspects,
            "raw_strengths": strengths,
            "raw_yogas": yogas
        }

    def get_sign_lord(self, sign: str) -> str:
        """Get the ruling planet of a sign."""
        sign_lords = {
            "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
            "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
            "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
            "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
        }
        return sign_lords.get(sign, "Unknown")

    def get_house_sign(self, house_number: int, ascendant: float) -> str:
        """Calculate the sign of a house in Whole Sign system."""
        asc_sign_num = int(ascendant / 30) + 1
        house_sign_num = ((asc_sign_num - 1 + house_number - 1) % 12) + 1
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return signs[house_sign_num - 1]

    def identify_chart_pattern(self, planet_positions: Dict[str, float], 
                              houses: Dict[int, List[str]]) -> str:
        """Identify overall chart pattern."""
        occupied_houses = [h for h, planets in houses.items() if planets]
        
        if len(occupied_houses) <= 4:
            return "Stellium"
        elif len(occupied_houses) >= 10:
            return "Scattered"
        else:
            return "Balanced"

    def get_dominant_element(self, planet_positions: Dict[str, float]) -> str:
        """Get the dominant element in the chart."""
        elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
        element_signs = {
            "Fire": ["Aries", "Leo", "Sagittarius"],
            "Earth": ["Taurus", "Virgo", "Capricorn"],
            "Air": ["Gemini", "Libra", "Aquarius"],
            "Water": ["Cancer", "Scorpio", "Pisces"]
        }
        
        for position in planet_positions.values():
            sign = get_zodiac_sign(position)
            for element, signs in element_signs.items():
                if sign in signs:
                    elements[element] += 1
                    break
        
        return max(elements, key=elements.get)

    def get_dominant_quality(self, planet_positions: Dict[str, float]) -> str:
        """Get the dominant quality (Cardinal, Fixed, Mutable) in the chart."""
        qualities = {"Cardinal": 0, "Fixed": 0, "Mutable": 0}
        quality_signs = {
            "Cardinal": ["Aries", "Cancer", "Libra", "Capricorn"],
            "Fixed": ["Taurus", "Leo", "Scorpio", "Aquarius"],
            "Mutable": ["Gemini", "Virgo", "Sagittarius", "Pisces"]
        }
        
        for position in planet_positions.values():
            sign = get_zodiac_sign(position)
            for quality, signs in quality_signs.items():
                if sign in signs:
                    qualities[quality] += 1
                    break
        
        return max(qualities, key=qualities.get)

    def get_hemisphere_emphasis(self, planet_positions: Dict[str, float]) -> Dict[str, int]:
        """Get hemisphere emphasis (Eastern/Western, Northern/Southern)."""
        eastern = 0  # Houses 10, 11, 12, 1, 2, 3
        western = 0  # Houses 4, 5, 6, 7, 8, 9
        northern = 0  # Houses 7, 8, 9, 10, 11, 12
        southern = 0  # Houses 1, 2, 3, 4, 5, 6
        
        for position in planet_positions.values():
            house = int(position / 30) + 1  # Simplified house calculation
            
            if house in [10, 11, 12, 1, 2, 3]:
                eastern += 1
            else:
                western += 1
                
            if house in [7, 8, 9, 10, 11, 12]:
                northern += 1
            else:
                southern += 1
        
        return {
            "eastern": eastern,
            "western": western,
            "northern": northern,
            "southern": southern
        }
