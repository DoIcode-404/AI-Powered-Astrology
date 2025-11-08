"""
Divisional Charts Interpretation Rules
Provides meaningful interpretations for D1, D2, D7, D9 charts.

Author: Astrology Backend
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class VargaRules:
    """Generate interpretations for divisional charts."""

    @staticmethod
    def interpret_navamsha_chart(navamsha_data: Dict) -> List[str]:
        """
        Generate interpretations for Navamsha (D9) chart.

        Navamsha is most important for marriage and hidden nature.

        Args:
            navamsha_data: Navamsha chart data

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            planets = navamsha_data.get('planets', {})
            ascendant = navamsha_data.get('ascendant', '')

            interpretations.append("NAVAMSHA CHART (D9) - Marriage & Hidden Nature")
            interpretations.append("=" * 50)

            # Ascendant interpretation
            if ascendant:
                interpretations.append(
                    f"Navamsha Ascendant is {ascendant}"
                )
                interpretations.append(
                    f"This reveals hidden strengths and spiritual nature"
                )

            # Venus position (marriage indicator)
            venus = planets.get('Venus', {})
            if venus:
                venus_sign = venus.get('navamsha_sign', 'Unknown')
                interpretations.append(
                    f"Venus in {venus_sign} (Navamsha) - Marriage quality"
                )
                interpretations.append(
                    VargaRules._get_navamsha_venus_interpretation(venus_sign)
                )

            # Jupiter position (spouse quality)
            jupiter = planets.get('Jupiter', {})
            if jupiter:
                jupiter_sign = jupiter.get('navamsha_sign', 'Unknown')
                interpretations.append(
                    f"Jupiter in {jupiter_sign} (Navamsha) - Spouse qualities"
                )

            # 7th house analysis
            interpretations.append(
                "Navamsha reveals the true nature of marriage"
            )
            interpretations.append(
                "Benefic placements indicate harmonious partnerships"
            )
            interpretations.append(
                "Malefic placements may indicate challenges in marriage"
            )

            # Marriage quality assessment
            marriage_analysis = navamsha_data.get('marriage_analysis', {})
            if marriage_analysis:
                interpretations.append(
                    VargaRules._assess_navamsha_marriage_quality(marriage_analysis)
                )

        except Exception as e:
            logger.error(f"Error interpreting Navamsha: {str(e)}")
            interpretations.append("Unable to generate Navamsha interpretation")

        return interpretations

    @staticmethod
    def _get_navamsha_venus_interpretation(venus_sign: str) -> str:
        """Get interpretation for Venus position in Navamsha."""
        interpretations = {
            'Aries': 'Passionate marriage, active partnership, adventurous',
            'Taurus': 'Stable, loyal, sensual, secure marriage',
            'Gemini': 'Communicative, diverse interests, intellectual partner',
            'Cancer': 'Emotional bond, nurturing, family-oriented',
            'Leo': 'Proud, generous, romantic, loyal partnership',
            'Virgo': 'Analytical, practical, service-oriented, particular',
            'Libra': 'Harmonious, balanced, romantic, social partnership',
            'Scorpio': 'Intense, passionate, mysterious, deep connection',
            'Sagittarius': 'Adventurous, philosophical, freedom-loving',
            'Capricorn': 'Traditional, committed, responsible partnership',
            'Aquarius': 'Unconventional, intellectual, independent marriage',
            'Pisces': 'Spiritual, romantic, sacrificing, idealistic'
        }
        return interpretations.get(venus_sign, 'Venus position indicates specific marriage qualities')

    @staticmethod
    def _assess_navamsha_marriage_quality(marriage_analysis: Dict) -> str:
        """Assess overall marriage quality from Navamsha."""
        venus_pos = marriage_analysis.get('venus_position', '')
        moon_pos = marriage_analysis.get('moon_position', '')

        if venus_pos and moon_pos:
            return (
                f"Venus in {venus_pos} and Moon in {moon_pos} "
                f"indicate marriage compatibility potential"
            )
        return "Assess marriage quality based on benefic planet positions"

    @staticmethod
    def interpret_hora_chart(hora_data: Dict) -> List[str]:
        """
        Generate interpretations for Hora (D2) chart.

        Hora is for wealth and finance.

        Args:
            hora_data: Hora chart data

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            planets = hora_data.get('planets', {})
            ascendant = hora_data.get('ascendant', '')

            interpretations.append("HORA CHART (D2) - Wealth & Finance")
            interpretations.append("=" * 50)

            # Ascendant interpretation
            if ascendant:
                interpretations.append(
                    f"Hora Ascendant is {ascendant} - Indicates financial capacity"
                )

            # Jupiter position (wealth indicator)
            jupiter = planets.get('Jupiter', {})
            if jupiter:
                interpretations.append(
                    f"Jupiter position: {jupiter.get('hora_lord', 'Unknown')} - Wealth support"
                )

            # Venus position (luxury indicator)
            venus = planets.get('Venus', {})
            if venus:
                interpretations.append(
                    f"Venus position: {venus.get('hora_lord', 'Unknown')} - Comfort & luxury"
                )

            # Mercury position (business indicator)
            mercury = planets.get('Mercury', {})
            if mercury:
                interpretations.append(
                    f"Mercury position: {mercury.get('hora_lord', 'Unknown')} - Business & trade"
                )

            interpretations.append(
                "Hora chart shows financial success potential"
            )
            interpretations.append(
                "Benefic planets in good positions indicate wealth accumulation"
            )
            interpretations.append(
                "Analyze 2nd and 11th house lords for financial gains"
            )

        except Exception as e:
            logger.error(f"Error interpreting Hora: {str(e)}")
            interpretations.append("Unable to generate Hora interpretation")

        return interpretations

    @staticmethod
    def interpret_saptamsha_chart(saptamsha_data: Dict) -> List[str]:
        """
        Generate interpretations for Saptamsha (D7) chart.

        Saptamsha is for children and progeny.

        Args:
            saptamsha_data: Saptamsha chart data

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            planets = saptamsha_data.get('planets', {})
            ascendant = saptamsha_data.get('ascendant', '')

            interpretations.append("SAPTAMSHA CHART (D7) - Children & Progeny")
            interpretations.append("=" * 50)

            # Ascendant interpretation
            if ascendant:
                interpretations.append(
                    f"Saptamsha Ascendant is {ascendant} - Indicates progeny potential"
                )

            # Jupiter position (children indicator)
            jupiter = planets.get('Jupiter', {})
            if jupiter:
                significance = jupiter.get('interpretation', '')
                interpretations.append(
                    f"Jupiter (5th lord signification): {significance}"
                )

            # Moon position (children support)
            moon = planets.get('Moon', {})
            if moon:
                interpretations.append(
                    f"Moon in Saptamsha: Shows emotional connection with children"
                )

            interpretations.append(
                "Saptamsha reveals fertility and progeny prospects"
            )
            interpretations.append(
                "Strong placements indicate healthy children and family happiness"
            )
            interpretations.append(
                "Analyze 5th house lord for children-related matters"
            )

            fertility = saptamsha_data.get('fertility_analysis', {})
            if fertility:
                interpretations.append(
                    "Fertility indicators: Based on Jupiter and Moon in D7"
                )

        except Exception as e:
            logger.error(f"Error interpreting Saptamsha: {str(e)}")
            interpretations.append("Unable to generate Saptamsha interpretation")

        return interpretations

    @staticmethod
    def interpret_d1_d9_alignment(alignment_data: Dict) -> List[str]:
        """
        Interpret D1-D9 alignment significance.

        Strong alignment = Life and hidden nature are in harmony.

        Args:
            alignment_data: D1-D9 alignment analysis

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            score = alignment_data.get('alignment_score', 0)
            percentage = alignment_data.get('alignment_percentage', 0)
            interpretation = alignment_data.get('interpretation', '')

            interpretations.append("D1-D9 ALIGNMENT ANALYSIS")
            interpretations.append("=" * 50)
            interpretations.append(
                f"Alignment Score: {score}/90 ({percentage:.1f}%)"
            )
            interpretations.append(
                f"Interpretation: {interpretation}"
            )

            if percentage >= 70:
                interpretations.append(
                    "✓ Excellent alignment - What you see is what you get"
                )
                interpretations.append(
                    "Your apparent nature matches your true nature"
                )
                interpretations.append(
                    "Life developments are harmonious and predictable"
                )
            elif percentage >= 50:
                interpretations.append(
                    "△ Good alignment - Generally consistent"
                )
                interpretations.append(
                    "Minor differences between apparent and true nature"
                )
            elif percentage >= 30:
                interpretations.append(
                    "⚠ Moderate alignment - Some differences exist"
                )
                interpretations.append(
                    "Life may reveal hidden aspects of your nature"
                )
            else:
                interpretations.append(
                    "⚠ Weak alignment - Significant differences"
                )
                interpretations.append(
                    "True nature very different from apparent personality"
                )
                interpretations.append(
                    "Life is a journey of self-discovery and transformation"
                )

            details = alignment_data.get('details', [])
            if details:
                interpretations.append("\nPlanet-wise alignment:")
                interpretations.extend(details)

        except Exception as e:
            logger.error(f"Error interpreting alignment: {str(e)}")
            interpretations.append("Unable to generate alignment interpretation")

        return interpretations

    @staticmethod
    def get_varga_recommendations(all_vargas: Dict) -> List[str]:
        """
        Get recommendations based on all vargas.

        Args:
            all_vargas: Complete varga analysis

        Returns:
            List of recommendations
        """
        recommendations = []

        try:
            d9 = all_vargas.get('D9_Navamsha', {})
            d7 = all_vargas.get('D7_Saptamsha', {})
            d2 = all_vargas.get('D2_Hora', {})

            # Marriage recommendations
            if d9:
                recommendations.append(
                    "1. For Marriage: Study Navamsha (D9) carefully for compatibility"
                )
                recommendations.append(
                    "   - Match D9 charts with potential partners"
                )
                recommendations.append(
                    "   - Strong D9 alignment indicates stable marriage"
                )

            # Children recommendations
            if d7:
                recommendations.append(
                    "2. For Children: Analyze Saptamsha (D7) for progeny"
                )
                recommendations.append(
                    "   - Assess fertility and number of children"
                )
                recommendations.append(
                    "   - Plan for children during favorable dasha periods"
                )

            # Finance recommendations
            if d2:
                recommendations.append(
                    "3. For Wealth: Study Hora (D2) for financial success"
                )
                recommendations.append(
                    "   - Undertake financial ventures in favorable periods"
                )
                recommendations.append(
                    "   - Build wealth gradually with persistent effort"
                )

            recommendations.append(
                "4. General: Use vargas for timing important life events"
            )
            recommendations.append(
                "   - Plan marriage, children, investments based on varga analysis"
            )
            recommendations.append(
                "   - Vargas provide deeper insights than D1 alone"
            )

        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")

        return recommendations

    @staticmethod
    def get_varga_timing(vargas_data: Dict) -> Dict:
        """
        Get timing predictions based on vargas.

        Args:
            vargas_data: Complete varga data

        Returns:
            Dictionary with timing recommendations
        """
        return {
            'marriage_timing': 'Check D9 Navamsha for marriage indicators',
            'children_timing': 'Check D7 Saptamsha and 5th house for children',
            'wealth_timing': 'Check D2 Hora and 2nd/11th houses for wealth',
            'important_note': 'Use Dasha periods and transits with vargas for precise timing'
        }
