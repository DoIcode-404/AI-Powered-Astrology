"""
Feature Extractor for ML Model Predictions
Extracts the exact 53 features needed for the trained XGBoost model
from a complete Kundali response.
"""

import logging
from typing import Dict, List, Any, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class KundaliFeatureExtractor:
    """
    Extract 53 features from Kundali response for ML model predictions.

    Features (53 total):
    - Planetary positions (10): sun_degree through ascendant_degree
    - House placements (24): For each house 1-12: planet_count + lord_strength
    - Planetary strengths (9): sun_strength through ketu_strength
    - Yoga counts (4): total_yoga_count, benefic_yoga_count, malefic_yoga_count, neutral_yoga_count
    - Aspect strengths (6): aspect_strength_1 through aspect_strength_6
    """

    def __init__(self):
        self.required_features = [
            # Planetary positions (10)
            'sun_degree', 'moon_degree', 'mercury_degree', 'venus_degree', 'mars_degree',
            'jupiter_degree', 'saturn_degree', 'rahu_degree', 'ketu_degree', 'ascendant_degree',
            # House placements (24)
            'house_1_planets', 'house_1_lord_strength',
            'house_2_planets', 'house_2_lord_strength',
            'house_3_planets', 'house_3_lord_strength',
            'house_4_planets', 'house_4_lord_strength',
            'house_5_planets', 'house_5_lord_strength',
            'house_6_planets', 'house_6_lord_strength',
            'house_7_planets', 'house_7_lord_strength',
            'house_8_planets', 'house_8_lord_strength',
            'house_9_planets', 'house_9_lord_strength',
            'house_10_planets', 'house_10_lord_strength',
            'house_11_planets', 'house_11_lord_strength',
            'house_12_planets', 'house_12_lord_strength',
            # Planetary strengths (9)
            'sun_strength', 'moon_strength', 'mercury_strength', 'venus_strength',
            'mars_strength', 'jupiter_strength', 'saturn_strength', 'rahu_strength',
            'ketu_strength',
            # Yoga counts (4)
            'total_yoga_count', 'benefic_yoga_count', 'malefic_yoga_count', 'neutral_yoga_count',
            # Aspect strengths (6)
            'aspect_strength_1', 'aspect_strength_2', 'aspect_strength_3',
            'aspect_strength_4', 'aspect_strength_5', 'aspect_strength_6'
        ]

    def extract_features(self, kundali_response: Dict[str, Any]) -> Tuple[Dict[str, float], List[str]]:
        """
        Extract 53 features from Kundali response.

        Args:
            kundali_response: Complete Kundali response from backend API

        Returns:
            Tuple of (features_dict, missing_features_list)
        """
        features = {}
        missing_features = []

        try:
            # 1. Extract planetary positions (10)
            logger.info("Extracting planetary positions...")
            planets_data = kundali_response.get('planets', {})

            planet_mapping = {
                'Sun': 'sun_degree',
                'Moon': 'moon_degree',
                'Mercury': 'mercury_degree',
                'Venus': 'venus_degree',
                'Mars': 'mars_degree',
                'Jupiter': 'jupiter_degree',
                'Saturn': 'saturn_degree',
                'Rahu': 'rahu_degree',
                'Ketu': 'ketu_degree',
            }

            for planet, feature_name in planet_mapping.items():
                try:
                    degree = planets_data.get(planet, {}).get('longitude', 0)
                    # Normalize to 0-360
                    degree = degree % 360
                    features[feature_name] = float(degree)
                except Exception as e:
                    logger.warning(f"Could not extract {planet} position: {str(e)}")
                    features[feature_name] = 0.0
                    missing_features.append(feature_name)

            # Ascendant
            try:
                asc_degree = kundali_response.get('ascendant', {}).get('longitude', 0)
                features['ascendant_degree'] = float(asc_degree % 360)
            except Exception as e:
                logger.warning(f"Could not extract ascendant degree: {str(e)}")
                features['ascendant_degree'] = 0.0
                missing_features.append('ascendant_degree')

            # 2. Extract house placements (24)
            logger.info("Extracting house placements...")
            houses_data = kundali_response.get('houses', {})

            for house_num in range(1, 13):
                house_key = str(house_num)
                house_info = houses_data.get(house_key, {})

                try:
                    # Planet count in house
                    planets_in_house = house_info.get('planets', [])
                    planet_count = len(planets_in_house) if isinstance(planets_in_house, list) else 0
                    features[f'house_{house_num}_planets'] = float(planet_count)
                except Exception as e:
                    logger.warning(f"Could not extract planets in house {house_num}: {str(e)}")
                    features[f'house_{house_num}_planets'] = 0.0
                    missing_features.append(f'house_{house_num}_planets')

                try:
                    # House lord strength (from shad_bala or estimate)
                    lord_strength = self._get_house_lord_strength(
                        kundali_response, house_num, house_info
                    )
                    features[f'house_{house_num}_lord_strength'] = float(lord_strength)
                except Exception as e:
                    logger.warning(f"Could not extract lord strength for house {house_num}: {str(e)}")
                    features[f'house_{house_num}_lord_strength'] = 50.0  # Default to neutral
                    missing_features.append(f'house_{house_num}_lord_strength')

            # 3. Extract planetary strengths (9)
            logger.info("Extracting planetary strengths...")
            shad_bala_data = kundali_response.get('shad_bala', {})
            planetary_strengths = shad_bala_data.get('planetary_strengths', {})

            for planet in planet_mapping.keys():
                feature_name = f"{planet.lower()}_strength"
                try:
                    strength = planetary_strengths.get(planet, {}).get('total_strength_percentage', 50)
                    features[feature_name] = float(strength)
                except Exception as e:
                    logger.warning(f"Could not extract {planet} strength: {str(e)}")
                    features[feature_name] = 50.0  # Default to neutral
                    missing_features.append(feature_name)

            # Rahu and Ketu strengths (estimated)
            for planet in ['Rahu', 'Ketu']:
                feature_name = f"{planet.lower()}_strength"
                try:
                    strength = planetary_strengths.get(planet, {}).get('total_strength_percentage', 50)
                    features[feature_name] = float(strength)
                except Exception as e:
                    features[feature_name] = 50.0
                    missing_features.append(feature_name)

            # 4. Extract yoga counts (4)
            logger.info("Extracting yoga information...")
            yogas_data = shad_bala_data.get('yogas', {}) or {}

            try:
                total_yogas = yogas_data.get('total_yoga_count', 0)
                features['total_yoga_count'] = float(total_yogas)
            except Exception as e:
                features['total_yoga_count'] = 0.0
                missing_features.append('total_yoga_count')

            try:
                benefic_yogas = yogas_data.get('benefic_yoga_count', 0)
                features['benefic_yoga_count'] = float(benefic_yogas)
            except Exception as e:
                features['benefic_yoga_count'] = 0.0
                missing_features.append('benefic_yoga_count')

            try:
                malefic_yogas = yogas_data.get('malefic_yoga_count', 0)
                features['malefic_yoga_count'] = float(malefic_yogas)
            except Exception as e:
                features['malefic_yoga_count'] = 0.0
                missing_features.append('malefic_yoga_count')

            try:
                neutral_yogas = yogas_data.get('neutral_yoga_count', 0)
                features['neutral_yoga_count'] = float(neutral_yogas)
            except Exception as e:
                features['neutral_yoga_count'] = 0.0
                missing_features.append('neutral_yoga_count')

            # 5. Extract aspect strengths (6)
            logger.info("Extracting aspect strengths...")
            aspect_strengths = shad_bala_data.get('aspect_strengths', {}) or {}

            # If aspect_strengths is empty, estimate from planetary positions
            if not aspect_strengths:
                aspect_strengths = self._calculate_aspect_strengths(
                    kundali_response.get('planets', {})
                )

            aspect_values = list(aspect_strengths.values())[:6]
            for i in range(1, 7):
                try:
                    if i - 1 < len(aspect_values):
                        strength = aspect_values[i - 1]
                    else:
                        strength = 0.0
                    features[f'aspect_strength_{i}'] = float(strength)
                except Exception as e:
                    features[f'aspect_strength_{i}'] = 0.0
                    missing_features.append(f'aspect_strength_{i}')

            # Validate we have all required features
            logger.info(f"Extracted {len(features)} features")
            if missing_features:
                logger.warning(f"Missing features: {missing_features}")

            return features, missing_features

        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}", exc_info=True)
            raise

    def _get_house_lord_strength(self, kundali_response: Dict, house_num: int,
                                 house_info: Dict) -> float:
        """
        Get house lord strength from shad_bala or estimate from planets in house.
        """
        # Try to get from shad_bala first
        shad_bala = kundali_response.get('shad_bala', {})
        house_strengths = shad_bala.get('house_lord_strengths', {})

        if str(house_num) in house_strengths:
            return house_strengths[str(house_num)].get('strength_percentage', 50)

        # Estimate from planets in house
        planets_in_house = house_info.get('planets', [])
        if planets_in_house:
            planetary_strengths = shad_bala.get('planetary_strengths', {})
            strengths = []
            for planet in planets_in_house:
                strength = planetary_strengths.get(planet, {}).get('total_strength_percentage', 50)
                strengths.append(strength)
            return float(np.mean(strengths)) if strengths else 50.0

        # Default: neutral strength
        return 50.0

    def _calculate_aspect_strengths(self, planets_data: Dict[str, Any]) -> Dict[int, float]:
        """
        Calculate aspect strengths from planetary positions.

        Returns dictionary with aspect strength values (0-100).
        """
        aspect_strengths = {}

        try:
            positions = {}
            for planet, info in planets_data.items():
                if isinstance(info, dict) and 'longitude' in info:
                    positions[planet] = info['longitude']

            if len(positions) < 2:
                return {i: 0.0 for i in range(1, 7)}

            # Calculate pairwise aspects
            planets = list(positions.keys())
            aspect_count = 0

            for i in range(len(planets)):
                for j in range(i + 1, len(planets)):
                    pos1 = positions[planets[i]]
                    pos2 = positions[planets[j]]

                    # Calculate angular distance
                    diff = abs(pos1 - pos2)
                    if diff > 180:
                        diff = 360 - diff

                    # Aspect strength based on distance
                    # Strong aspects: 0 (conjunction), 60, 90, 120, 180 degrees
                    aspect_degrees = [0, 60, 90, 120, 180]
                    orb = 8

                    for aspect_deg in aspect_degrees:
                        if abs(diff - aspect_deg) <= orb:
                            strength = max(0, 100 * (1 - abs(diff - aspect_deg) / orb))
                            aspect_count += 1
                            aspect_strengths[aspect_count] = strength
                            break

            # Pad with zeros if needed
            while len(aspect_strengths) < 6:
                aspect_strengths[len(aspect_strengths) + 1] = 0.0

            return aspect_strengths

        except Exception as e:
            logger.warning(f"Error calculating aspect strengths: {str(e)}")
            return {i: 0.0 for i in range(1, 7)}

    def validate_features(self, features: Dict[str, float]) -> Tuple[bool, List[str]]:
        """
        Validate that all 53 features are present and in valid range.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Check all features present
        for feature_name in self.required_features:
            if feature_name not in features:
                issues.append(f"Missing feature: {feature_name}")
            elif features[feature_name] is None:
                issues.append(f"Feature {feature_name} is None")
            elif np.isnan(features[feature_name]):
                issues.append(f"Feature {feature_name} is NaN")
            elif np.isinf(features[feature_name]):
                issues.append(f"Feature {feature_name} is infinite")

        # Check reasonable ranges
        for feature_name, value in features.items():
            if '_degree' in feature_name:
                if not (0 <= value <= 360):
                    issues.append(f"Degree feature {feature_name} out of range: {value}")
            elif '_strength' in feature_name or '_lord_strength' in feature_name:
                if not (0 <= value <= 100):
                    issues.append(f"Strength feature {feature_name} out of range: {value}")
            elif '_planets' in feature_name or '_yoga_count' in feature_name or 'aspect_strength' in feature_name:
                if value < 0:
                    issues.append(f"Count feature {feature_name} is negative: {value}")

        is_valid = len(issues) == 0
        return is_valid, issues