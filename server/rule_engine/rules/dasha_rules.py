"""
Dasha Interpretation Rules
Provides human-readable interpretations and predictions based on Dasha periods.

Author: Astrology Backend
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class DashaRules:
    """Generate interpretations based on current and upcoming Dasha periods."""

    @staticmethod
    def interpret_current_dasha(dasha_info: Dict) -> List[str]:
        """
        Generate interpretation for current Dasha period.

        Args:
            dasha_info: Dictionary with Dasha calculation results

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            current_dasha = dasha_info.get('current_maha_dasha')
            remaining_years = dasha_info.get('remaining_maha_dasha_years', 0)
            next_dasha = dasha_info.get('next_dasha_lord')

            if not current_dasha:
                return ["Unable to interpret Dasha at this time"]

            # General interpretation based on current dasha
            dasha_interpretations = {
                'Sun': [
                    f"You are currently under {current_dasha} Maha Dasha, which lasts {int(remaining_years)} more years.",
                    "This is a period of self-assertion, ambition, and seeking recognition.",
                    "Focus on developing your authority and leadership qualities.",
                    "Be cautious of ego and overconfidence during this period.",
                    "Health-wise, pay attention to the heart and circulatory system.",
                    "This period favors professional achievements and public recognition."
                ],
                'Moon': [
                    f"You are under {current_dasha} Maha Dasha with approximately {int(remaining_years)} years remaining.",
                    "This is a period of emotional sensitivity and psychological development.",
                    "Focus on nurturing relationships, especially with family and close ones.",
                    "Mental peace and emotional stability are key themes.",
                    "Travel and relocation may be favorable during this period.",
                    "This is an excellent time for spiritual development and introspection."
                ],
                'Mars': [
                    f"You are currently in {current_dasha} Maha Dasha for about {int(remaining_years)} more years.",
                    "This is a period of high energy, courage, and action.",
                    "Channel your aggressive energy into competitive ventures and sports.",
                    "Property transactions and real estate deals are favored.",
                    "Be cautious of accidents, conflicts, and impulsive decisions.",
                    "Sibling relationships may require attention during this period."
                ],
                'Mercury': [
                    f"You are under {current_dasha} Maha Dasha, a {int(remaining_years)}-year period ahead.",
                    "This is a period of intellectual growth, communication, and learning.",
                    "Business ventures and commerce are particularly favored.",
                    "Writing, teaching, and media activities will flourish.",
                    "Be cautious of nervousness and mental restlessness.",
                    "Short journeys and trading activities are beneficial."
                ],
                'Jupiter': [
                    f"You are blessed with {current_dasha} Maha Dasha, with {int(remaining_years)} years remaining.",
                    "This is a period of expansion, wisdom, and spiritual growth.",
                    "Children and family matters receive positive influences.",
                    "This is an excellent time for higher education and learning.",
                    "Wealth accumulation and prosperity are likely during this period.",
                    "Religious and spiritual inclinations will strengthen."
                ],
                'Venus': [
                    f"You are under {current_dasha} Maha Dasha for approximately {int(remaining_years)} more years.",
                    "This is a period of love, beauty, and artistic expression.",
                    "Marriage and relationship matters are significantly favored.",
                    "Enjoyment, luxury, and comfort are theme of this period.",
                    "Creative and artistic pursuits will flourish.",
                    "Be cautious of over-indulgence and sensual excess."
                ],
                'Saturn': [
                    f"You are in {current_dasha} Maha Dasha, with {int(remaining_years)} years left.",
                    "This is a period of discipline, hard work, and karmic lessons.",
                    "Expect delays and obstacles, but they lead to lasting foundations.",
                    "Patience and perseverance are essential virtues now.",
                    "This period favors spiritual growth and detachment.",
                    "Long-term projects and commitments will bear fruit."
                ],
                'Rahu': [
                    f"You are under {current_dasha} Maha Dasha for {int(remaining_years)} more years.",
                    "This is a period of rapid changes, success, and sometimes illusions.",
                    "Foreign matters and technology ventures are highly favored.",
                    "Unexpected gains and opportunities may appear.",
                    "Be cautious of obsessions, addictions, and illusions.",
                    "This period can bring sudden fame and recognition."
                ],
                'Ketu': [
                    f"You are in {current_dasha} Maha Dasha, with {int(remaining_years)} years remaining.",
                    "This is a period of spiritual growth and detachment from worldly matters.",
                    "Focus on inner development and meditation practices.",
                    "A minimalist approach will serve you well.",
                    "Health requires careful attention during this period.",
                    "This period favors occult studies and spiritual knowledge."
                ]
            }

            if current_dasha in dasha_interpretations:
                interpretations.extend(dasha_interpretations[current_dasha])

            # Next dasha transition
            if next_dasha and remaining_years < 3:
                interpretations.append(
                    f"\nTransition Alert: You are approaching {next_dasha} Maha Dasha. "
                    f"Prepare for a shift in life's themes and priorities."
                )

        except Exception as e:
            logger.error(f"Error interpreting current Dasha: {str(e)}", exc_info=True)
            interpretations.append("Unable to provide detailed interpretation at this time.")

        return interpretations

    @staticmethod
    def get_dasha_period_quality(planet: str) -> str:
        """
        Get the overall quality/nature of a Dasha period.

        Args:
            planet: Planet name

        Returns:
            Quality descriptor string
        """
        quality_map = {
            'Sun': 'Powerful and authoritative - strong results but may bring ego challenges',
            'Moon': 'Gentle and emotional - focuses on mind, emotions, and comfort',
            'Mars': 'Energetic and aggressive - brings action but risk of accidents',
            'Mercury': 'Intellectual and communicative - favors learning and commerce',
            'Jupiter': 'Expansive and beneficial - the most fortunate period typically',
            'Venus': 'Pleasurable and artistic - favors relationships and beauty',
            'Saturn': 'Challenging but rewarding - builds character through trials',
            'Rahu': 'Unpredictable and dynamic - sudden changes and unexpected gains',
            'Ketu': 'Spiritual and detaching - inner development focus'
        }
        return quality_map.get(planet, 'Unknown quality')

    @staticmethod
    def get_antar_dasha_influence(maha_lord: str, antar_lord: str) -> List[str]:
        """
        Get interpretation of Antar Dasha influence within Maha Dasha.

        Args:
            maha_lord: Main period planet
            antar_lord: Sub-period planet

        Returns:
            List of interpretation strings
        """
        interpretations = []

        try:
            # Compatibility matrix for planet combinations
            influence_map = {
                ('Sun', 'Sun'): [
                    "Double strength of Sun's qualities",
                    "Highest authority and recognition period",
                    "Ego and pride need management"
                ],
                ('Sun', 'Moon'): [
                    "Balance between will and emotion",
                    "Good for public relations and popularity",
                    "Some emotional challenges with authority figures"
                ],
                ('Moon', 'Venus'): [
                    "Excellent for relationships and romance",
                    "Emotional fulfillment and comfort sought",
                    "Social popularity increases"
                ],
                ('Jupiter', 'Jupiter'): [
                    "Double blessing period - very auspicious",
                    "Expansion and prosperity at maximum",
                    "Spiritual growth accelerates"
                ],
                ('Saturn', 'Saturn'): [
                    "Double challenges - difficult period",
                    "Patience and persistence absolutely required",
                    "But great rewards for sincere effort"
                ]
            }

            # Check for specific combination
            key = (maha_lord, antar_lord)
            if key in influence_map:
                interpretations.extend(influence_map[key])
            else:
                # Generic interpretation
                interpretations.append(
                    f"During {antar_lord} sub-period within {maha_lord} Maha Dasha: "
                    f"Expect blended influences of both planets"
                )

        except Exception as e:
            logger.error(f"Error getting Antar Dasha influence: {str(e)}", exc_info=True)

        return interpretations if interpretations else ["Sub-period influence varies based on planetary positions"]

    @staticmethod
    def predict_dasha_events(dasha_info: Dict, planets_info: Dict) -> List[str]:
        """
        Predict possible events during current Dasha period.

        Args:
            dasha_info: Dictionary with Dasha calculations
            planets_info: Dictionary with planetary positions

        Returns:
            List of event predictions
        """
        predictions = []

        try:
            current_dasha = dasha_info.get('current_maha_dasha')
            remaining_years = dasha_info.get('remaining_maha_dasha_years', 0)

            if not current_dasha:
                return ["Unable to make predictions at this time"]

            # Event predictions based on Dasha
            event_map = {
                'Sun': [
                    "Possible promotion or increase in professional status",
                    "Good period for starting your own business/ventures",
                    "Government or authority-related gains likely",
                    "Watch for health issues related to heart/circulation"
                ],
                'Moon': [
                    "Relocation or change of residence likely",
                    "Maternal relationships undergo significant changes",
                    "Property and real estate gains possible",
                    "International travel may be on the cards"
                ],
                'Mars': [
                    "Real estate or property acquisitions likely",
                    "Be cautious of accidents and injuries",
                    "Possible surgery or medical procedures",
                    "Sibling relationships may need resolution"
                ],
                'Mercury': [
                    "Business expansion and new ventures likely",
                    "Communication-related successes expected",
                    "Short journeys and travel for business",
                    "Education and learning opportunities abound"
                ],
                'Jupiter': [
                    "Childbirth or family expansion possible",
                    "Educational achievements and higher learning",
                    "Significant wealth accumulation likely",
                    "Spiritual inclination and religious activities increase"
                ],
                'Venus': [
                    "Marriage or serious relationship formation likely",
                    "Artistic and creative projects flourish",
                    "Luxury purchases and comfort gains",
                    "Watch for relationship-related challenges"
                ],
                'Saturn': [
                    "Major life lessons and character building",
                    "Long-term projects finally bear fruit",
                    "Possible losses to teach detachment",
                    "Spiritual development accelerates"
                ],
                'Rahu': [
                    "Unexpected fortunate events possible",
                    "Foreign travel or relocation likely",
                    "Rapid success in technology/modern ventures",
                    "Be cautious of illusions and false promises"
                ],
                'Ketu': [
                    "Spiritual awakening or occult interest",
                    "Possible isolation or withdrawal from social life",
                    "Health issues require attention",
                    "Losses or detachment from material possessions"
                ]
            }

            if current_dasha in event_map:
                predictions.extend(event_map[current_dasha])

            # Add timeline context
            if remaining_years < 1:
                predictions.append("\nImportant: Your current Dasha is ending soon. Prepare for major life changes.")
            elif remaining_years < 5:
                predictions.append(f"\nNote: {int(remaining_years)} years remain in current Dasha. Begin planning for transition.")

        except Exception as e:
            logger.error(f"Error predicting Dasha events: {str(e)}", exc_info=True)
            predictions.append("Unable to provide detailed predictions at this time.")

        return predictions

    @staticmethod
    def get_dasha_remedies(planet: str) -> List[str]:
        """
        Get remedies and recommendations for managing Dasha effects.

        Args:
            planet: Planet name

        Returns:
            List of remedy/recommendation strings
        """
        remedies = {
            'Sun': [
                "Chant Aditya Hridaya Stotra or Sun mantras",
                "Donate gold, wheat, or red items",
                "Avoid conflicts with authority figures",
                "Practice yoga and develop self-confidence",
                "Wear ruby or saffron color"
            ],
            'Moon': [
                "Chant Moon mantras or Chandra Beej mantra",
                "Donate white items or silver",
                "Maintain emotional balance through meditation",
                "Avoid excessive water-related risks",
                "Wear pearl or white color"
            ],
            'Mars': [
                "Chant Mars mantras or Mangal Beej mantra",
                "Donate red items, blood, or lentils",
                "Practice caution in travel and driving",
                "Avoid conflicts and aggressive behavior",
                "Wear red coral with proper consultation"
            ],
            'Mercury': [
                "Chant Mercury mantras or Budha Beej mantra",
                "Donate green items or emeralds",
                "Engage in writing, teaching, and learning",
                "Maintain mental clarity through meditation",
                "Wear emerald or green color"
            ],
            'Jupiter': [
                "Chant Jupiter mantras or Brihaspati Beej mantra",
                "Donate yellow items or gold",
                "Practice generosity and charity",
                "Engage in spiritual and religious activities",
                "Wear yellow sapphire with proper consultation"
            ],
            'Venus': [
                "Chant Venus mantras or Shukra Beej mantra",
                "Donate white items or diamonds",
                "Practice moderation in pleasures",
                "Engage in artistic and creative pursuits",
                "Wear diamond or white color"
            ],
            'Saturn': [
                "Chant Saturn mantras or Shani Beej mantra",
                "Donate black items or iron",
                "Practice patience and discipline",
                "Serve the poor and marginalized",
                "Wear blue sapphire with proper consultation"
            ],
            'Rahu': [
                "Chant Rahu mantras or Rahu Beej mantra",
                "Donate blue items or mustard seeds",
                "Avoid addictions and obsessions",
                "Practice grounding meditation",
                "Wear hessonite (gomedh) with proper consultation"
            ],
            'Ketu': [
                "Chant Ketu mantras or Ketu Beej mantra",
                "Donate brown items or sesame",
                "Engage in spiritual practices and meditation",
                "Study occult sciences and philosophy",
                "Wear cat's eye with proper consultation"
            ]
        }

        return remedies.get(planet, [
            "Consult a qualified astrologer for personalized remedies",
            "Practice meditation and mindfulness",
            "Focus on self-improvement and character development"
        ])
