"""
Planetary Strength Interpretation Rules
Provides meaningful interpretations based on Shad Bala analysis.

Author: Astrology Backend
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class StrengthRules:
    """Generate interpretations based on planetary strengths."""

    @staticmethod
    def interpret_planetary_strength(strength_data: Dict) -> List[str]:
        """
        Generate interpretations for a planet's strength.

        Args:
            strength_data: Complete strength analysis for a planet

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            planet = strength_data.get('planet')
            percentage = strength_data.get('strength_percentage', 0)
            breakdown = strength_data.get('breakdown', {})
            status = strength_data.get('strength_status')

            if not planet:
                return ["Unable to interpret strength data"]

            # Main interpretation
            interpretations.append(
                f"{planet} is {status} with {percentage}% strength"
            )

            # Capacity interpretation
            if percentage >= 80:
                interpretations.append(
                    f"{planet} can give excellent results in its dasha and transit periods"
                )
                interpretations.append(
                    f"Full capacity: All significations of {planet} will manifest favorably"
                )
            elif percentage >= 60:
                interpretations.append(
                    f"{planet} can give good results with proper conditions"
                )
                interpretations.append(
                    f"Good capacity: Most significations of {planet} will materialize"
                )
            elif percentage >= 40:
                interpretations.append(
                    f"{planet} gives mixed results - both favorable and challenging"
                )
                interpretations.append(
                    f"Moderate capacity: Some significations will work, others won't"
                )
            else:
                interpretations.append(
                    f"{planet} struggles to give results due to weakness"
                )
                interpretations.append(
                    f"Limited capacity: Significations are minimized or blocked"
                )

            # Breakdown analysis
            sthana = breakdown.get('sthana_bala', 0)
            dig = breakdown.get('dig_bala', 0)
            kala = breakdown.get('kala_bala', 0)
            chesta = breakdown.get('chesta_bala', 0)
            naisargika = breakdown.get('naisargika_bala', 0)
            drishti = breakdown.get('drishti_bala', 0)

            if sthana >= 12:
                interpretations.append(
                    f"{planet}'s position in the zodiac is excellent"
                )
            elif sthana <= 5:
                interpretations.append(
                    f"{planet} is poorly placed in the zodiac - needs remedies"
                )

            if dig >= 12:
                interpretations.append(
                    f"{planet} is in a favorable direction"
                )

            if kala >= 10:
                interpretations.append(
                    f"Time factors support {planet}"
                )

            if chesta >= 12:
                interpretations.append(
                    f"{planet} has good motion and speed"
                )

            if drishti >= 10:
                interpretations.append(
                    f"{planet} is receiving beneficial aspects"
                )
            elif drishti <= 3:
                interpretations.append(
                    f"{planet} is under malefic influence - external support needed"
                )

        except Exception as e:
            logger.error(f"Error interpreting strength: {str(e)}")
            interpretations.append("Unable to generate interpretation")

        return interpretations

    @staticmethod
    def get_strength_remedies(planet: str, percentage: float) -> List[str]:
        """
        Get remedies for weak planets.

        Args:
            planet: Planet name
            percentage: Strength percentage

        Returns:
            List of remedy suggestions
        """
        if percentage >= 70:
            return [f"{planet} is strong - No special remedies needed"]

        remedies = {
            'Sun': [
                "Chant Aditya Hridaya Stotra or Sun mantras daily",
                "Donate saffron, gold, or red cloth",
                "Perform Surya Namaskar (Sun salutation) every morning",
                "Wear ruby or red coral gemstone",
                "Fast on Sundays",
                "Spend time in sunlight"
            ],
            'Moon': [
                "Chant Moon mantras or 'Om Chandaya Namaha'",
                "Donate white items, milk, or silver",
                "Observe fasting on Mondays",
                "Wear pearl gemstone",
                "Practice meditation for mental peace",
                "Keep water-related objects at home"
            ],
            'Mars': [
                "Chant Mars mantras or 'Om Mangalaya Namaha'",
                "Donate red items, blood, or red lentils",
                "Practice martial arts or physical activities",
                "Wear red coral or red stone",
                "Fast on Tuesdays",
                "Be courageous and stand for justice"
            ],
            'Mercury': [
                "Chant Mercury mantras or 'Om Buddhaya Namaha'",
                "Donate green items or emeralds",
                "Engage in business and trading",
                "Wear green or emerald stone",
                "Improve communication skills",
                "Study and teach others"
            ],
            'Jupiter': [
                "Chant Jupiter mantras or 'Om Guruve Namaha'",
                "Donate yellow items, gold, or turmeric",
                "Wear yellow sapphire gemstone",
                "Fast on Thursdays",
                "Feed cows and poor people",
                "Engage in spiritual practices"
            ],
            'Venus': [
                "Chant Venus mantras or 'Om Shukraya Namaha'",
                "Donate white items, diamonds, or perfume",
                "Wear diamond or white stone",
                "Cultivate arts and beauty",
                "Maintain harmonious relationships",
                "Practice devotion and love"
            ],
            'Saturn': [
                "Chant Saturn mantras or 'Om Shanaischaraya Namaha'",
                "Donate black items, iron, or mustard seeds",
                "Wear blue sapphire (consult astrologer first)",
                "Fast on Saturdays",
                "Serve the poor and disabled",
                "Practice discipline and patience"
            ],
            'Rahu': [
                "Chant Rahu mantras or 'Om Rahuve Namaha'",
                "Donate blue or dark items",
                "Wear hessonite (gomedh) gemstone",
                "Perform Durga Puja or Kali Puja",
                "Practice grounding meditation",
                "Avoid addictions and obsessions"
            ],
            'Ketu': [
                "Chant Ketu mantras or 'Om Ketave Namaha'",
                "Donate brown or dark items and sesame",
                "Wear cat's eye gemstone",
                "Engage in spiritual practices",
                "Practice meditation regularly",
                "Study occult sciences"
            ]
        }

        planet_remedies = remedies.get(planet, [
            "Consult a qualified astrologer for personalized remedies",
            "Perform charitable deeds",
            "Practice meditation and yoga"
        ])

        if percentage < 40:
            planet_remedies.insert(0, "⚠️ CRITICAL: Planet is very weak - immediate remedies recommended")

        return planet_remedies

    @staticmethod
    def interpret_chart_strength(chart_strength: Dict) -> List[str]:
        """
        Generate interpretations for overall chart strength.

        Args:
            chart_strength: Overall chart strength assessment

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            strong_count = chart_strength.get('strong_planets_count', 0)
            quality = chart_strength.get('chart_quality', '')
            avg_strength = chart_strength.get('average_planet_strength', 0)

            interpretations.append(f"Overall Chart Quality: {quality}")

            if strong_count >= 6:
                interpretations.append(
                    "You have excellent planetary support - Life will generally flow smoothly"
                )
                interpretations.append(
                    "Multiple strong planets indicate you can handle life's challenges well"
                )
            elif strong_count >= 4:
                interpretations.append(
                    "You have good planetary support - Can achieve goals with effort"
                )
                interpretations.append(
                    "Adequate strength to overcome obstacles"
                )
            elif strong_count >= 2:
                interpretations.append(
                    "You have moderate planetary support - Mixed results expected"
                )
                interpretations.append(
                    "Need to work harder to achieve goals"
                )
            else:
                interpretations.append(
                    "You have limited planetary support - Challenges are likely"
                )
                interpretations.append(
                    "Focus on remedies for weak planets"
                )

            if avg_strength >= 40:
                interpretations.append(
                    "Average planetary strength is good - Most areas of life are supported"
                )
            elif avg_strength >= 25:
                interpretations.append(
                    "Average strength is moderate - Some areas need attention"
                )
            else:
                interpretations.append(
                    "Average strength is low - Comprehensive remedies recommended"
                )

            strong_planets = chart_strength.get('strong_planets', [])
            if strong_planets:
                interpretations.append(
                    f"Strong planets: {', '.join(strong_planets)} - "
                    f"These will give excellent results in their periods"
                )

        except Exception as e:
            logger.error(f"Error interpreting chart strength: {str(e)}")

        return interpretations

    @staticmethod
    def get_strength_timing_predictions(planet: str, strength_percentage: float) -> Dict:
        """
        Get predictions based on planet strength during its dasha.

        Args:
            planet: Planet name
            strength_percentage: Planet's strength percentage

        Returns:
            Dictionary with timing predictions
        """
        predictions = {
            'planet': planet,
            'strength_level': 'Strong' if strength_percentage >= 70 else 'Weak',
            'dasha_prediction': ''
        }

        if strength_percentage >= 80:
            predictions['dasha_prediction'] = (
                f"{planet} Dasha will be highly beneficial. "
                f"Major positive events and growth expected. "
                f"All significations of {planet} will manifest excellently."
            )
            predictions['expected_results'] = 'Excellent'
        elif strength_percentage >= 60:
            predictions['dasha_prediction'] = (
                f"{planet} Dasha will be generally favorable. "
                f"Good results expected with some challenges. "
                f"Most significations will work positively."
            )
            predictions['expected_results'] = 'Good'
        elif strength_percentage >= 40:
            predictions['dasha_prediction'] = (
                f"{planet} Dasha will give mixed results. "
                f"Both positive and challenging periods expected. "
                f"Outcomes depend on other planetary periods."
            )
            predictions['expected_results'] = 'Mixed'
        else:
            predictions['dasha_prediction'] = (
                f"{planet} Dasha may be challenging. "
                f"Limited positive results. Obstacles expected. "
                f"Remedies strongly recommended."
            )
            predictions['expected_results'] = 'Challenging'

        return predictions

    @staticmethod
    def generate_strength_action_plan(strengths_data: Dict) -> List[str]:
        """
        Generate practical action plan based on strengths.

        Args:
            strengths_data: Complete strength analysis

        Returns:
            List of action items
        """
        action_plan = []

        try:
            planetary_strengths = strengths_data.get('planetary_strengths', {})

            # Find weak planets
            weak_planets = [
                p for p, data in planetary_strengths.items()
                if isinstance(data, dict) and not data.get('is_strong')
            ]

            # Find strong planets
            strong_planets = [
                p for p, data in planetary_strengths.items()
                if isinstance(data, dict) and data.get('is_strong')
            ]

            if weak_planets:
                action_plan.append(
                    f"1. Focus on strengthening: {', '.join(weak_planets)}"
                )
                for planet in weak_planets:
                    action_plan.append(
                        f"   - Research and perform remedies for {planet}"
                    )

            if strong_planets:
                action_plan.append(
                    f"2. Leverage strength of: {', '.join(strong_planets)}"
                )
                action_plan.append(
                    "   - Plan important activities during these planets' periods"
                )

            action_plan.append("3. General practices:")
            action_plan.append("   - Regular meditation and yoga")
            action_plan.append("   - Charitable deeds and service")
            action_plan.append("   - Follow ethical practices")
            action_plan.append("   - Maintain positive mindset")

            action_plan.append("4. Consult astrologer for:")
            action_plan.append("   - Gemstone recommendations")
            action_plan.append("   - Personalized rituals")
            action_plan.append("   - Timing of important events")
            action_plan.append("   - Career guidance based on strengths")

        except Exception as e:
            logger.error(f"Error generating action plan: {str(e)}")
            action_plan.append("Consult a qualified astrologer for guidance")

        return action_plan
