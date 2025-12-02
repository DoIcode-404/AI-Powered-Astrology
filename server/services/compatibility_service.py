"""
Compatibility Analysis Service
Calculates relationship compatibility between two birth charts using Vedic astrology.

Methods:
- Planetary Overlays (5 metrics)
- House Overlays (4 metrics)
- Aspect Analysis (3 metrics)
- D9 (Navamsha) Compatibility (2 metrics)
- Guna Matching (8-point traditional system)

Relationship Types: Romantic, Business, Friendship, Family
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Zodiac element mapping
ELEMENT_MAP = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water",
}

# Planet ruling planets mapping
RULING_PLANETS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Exaltation and debilitation signs
EXALTED_SIGNS = {
    "Sun": "Aries", "Moon": "Taurus", "Mercury": "Virgo",
    "Venus": "Pisces", "Mars": "Capricorn", "Jupiter": "Cancer",
    "Saturn": "Libra", "Rahu": "Gemini", "Ketu": "Sagittarius"
}

DEBILITATED_SIGNS = {
    "Sun": "Libra", "Moon": "Scorpio", "Mercury": "Pisces",
    "Venus": "Virgo", "Mars": "Cancer", "Jupiter": "Capricorn",
    "Saturn": "Aries", "Rahu": "Sagittarius", "Ketu": "Gemini"
}


@dataclass
class OverlayScore:
    """Individual overlay analysis"""
    planet: str
    person_a_sign: str
    person_a_house: int
    person_b_sign: str
    person_b_house: int
    score: float
    description: str


@dataclass
class AspectScore:
    """Cross-chart aspect analysis"""
    planet_a: str
    planet_b: str
    aspect_type: str  # Conjunction, Sextile, Trine, Square, Opposition
    orb: float
    score: float
    description: str


class CompatibilityCalculator:
    """Comprehensive compatibility analysis between two birth charts"""

    def __init__(self, chart_a: Dict[str, Any], chart_b: Dict[str, Any],
                 relationship_type: str = "romantic"):
        """
        Initialize compatibility calculator with two birth charts.

        Args:
            chart_a: Person A's kundali/birth chart
            chart_b: Person B's kundali/birth chart
            relationship_type: "romantic", "business", "friendship", "family"
        """
        self.chart_a = chart_a
        self.chart_b = chart_b
        self.relationship_type = relationship_type
        self.validation_errors = []

    def validate_charts(self) -> bool:
        """Validate both charts have required fields"""
        required_fields = ["planets", "ascendant", "houses"]

        for field in required_fields:
            if field not in self.chart_a:
                self.validation_errors.append(f"Chart A missing: {field}")
            if field not in self.chart_b:
                self.validation_errors.append(f"Chart B missing: {field}")

        return len(self.validation_errors) == 0

    # ========== METRIC 1: PLANETARY OVERLAYS ==========

    def calculate_overlay_scores(self) -> tuple[List[OverlayScore], float]:
        """
        Calculate personal planet overlays.
        Person A's planets in Person B's houses.

        Returns: (overlay_list, total_score)
        """
        overlays = []
        total_score = 0
        personal_planets = ["Sun", "Moon", "Venus", "Mars"]

        for planet_a in personal_planets:
            if planet_a not in self.chart_a["planets"]:
                continue

            planet_a_data = self.chart_a["planets"][planet_a]
            planet_a_sign = planet_a_data.get("sign", "")

            # Get Person B's house positions
            person_b_houses = self.chart_b.get("houses", {})

            # Determine which house this planet falls into in Person B's chart
            overlay_house = self._find_planet_house(
                planet_a_data.get("longitude", 0),
                person_b_houses
            )

            # Calculate overlay score based on house
            score = self._score_overlay_by_house(planet_a, overlay_house)

            # Check for conjunction (0-10° orb)
            person_b_ruler = RULING_PLANETS.get(self.chart_b["ascendant"]["sign"], "")
            if person_b_ruler in self.chart_b["planets"]:
                person_b_ruler_lon = self.chart_b["planets"][person_b_ruler].get("longitude", 0)
                orb = abs(planet_a_data.get("longitude", 0) - person_b_ruler_lon)
                if orb < 10 or orb > 350:  # Conjunction
                    score *= 1.5

            overlay = OverlayScore(
                planet=planet_a,
                person_a_sign=planet_a_sign,
                person_a_house=0,  # Not used here
                person_b_sign=self.chart_b["ascendant"]["sign"],
                person_b_house=overlay_house,
                score=score,
                description=self._describe_overlay(planet_a, overlay_house)
            )
            overlays.append(overlay)
            total_score += score

        # Add malefic penalty
        malefic_penalty = self._calculate_malefic_overlay_penalty()
        total_score -= malefic_penalty

        return overlays, max(0, total_score)

    def _score_overlay_by_house(self, planet: str, house: int) -> float:
        """Score overlay based on house position"""
        base_scores = {
            1: 15,   # Identity/Lagna
            5: 20,   # Romance (Venus/Mars)
            7: 25,   # Marriage house (Venus) / 18 (Mars)
            8: 15,   # Intimacy
            11: 10,  # Friendship
        }

        # Adjust for planet type
        if planet in ["Venus", "Mars"] and house == 7:
            return 25 if planet == "Venus" else 18

        return base_scores.get(house, 5)

    def _calculate_malefic_overlay_penalty(self) -> float:
        """Penalty for Mars/Saturn in unfavorable houses"""
        penalty = 0
        malefic_planets = ["Mars", "Saturn"]

        for planet in malefic_planets:
            if planet not in self.chart_a["planets"]:
                continue

            planet_lon = self.chart_a["planets"][planet].get("longitude", 0)
            overlay_house = self._find_planet_house(
                planet_lon,
                self.chart_b.get("houses", {})
            )

            if planet == "Mars" and overlay_house in [1, 7, 8]:
                penalty += 15
            elif planet == "Saturn" and overlay_house == 7:
                penalty += 10

        return penalty

    # ========== METRIC 2: HOUSE OVERLAYS ==========

    def calculate_house_overlay_scores(self) -> float:
        """
        Calculate house overlay compatibility.
        Compares Venus/Mars signs between charts.
        """
        score = 0

        # Venus sign comparison
        if "Venus" in self.chart_a["planets"] and "Moon" in self.chart_b["planets"]:
            venus_a_sign = self.chart_a["planets"]["Venus"].get("sign", "")
            sun_b_sign = self.chart_b["planets"]["Sun"].get("sign", "")

            score += self._score_sign_compatibility(venus_a_sign, sun_b_sign)

        # Mars sign comparison
        if "Mars" in self.chart_a["planets"] and "Mars" in self.chart_b["planets"]:
            mars_a_sign = self.chart_a["planets"]["Mars"].get("sign", "")
            mars_b_sign = self.chart_b["planets"]["Mars"].get("sign", "")

            score += self._score_sign_compatibility(mars_a_sign, mars_b_sign) * 0.6

        # Moon sign compatibility (emotional)
        if "Moon" in self.chart_a["planets"] and "Moon" in self.chart_b["planets"]:
            moon_a_sign = self.chart_a["planets"]["Moon"].get("sign", "")
            moon_b_sign = self.chart_b["planets"]["Moon"].get("sign", "")

            if moon_a_sign == moon_b_sign:
                score += 20  # Same moon = emotional harmony
            elif self._get_element(moon_a_sign) == self._get_element(moon_b_sign):
                score += 15  # Same element = compatible emotions

        # Ascendant compatibility (physical attraction)
        asc_a_sign = self.chart_a["ascendant"].get("sign", "")
        asc_b_sign = self.chart_b["ascendant"].get("sign", "")

        asc_score = self._score_ascendant_compatibility(asc_a_sign, asc_b_sign)
        score += asc_score

        return min(80, score)  # Cap at 80

    def _score_sign_compatibility(self, sign_a: str, sign_b: str) -> float:
        """Score compatibility between two zodiac signs"""
        element_a = self._get_element(sign_a)
        element_b = self._get_element(sign_b)

        if sign_a == sign_b:
            return 20

        # Same element compatibility
        if element_a == element_b:
            if element_a in ["Fire", "Earth"]:
                return 20
            else:  # Air, Water
                return 18

        # Complementary elements
        complementary = [("Fire", "Air"), ("Earth", "Water")]
        if (element_a, element_b) in complementary or (element_b, element_a) in complementary:
            return 15

        # Less compatible but workable
        if (element_a in ["Fire", "Earth"] and element_b in ["Fire", "Earth"]) or \
           (element_a in ["Air", "Water"] and element_b in ["Air", "Water"]):
            return 8

        return 5  # Challenging

    def _score_ascendant_compatibility(self, asc_a: str, asc_b: str) -> float:
        """Score physical attraction based on ascendant"""
        if asc_a == asc_b:
            return 15

        # Calculate degree difference
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        try:
            idx_a = signs.index(asc_a)
            idx_b = signs.index(asc_b)
            diff = min(abs(idx_a - idx_b), 12 - abs(idx_a - idx_b))

            if diff == 3:  # Trine (120°)
                return 12
            elif diff == 2:  # Sextile (60°)
                return 10
            elif diff == 6:  # Opposition (180°)
                return -8
            elif diff == 3:  # Square (90°)
                return -5
        except ValueError:
            pass

        return 5

    # ========== METRIC 3: ASPECT ANALYSIS ==========

    def calculate_aspect_scores(self) -> tuple[List[AspectScore], float]:
        """
        Calculate cross-chart aspects.
        Person A's planets aspecting Person B's planets.
        """
        aspects = []
        total_score = 0

        planets_to_check = ["Sun", "Moon", "Venus", "Mars", "Jupiter"]
        major_aspects = {
            0: ("Conjunction", 10),
            60: ("Sextile", 8),
            120: ("Trine", 12),
            90: ("Square", -5),
            180: ("Opposition", -3),
        }

        for planet_a in planets_to_check:
            if planet_a not in self.chart_a["planets"]:
                continue

            lon_a = self.chart_a["planets"][planet_a].get("longitude", 0)

            for planet_b in planets_to_check:
                if planet_b not in self.chart_b["planets"]:
                    continue

                lon_b = self.chart_b["planets"][planet_b].get("longitude", 0)

                # Calculate aspect
                diff = abs(lon_a - lon_b)
                if diff > 180:
                    diff = 360 - diff

                # Check for aspects
                for aspect_deg, (aspect_name, base_score) in major_aspects.items():
                    orb = 8  # Standard orb

                    if abs(diff - aspect_deg) <= orb:
                        actual_orb = abs(diff - aspect_deg)
                        score = base_score * (1 - actual_orb / orb)

                        aspect = AspectScore(
                            planet_a=planet_a,
                            planet_b=planet_b,
                            aspect_type=aspect_name,
                            orb=actual_orb,
                            score=score,
                            description=f"{planet_a} {aspect_name} {planet_b}"
                        )
                        aspects.append(aspect)
                        total_score += score
                        break

        return aspects, max(0, total_score)

    # ========== METRIC 4: D9 (NAVAMSHA) COMPATIBILITY ==========

    def calculate_d9_compatibility(self) -> float:
        """
        Calculate D9 (Navamsha) compatibility.
        Vedic indicator of marriage potential and hidden nature.
        """
        score = 0

        # Get D9 charts (simplified - using planet positions in D9)
        if "divisional_charts" not in self.chart_a or "divisional_charts" not in self.chart_b:
            return 0

        # D9 Venus sign comparison (most important)
        d9_a = self.chart_a.get("divisional_charts", {}).get("D9", {})
        d9_b = self.chart_b.get("divisional_charts", {}).get("D9", {})

        if d9_a and d9_b:
            if "Venus" in d9_a.get("planets", {}) and "Venus" in d9_b.get("planets", {}):
                venus_a_sign = d9_a["planets"]["Venus"].get("sign", "")
                venus_b_sign = d9_b["planets"]["Venus"].get("sign", "")

                if venus_a_sign == venus_b_sign:
                    score += 20
                elif self._get_element(venus_a_sign) == self._get_element(venus_b_sign):
                    score += 15
                else:
                    score += 8

        # D9 7th house lord comparison
        if "houses" in d9_a and "houses" in d9_b:
            score += 15  # Simplified for now

        return min(60, score)

    # ========== METRIC 5: GUNA MATCHING ==========

    def calculate_guna_matching(self) -> Dict[str, Any]:
        """
        Traditional 8-point Guna matching system.
        Returns individual guna scores and compatibility interpretation.
        """
        gunas = {
            "Varna": self._calculate_varna(),      # 1 point
            "Vasya": self._calculate_vasya(),      # 2 points
            "Tara": self._calculate_tara(),        # 3 points
            "Yoni": self._calculate_yoni(),        # 4 points
            "Graha Maitri": self._calculate_graha_maitri(),  # 5 points
            "Gana": self._calculate_gana(),        # 6 points
            "Bhakoot": self._calculate_bhakoot(),  # 7 points
            "Nadi": self._calculate_nadi(),        # 8 points
        }

        total_score = sum(gunas.values())

        # Convert to percentage of max 36
        compatibility_percentage = (total_score / 36) * 100

        return {
            "individual_scores": gunas,
            "total_score": total_score,
            "max_score": 36,
            "compatibility_percentage": compatibility_percentage,
            "rating": self._rate_guna_compatibility(total_score)
        }

    def _calculate_varna(self) -> int:
        """Nature harmony - 1 point max"""
        moon_a_sign = self.chart_a["planets"].get("Moon", {}).get("sign", "")
        moon_b_sign = self.chart_b["planets"].get("Moon", {}).get("sign", "")

        varnas = {
            "Fire": "Brahmana",
            "Earth": "Vaishya",
            "Air": "Kshatriya",
            "Water": "Shudra"
        }

        varna_a = varnas.get(ELEMENT_MAP.get(moon_a_sign, ""), "")
        varna_b = varnas.get(ELEMENT_MAP.get(moon_b_sign, ""), "")

        if varna_a == varna_b:
            return 1
        return 0

    def _calculate_vasya(self) -> int:
        """Physical/sexual attraction - 2 points max"""
        score = 0
        moon_a_sign = self.chart_a["planets"].get("Moon", {}).get("sign", "")
        moon_b_sign = self.chart_b["planets"].get("Moon", {}).get("sign", "")

        # Vasya compatibility based on zodiac
        if ELEMENT_MAP.get(moon_a_sign) == ELEMENT_MAP.get(moon_b_sign):
            score = 2
        elif {ELEMENT_MAP.get(moon_a_sign), ELEMENT_MAP.get(moon_b_sign)} in [
            {"Fire", "Air"}, {"Earth", "Water"}
        ]:
            score = 1

        return score

    def _calculate_tara(self) -> int:
        """Longevity together - 3 points max"""
        # Simplified calculation based on nakshatra
        score = 0

        moon_a_nak = self.chart_a.get("ascendant", {}).get("nakshatra", "")
        moon_b_nak = self.chart_b.get("ascendant", {}).get("nakshatra", "")

        if moon_a_nak and moon_b_nak:
            score = min(3, 3)  # Simplified

        return score

    def _calculate_yoni(self) -> int:
        """Sexual compatibility - 4 points max"""
        # Based on nakshatra animal symbols
        score = 0

        moon_a_nak = self.chart_a.get("ascendant", {}).get("nakshatra", "")
        moon_b_nak = self.chart_b.get("ascendant", {}).get("nakshatra", "")

        # Yoni compatibility matrix (simplified)
        if moon_a_nak and moon_b_nak:
            if moon_a_nak == moon_b_nak:
                score = 4
            else:
                score = 2

        return score

    def _calculate_graha_maitri(self) -> int:
        """Mental/intellectual compatibility - 5 points max"""
        score = 0

        mercury_a = self.chart_a["planets"].get("Mercury", {})
        mercury_b = self.chart_b["planets"].get("Mercury", {})

        if mercury_a and mercury_b:
            merc_a_sign = mercury_a.get("sign", "")
            merc_b_sign = mercury_b.get("sign", "")

            if ELEMENT_MAP.get(merc_a_sign) == ELEMENT_MAP.get(merc_b_sign):
                score = 5
            else:
                score = 2

        return score

    def _calculate_gana(self) -> int:
        """Temperament compatibility - 6 points max"""
        # Deva, Manushya, Rakshasa ganas based on nakshatras
        score = 0

        # Simplified calculation
        moon_a_nak = self.chart_a.get("ascendant", {}).get("nakshatra", "")
        moon_b_nak = self.chart_b.get("ascendant", {}).get("nakshatra", "")

        if moon_a_nak == moon_b_nak:
            score = 6
        elif moon_a_nak and moon_b_nak:
            score = 3

        return score

    def _calculate_bhakoot(self) -> int:
        """Emotional compatibility - 7 points max"""
        score = 0

        moon_a_sign_idx = self._get_sign_index(
            self.chart_a["planets"].get("Moon", {}).get("sign", "")
        )
        moon_b_sign_idx = self._get_sign_index(
            self.chart_b["planets"].get("Moon", {}).get("sign", "")
        )

        if moon_a_sign_idx >= 0 and moon_b_sign_idx >= 0:
            diff = abs(moon_a_sign_idx - moon_b_sign_idx)
            if diff in [0, 5, 9]:
                score = 7
            elif diff in [1, 4, 8, 11]:
                score = 6
            elif diff == 6:
                score = 0  # Unfavorable
            else:
                score = 4

        return score

    def _calculate_nadi(self) -> int:
        """Health/genetics compatibility - 8 points max"""
        score = 0

        # Nadi based on nakshatra pada
        nadi_a = self._get_nakshatra_nadi(
            self.chart_a.get("ascendant", {}).get("nakshatra", "")
        )
        nadi_b = self._get_nakshatra_nadi(
            self.chart_b.get("ascendant", {}).get("nakshatra", "")
        )

        if nadi_a == nadi_b:
            score = 8
        elif nadi_a and nadi_b:
            score = 0  # Same nadi = genetic incompatibility

        return score

    def _rate_guna_compatibility(self, total_score: int) -> str:
        """Rating based on total guna score"""
        if total_score >= 30:
            return "Perfect"
        elif total_score >= 24:
            return "Excellent"
        elif total_score >= 18:
            return "Very Good"
        elif total_score >= 14:
            return "Good"
        elif total_score >= 10:
            return "Average"
        else:
            return "Poor"

    # ========== HELPER METHODS ==========

    def _get_element(self, sign: str) -> str:
        """Get element of zodiac sign"""
        return ELEMENT_MAP.get(sign, "")

    def _get_sign_index(self, sign: str) -> int:
        """Get numerical index of zodiac sign"""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        try:
            return signs.index(sign)
        except ValueError:
            return -1

    def _get_nakshatra_nadi(self, nakshatra: str) -> Optional[str]:
        """Get Nadi (Vata, Pitta, Kapha) from nakshatra"""
        # Simplified mapping
        vata_nakshatras = ["Ashwini", "Ardra", "Punarvasu", "Shatabhisha", "Dhanishta", "Shatvisha"]
        pitta_nakshatras = ["Krittika", "Rohini", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitta", "Swati", "Vishakha", "Jyeshtha", "Mula", "Purva Ashadha"]
        kapha_nakshatras = ["Mrigashirsha", "Pushya", "Ashlesha", "Pushya", "Uttara Ashadha", "Revati", "Bharani"]

        if nakshatra in vata_nakshatras:
            return "Vata"
        elif nakshatra in pitta_nakshatras:
            return "Pitta"
        elif nakshatra in kapha_nakshatras:
            return "Kapha"
        return None

    def _find_planet_house(self, longitude: float, houses: Dict) -> int:
        """Find which house a planet falls into"""
        # Simplified - assumes houses dict has house cusps
        # In real implementation, compare with house cusps
        return 7  # Default for now

    def _describe_overlay(self, planet: str, house: int) -> str:
        """Generate description of overlay"""
        house_meanings = {
            1: "Identity and self",
            5: "Romance and creativity",
            7: "Marriage and partnership",
            8: "Intimacy and secrets",
            11: "Friendship and support"
        }

        return f"{planet} in {house_meanings.get(house, f'house {house}')}"

    # ========== FINAL COMPATIBILITY SCORE ==========

    def calculate_final_compatibility(self) -> Dict[str, Any]:
        """
        Calculate final compatibility score using all metrics.
        Returns comprehensive compatibility analysis.
        """
        if not self.validate_charts():
            return {
                "error": "Invalid charts",
                "validation_errors": self.validation_errors
            }

        # Calculate all metrics
        overlays, overlay_score = self.calculate_overlay_scores()
        house_score = self.calculate_house_overlay_scores()
        aspects, aspect_score = self.calculate_aspect_scores()
        d9_score = self.calculate_d9_compatibility()
        guna_data = self.calculate_guna_matching()

        # Weighted formula
        weights = {
            "overlay": 0.30,
            "house": 0.25,
            "aspect": 0.20,
            "d9": 0.15,
            "guna": 0.10,
        }

        # Normalize scores to 0-100 range
        normalized_overlay = min(100, overlay_score)
        normalized_house = min(100, house_score)
        normalized_aspect = min(100, max(0, aspect_score + 50))  # Offset to 0-100
        normalized_d9 = min(100, d9_score)
        normalized_guna = guna_data["compatibility_percentage"]

        # Calculate weighted final score
        final_score = (
            weights["overlay"] * normalized_overlay +
            weights["house"] * normalized_house +
            weights["aspect"] * normalized_aspect +
            weights["d9"] * normalized_d9 +
            weights["guna"] * normalized_guna
        )

        # Apply relationship-type adjustments
        final_score = self._apply_relationship_adjustments(final_score)

        # Determine rating
        rating = self._rate_compatibility(final_score)

        return {
            "compatibility_percentage": min(100, max(0, final_score)),
            "compatibility_rating": rating,
            "overlay_score": normalized_overlay,
            "house_score": normalized_house,
            "aspect_score": normalized_aspect,
            "d9_score": normalized_d9,
            "guna_score": normalized_guna,
            "component_scores": {
                "overlay": overlay_score,
                "house": house_score,
                "aspect": aspect_score,
                "d9": d9_score,
                "guna": guna_data
            },
            "overlay_analysis": overlays,
            "aspect_analysis": aspects,
            "created_at": datetime.utcnow()
        }

    def _apply_relationship_adjustments(self, score: float) -> float:
        """Apply relationship-type specific multipliers"""
        multipliers = {
            "romantic": {"overlay": 1.2, "d9": 1.2},
            "business": {"house": 1.3, "aspect": 1.2},
            "friendship": {"house": 1.2},
            "family": {"house": 1.2, "d9": 1.0},
        }

        adjustments = multipliers.get(self.relationship_type, {})

        # Simple adjustment (can be more sophisticated)
        if self.relationship_type == "romantic":
            score *= 1.1
        elif self.relationship_type == "business":
            score *= 1.05

        return score

    def _rate_compatibility(self, score: float) -> str:
        """Rate compatibility based on score"""
        if score >= 85:
            return "Perfect"
        elif score >= 75:
            return "Excellent"
        elif score >= 65:
            return "Very Good"
        elif score >= 50:
            return "Good"
        elif score >= 35:
            return "Average"
        elif score >= 20:
            return "Poor"
        else:
            return "Very Poor"
