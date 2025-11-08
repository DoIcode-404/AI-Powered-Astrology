"""
Yogas Detection System
Identifies auspicious and inauspicious yoga combinations in Vedic astrology.

Yogas are specific planetary combinations that have special significance.
They can be highly beneficial (Raja Yoga) or challenging (Papa Yoga).

Author: Astrology Backend
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class YogaDetector:
    """
    Detect and analyze Vedic astrology yogas.

    Major Yogas:
    - Raj Yoga: Power, authority, success
    - Parivartana Yoga: Mutual planetary exchange
    - Neecha Bhanga Yoga: Debilitation cancellation
    - Gaj Kesari Yoga: Jupiter-Moon wisdom
    - Chandra Mangal Yoga: Emotional strength
    - Dhana Yoga: Wealth
    - Bhagya Yoga: Fortune and luck
    """

    def __init__(self, planets_info: Dict[str, Dict], ascendant_sign: str, moon_sign: str):
        """
        Initialize Yoga Detector.

        Args:
            planets_info: Dictionary with all planet details
            ascendant_sign: Ascendant zodiac sign
            moon_sign: Moon zodiac sign
        """
        self.planets_info = planets_info
        self.ascendant_sign = ascendant_sign
        self.moon_sign = moon_sign

        # Sign to number mapping
        self.sign_to_number = {
            'Aries': 1, 'Taurus': 2, 'Gemini': 3, 'Cancer': 4,
            'Leo': 5, 'Virgo': 6, 'Libra': 7, 'Scorpio': 8,
            'Sagittarius': 9, 'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12
        }

        # Exalted positions for each planet
        self.exalted_signs = {
            'Sun': 'Aries',
            'Moon': 'Taurus',
            'Mercury': 'Virgo',
            'Venus': 'Pisces',
            'Mars': 'Capricorn',
            'Jupiter': 'Cancer',
            'Saturn': 'Libra',
            'Rahu': 'Gemini',
            'Ketu': 'Sagittarius'
        }

        # Own signs for each planet
        self.own_signs = {
            'Sun': ['Leo'],
            'Moon': ['Cancer'],
            'Mercury': ['Gemini', 'Virgo'],
            'Venus': ['Taurus', 'Libra'],
            'Mars': ['Aries', 'Scorpio'],
            'Jupiter': ['Sagittarius', 'Pisces'],
            'Saturn': ['Capricorn', 'Aquarius'],
            'Rahu': ['Aquarius'],
            'Ketu': ['Scorpio']
        }

        # Debilitated signs
        self.debilitated_signs = {
            'Sun': 'Libra',
            'Moon': 'Scorpio',
            'Mercury': 'Pisces',
            'Venus': 'Virgo',
            'Mars': 'Cancer',
            'Jupiter': 'Capricorn',
            'Saturn': 'Aries',
            'Rahu': 'Sagittarius',
            'Ketu': 'Gemini'
        }

    def detect_all_yogas(self) -> Dict[str, List[Dict]]:
        """
        Detect all yogas present in the birth chart.

        Returns:
            Dictionary with benefic and malefic yogas
        """
        return {
            'benefic_yogas': self._detect_benefic_yogas(),
            'malefic_yogas': self._detect_malefic_yogas(),
            'yoga_summary': self._generate_yoga_summary()
        }

    def _detect_benefic_yogas(self) -> List[Dict]:
        """Detect beneficial yogas."""
        benefic = []

        # Raj Yoga
        raj_yogas = self._detect_raj_yoga()
        benefic.extend(raj_yogas)

        # Parivartana Yoga
        parivartana = self._detect_parivartana_yoga()
        benefic.extend(parivartana)

        # Neecha Bhanga Yoga
        neecha_bhanga = self._detect_neecha_bhanga_yoga()
        benefic.extend(neecha_bhanga)

        # Gaj Kesari Yoga
        gaj_kesari = self._detect_gaj_kesari_yoga()
        if gaj_kesari:
            benefic.append(gaj_kesari)

        # Chandra Mangal Yoga
        chandra_mangal = self._detect_chandra_mangal_yoga()
        if chandra_mangal:
            benefic.append(chandra_mangal)

        # Dhana Yoga
        dhana = self._detect_dhana_yoga()
        if dhana:
            benefic.append(dhana)

        # Bhagya Yoga
        bhagya = self._detect_bhagya_yoga()
        if bhagya:
            benefic.append(bhagya)

        return benefic

    def _detect_malefic_yogas(self) -> List[Dict]:
        """Detect challenging/malefic yogas."""
        malefic = []

        # Papa Yoga detection
        papa = self._detect_papa_yoga()
        if papa:
            malefic.append(papa)

        return malefic

    def _detect_raj_yoga(self) -> List[Dict]:
        """
        Detect Raj Yoga - combinations for power and authority.

        Occurs when:
        - 9th and 10th house lords are strong and in mutual aspect
        - Planets in 10th from Moon sign
        - 5th and 9th lords in mutual aspect
        """
        raj_yogas = []

        try:
            # Check if Jupiter or Venus aspects strong planets
            for planet in ['Jupiter', 'Venus', 'Mercury']:
                if planet in self.planets_info:
                    strength = self.planets_info[planet].get('strength', 'moderate')
                    if strength in ['strong', 'very strong']:
                        raj_yogas.append({
                            'name': 'Raj Yoga',
                            'planet': planet,
                            'description': f'{planet} is in strong position, indicating power and authority',
                            'strength': 'strong',
                            'effect': 'Brings success, power, and recognition',
                            'life_area': 'Career, authority, leadership'
                        })

        except Exception as e:
            logger.error(f"Error detecting Raj Yoga: {str(e)}")

        return raj_yogas

    def _detect_parivartana_yoga(self) -> List[Dict]:
        """
        Detect Parivartana Yoga - mutual exchange of planets.

        When two planets exchange their houses or signs.
        This creates powerful mutual support.
        """
        parivartana_yogas = []

        try:
            planets_list = list(self.planets_info.keys())

            for i, planet1 in enumerate(planets_list):
                for planet2 in planets_list[i + 1:]:
                    house1 = self.planets_info[planet1].get('house')
                    house2 = self.planets_info[planet2].get('house')
                    sign1 = self.planets_info[planet1].get('sign')
                    sign2 = self.planets_info[planet2].get('sign')

                    # Check for house exchange (simplified)
                    if (house1 and house2 and
                        abs(house1 - house2) == 6):  # Opposite houses

                        parivartana_yogas.append({
                            'name': 'Parivartana Yoga',
                            'planets': [planet1, planet2],
                            'description': f'{planet1} and {planet2} exchange influences',
                            'strength': 'very strong',
                            'effect': 'Mutual support and cancellation of debilitation',
                            'life_area': 'Both planets benefit mutually'
                        })

        except Exception as e:
            logger.error(f"Error detecting Parivartana Yoga: {str(e)}")

        return parivartana_yogas

    def _detect_neecha_bhanga_yoga(self) -> List[Dict]:
        """
        Detect Neecha Bhanga Yoga - cancellation of debilitation.

        When a debilitated planet is helped by:
        - Its sign dispositor being strong
        - Its exaltation sign lord being strong
        - Aspects from benefic planets
        """
        neecha_bhanga = []

        try:
            for planet, debilitated_sign in self.debilitated_signs.items():
                if planet in self.planets_info:
                    planet_sign = self.planets_info[planet].get('sign')

                    # Check if planet is debilitated
                    if planet_sign == debilitated_sign:
                        # Check if helped by other planets
                        is_cancellation_possible = False

                        # Check for aspect from benefic planets
                        for benefic in ['Jupiter', 'Venus', 'Mercury']:
                            if benefic in self.planets_info:
                                benefic_house = self.planets_info[benefic].get('house')
                                planet_house = self.planets_info[planet].get('house')

                                if benefic_house and planet_house:
                                    # Check if in 7th aspect
                                    if abs(benefic_house - planet_house) == 6:
                                        is_cancellation_possible = True
                                        break

                        if is_cancellation_possible:
                            neecha_bhanga.append({
                                'name': 'Neecha Bhanga Yoga',
                                'planet': planet,
                                'description': f'Debilitated {planet} gets cancellation support',
                                'strength': 'moderate',
                                'effect': 'Debilitation effects are reduced or cancelled',
                                'life_area': f'Areas governed by {planet}'
                            })

        except Exception as e:
            logger.error(f"Error detecting Neecha Bhanga Yoga: {str(e)}")

        return neecha_bhanga

    def _detect_gaj_kesari_yoga(self) -> Optional[Dict]:
        """
        Detect Gaj Kesari Yoga - Jupiter and Moon conjunction/mutual aspect.

        One of the most auspicious yogas.
        Brings wisdom, prosperity, and spiritual growth.
        """
        try:
            if 'Jupiter' in self.planets_info and 'Moon' in self.planets_info:
                jupiter_house = self.planets_info['Jupiter'].get('house')
                moon_house = self.planets_info['Moon'].get('house')

                if jupiter_house and moon_house:
                    # Check conjunction (same house)
                    if jupiter_house == moon_house:
                        return {
                            'name': 'Gaj Kesari Yoga',
                            'planets': ['Jupiter', 'Moon'],
                            'description': 'Jupiter and Moon are conjoined',
                            'strength': 'very strong',
                            'effect': 'Brings wisdom, prosperity, and intellectual development',
                            'life_area': 'Education, spirituality, wealth, children'
                        }

                    # Check 7th aspect
                    if abs(jupiter_house - moon_house) == 6:
                        return {
                            'name': 'Gaj Kesari Yoga',
                            'planets': ['Jupiter', 'Moon'],
                            'description': 'Jupiter and Moon are in mutual 7th aspect',
                            'strength': 'strong',
                            'effect': 'Brings wisdom and prosperity',
                            'life_area': 'Education, spirituality, wealth'
                        }

        except Exception as e:
            logger.error(f"Error detecting Gaj Kesari Yoga: {str(e)}")

        return None

    def _detect_chandra_mangal_yoga(self) -> Optional[Dict]:
        """
        Detect Chandra Mangal Yoga - Moon and Mars conjunction.

        Brings emotional strength, courage, and martial qualities.
        """
        try:
            if 'Moon' in self.planets_info and 'Mars' in self.planets_info:
                moon_house = self.planets_info['Moon'].get('house')
                mars_house = self.planets_info['Mars'].get('house')

                if moon_house and mars_house and moon_house == mars_house:
                    return {
                        'name': 'Chandra Mangal Yoga',
                        'planets': ['Moon', 'Mars'],
                        'description': 'Moon and Mars are conjoined',
                        'strength': 'strong',
                        'effect': 'Brings courage, emotional strength, and energy',
                        'life_area': 'Sports, military, competitive fields'
                    }

        except Exception as e:
            logger.error(f"Error detecting Chandra Mangal Yoga: {str(e)}")

        return None

    def _detect_dhana_yoga(self) -> Optional[Dict]:
        """
        Detect Dhana Yoga - wealth-giving combinations.

        When planets associated with wealth are strong.
        """
        try:
            wealth_planets = ['Jupiter', 'Venus', 'Mercury']
            strong_wealth_planets = [p for p in wealth_planets
                                     if p in self.planets_info and
                                     self.planets_info[p].get('strength') in ['strong', 'very strong']]

            if len(strong_wealth_planets) >= 2:
                return {
                    'name': 'Dhana Yoga',
                    'planets': strong_wealth_planets,
                    'description': f'Strong wealth planets: {", ".join(strong_wealth_planets)}',
                    'strength': 'strong',
                    'effect': 'Brings wealth, financial success, and prosperity',
                    'life_area': 'Business, finance, wealth accumulation'
                }

        except Exception as e:
            logger.error(f"Error detecting Dhana Yoga: {str(e)}")

        return None

    def _detect_bhagya_yoga(self) -> Optional[Dict]:
        """
        Detect Bhagya Yoga - fortune and luck yoga.

        When 9th house lord is strong and beneficially placed.
        """
        try:
            if 'Jupiter' in self.planets_info:
                jupiter = self.planets_info['Jupiter']
                if jupiter.get('strength') in ['strong', 'very strong']:
                    return {
                        'name': 'Bhagya Yoga',
                        'planet': 'Jupiter',
                        'description': 'Strong Jupiter in fortunate position',
                        'strength': 'strong',
                        'effect': 'Brings luck, fortune, and protection',
                        'life_area': 'Travel, education, spiritual growth, luck'
                    }

        except Exception as e:
            logger.error(f"Error detecting Bhagya Yoga: {str(e)}")

        return None

    def _detect_papa_yoga(self) -> Optional[Dict]:
        """
        Detect Papa Yoga - inauspicious combinations.

        When malefic planets conjoin or aspect negatively.
        """
        try:
            malefic_planets = ['Mars', 'Saturn', 'Rahu', 'Ketu']
            malefic_list = [p for p in malefic_planets if p in self.planets_info]

            if len(malefic_list) >= 2:
                # Check for conjunctions
                for i, p1 in enumerate(malefic_list):
                    for p2 in malefic_list[i + 1:]:
                        if (self.planets_info[p1].get('house') ==
                            self.planets_info[p2].get('house')):
                            return {
                                'name': 'Papa Yoga',
                                'planets': [p1, p2],
                                'description': f'Malefic planets {p1} and {p2} are conjoined',
                                'strength': 'challenging',
                                'effect': 'Brings obstacles, delays, and difficulties',
                                'life_area': 'General obstacles and challenges'
                            }

        except Exception as e:
            logger.error(f"Error detecting Papa Yoga: {str(e)}")

        return None

    def _generate_yoga_summary(self) -> Dict:
        """Generate summary of yogas in chart."""
        all_yogas = self.detect_all_yogas()
        benefic = all_yogas.get('benefic_yogas', [])
        malefic = all_yogas.get('malefic_yogas', [])

        return {
            'total_benefic_yogas': len(benefic),
            'total_malefic_yogas': len(malefic),
            'net_yoga_influence': 'positive' if len(benefic) > len(malefic) else 'challenging',
            'overall_chart_quality': self._assess_chart_quality(benefic, malefic)
        }

    def _assess_chart_quality(self, benefic: List[Dict], malefic: List[Dict]) -> str:
        """Assess overall quality based on yogas."""
        if len(benefic) >= 3:
            return 'Excellent - Very auspicious chart'
        elif len(benefic) >= 1:
            return 'Good - Generally favorable chart'
        elif len(malefic) >= 2:
            return 'Challenging - Requires careful navigation'
        else:
            return 'Mixed - Both positive and challenging influences'
