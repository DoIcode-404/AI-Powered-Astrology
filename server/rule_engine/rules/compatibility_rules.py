"""
Compatibility Rules and Interpretations
Provides detailed interpretations, remedies, and predictions for compatibility analysis.
"""

from typing import List, Dict, Any

# ========== INTERPRETATION TEMPLATES ==========

OVERLAY_INTERPRETATIONS = {
    "Sun": {
        "1": "Strong identity alignment. Your partner sees you clearly and is drawn to your essence.",
        "5": "Romantic attraction and creative collaboration. Natural chemistry.",
        "7": "Ideal placement for marriage. Partner recognizes you as potential life partner.",
        "8": "Intense attraction but may require emotional depth and trust building.",
        "11": "Strong friendship foundation. Good for long-term companionship.",
    },
    "Moon": {
        "1": "Emotional understanding. Your partner intuitively grasps your needs.",
        "5": "Emotional nurturing and care. Natural caregiving compatibility.",
        "7": "Domestic happiness and family orientation. Strong emotional bond.",
        "8": "Deep emotional connection but may have privacy needs.",
        "11": "Supportive and nurturing friendship. Comfortable companionship.",
    },
    "Venus": {
        "1": "Natural charm attracts partner. Aesthetic appreciation.",
        "5": "Love and affection. Strong romantic potential.",
        "7": "Marriage indicator. Love and commitment potential.",
        "8": "Passionate intimacy. Physical attraction.",
        "11": "Harmonious friendship and social compatibility.",
    },
    "Mars": {
        "1": "Energetic and dynamic interaction. Assertiveness is appreciated.",
        "5": "Passionate romance. Sexual chemistry and excitement.",
        "7": "Assertiveness in partnership. May need balance.",
        "8": "Intense passion and sexual chemistry.",
        "11": "Active partnership with shared pursuits.",
    }
}

ASPECT_INTERPRETATIONS = {
    "Conjunction": "Strong blending of planets. Intense connection.",
    "Sextile": "Harmonious flow. Easy compatibility and mutual support.",
    "Trine": "Natural ease and flow. Effortless compatibility.",
    "Square": "Tension and friction. Growth through challenge.",
    "Opposition": "Complementary but opposing. Requires understanding.",
}

HOUSE_INTERPRETATIONS = {
    1: "Physical attraction and first impressions",
    2: "Finances and values alignment",
    3: "Communication and intellect",
    4: "Family and domestic life",
    5: "Romance, creativity, and children",
    6: "Health, work, and daily life",
    7: "Marriage, partnership, and contracts",
    8: "Intimacy, secrets, and shared resources",
    9: "Philosophy, travel, and spirituality",
    10: "Career, reputation, and social status",
    11: "Friendship, groups, and hopes",
    12: "Spirituality, hidden matters, and privacy",
}

# ========== STRENGTH FACTORS ==========

def generate_strength_factors(compatibility_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate top compatibility strength factors"""
    factors = []

    # Extract highest scoring components
    overlay_score = compatibility_data.get("overlay_score", 0)
    house_score = compatibility_data.get("house_score", 0)
    aspect_score = compatibility_data.get("aspect_score", 0)

    if overlay_score > 70:
        factors.append({
            "factor_name": "Strong Planetary Overlays",
            "description": "Personal planets create harmonious interaction between your charts",
            "impact_score": overlay_score,
            "area_of_life": "Romance & Attraction"
        })

    if house_score > 60:
        factors.append({
            "factor_name": "Excellent House Compatibility",
            "description": "Sign and elemental harmony shows strong foundational compatibility",
            "impact_score": house_score,
            "area_of_life": "Daily Life & Harmony"
        })

    guna_score = compatibility_data.get("component_scores", {}).get("guna", {}).get("total_score", 0)
    if guna_score >= 28:
        factors.append({
            "factor_name": "Outstanding Guna Matching",
            "description": "Traditional 8-point matching shows exceptional harmony",
            "impact_score": guna_score,
            "area_of_life": "Overall Compatibility"
        })

    if aspect_score > 30:
        factors.append({
            "factor_name": "Harmonious Planetary Aspects",
            "description": "Multiple trine and sextile aspects create ease in relationship",
            "impact_score": aspect_score,
            "area_of_life": "Communication & Understanding"
        })

    return factors[:5]  # Top 5 factors


def generate_challenge_factors(compatibility_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate main compatibility challenges"""
    factors = []

    overlay_score = compatibility_data.get("overlay_score", 0)
    aspect_score = compatibility_data.get("aspect_score", 0)
    guna_score = compatibility_data.get("component_scores", {}).get("guna", {}).get("total_score", 0)

    if overlay_score < 30:
        factors.append({
            "factor_name": "Limited Planetary Overlap",
            "description": "Less natural attraction at first glance; requires time to develop",
            "severity": 40,
            "mitigation_strategies": [
                "Build emotional connection through communication",
                "Spend quality time together regularly",
                "Focus on shared interests and values"
            ]
        })

    if aspect_score < 10:
        factors.append({
            "factor_name": "Challenging Planetary Aspects",
            "description": "Square and opposition aspects create friction areas",
            "severity": 45,
            "mitigation_strategies": [
                "Practice patience and understanding",
                "Address conflicts early through communication",
                "Seek astrological remedies for difficult planets"
            ]
        })

    if guna_score < 14:
        factors.append({
            "factor_name": "Low Guna Compatibility",
            "description": "Traditional metrics show limited compatibility",
            "severity": 35,
            "mitigation_strategies": [
                "Perform pujas and remedial rituals",
                "Wear appropriate gemstones",
                "Seek guidance from experienced astrologer"
            ]
        })

    # Nadi incompatibility (worst match in traditional astrology)
    nadi_compatibility = compatibility_data.get("component_scores", {}).get("guna", {}).get("individual_scores", {}).get("Nadi", 0)
    if nadi_compatibility == 0:
        factors.append({
            "factor_name": "Nadi Incompatibility",
            "description": "Same Nadi (nervous system) may cause genetic/health incompatibility",
            "severity": 60,
            "mitigation_strategies": [
                "Consider medical consultation for genetic compatibility",
                "Perform Nadi Shanti puja (Nadi reconciliation ritual)",
                "Consult experienced Vedic astrologer for detailed analysis"
            ]
        })

    return factors[:5]


# ========== REMEDIES SUGGESTIONS ==========

def generate_remedies(compatibility_data: Dict[str, Any], relationship_type: str) -> List[Dict[str, Any]]:
    """Generate remedial suggestions based on compatibility analysis"""
    remedies = []

    compatibility_score = compatibility_data.get("compatibility_percentage", 50)

    # Gemstone recommendations
    if compatibility_score < 75:
        # Venus (love/attraction)
        remedies.append({
            "type": "Gemstone",
            "description": "Diamond or White Sapphire for Venus - enhances love and attraction",
            "target_planet": "Venus",
            "effectiveness": 75,
            "cost_level": "High",
            "finger": "Ring finger",
            "metal": "Silver or White Metal"
        })

        # Mars (passion, sexual chemistry)
        remedies.append({
            "type": "Gemstone",
            "description": "Red Coral for Mars - increases passion and sexual energy",
            "target_planet": "Mars",
            "effectiveness": 70,
            "cost_level": "Low",
            "finger": "Ring finger",
            "metal": "Copper or Gold"
        })

    # Jupiter for expansion and luck
    remedies.append({
        "type": "Gemstone",
        "description": "Yellow Sapphire for Jupiter - brings luck and expansion to relationship",
        "target_planet": "Jupiter",
        "effectiveness": 72,
        "cost_level": "Medium",
        "finger": "Index finger",
        "metal": "Gold"
    })

    # Saturn for stability (if there are Saturn issues)
    if compatibility_score < 60:
        remedies.append({
            "type": "Gemstone",
            "description": "Blue Sapphire for Saturn - brings discipline and longevity",
            "target_planet": "Saturn",
            "effectiveness": 65,
            "cost_level": "High",
            "finger": "Middle finger",
            "metal": "Silver or Iron"
        })

    # Mantra recommendations
    if relationship_type == "romantic":
        remedies.append({
            "type": "Mantra",
            "description": "Shukra Mantra (Venus): 'Om Shum Shukraya Namah' - 108 times daily",
            "target_planet": "Venus",
            "effectiveness": 68,
            "cost_level": "Free",
            "benefits": "Enhances love, attraction, and harmony"
        })

        remedies.append({
            "type": "Mantra",
            "description": "Mangal Mantra (Mars): 'Om Angarakaya Namah' - 108 times",
            "target_planet": "Mars",
            "effectiveness": 65,
            "cost_level": "Free",
            "benefits": "Increases passion and sexual chemistry"
        })

    # Ritual recommendations
    remedies.append({
        "type": "Ritual",
        "description": "Venus Puja - Perform on Fridays during Shukra hora",
        "target_planet": "Venus",
        "effectiveness": 70,
        "cost_level": "Medium",
        "frequency": "Monthly or on significant dates"
    })

    if compatibility_score < 65:
        remedies.append({
            "type": "Ritual",
            "description": "Nadi Shanti Puja - Reconciliation ritual for Nadi incompatibility",
            "target_planet": "All",
            "effectiveness": 80,
            "cost_level": "High",
            "when": "Before marriage or commitment"
        })

    remedies.append({
        "type": "Ritual",
        "description": "Chandika Havan - Harmony and prosperity ritual",
        "target_planet": "Moon/Mars",
        "effectiveness": 75,
        "cost_level": "Medium",
        "frequency": "Once during relationship milestone"
    })

    # General recommendations
    remedies.append({
        "type": "Lifestyle",
        "description": "Wearing yellow on Thursdays - amplifies Jupiter's blessings",
        "target_planet": "Jupiter",
        "effectiveness": 60,
        "cost_level": "Free"
    })

    remedies.append({
        "type": "Lifestyle",
        "description": "White color on Mondays - strengthens Moon connection",
        "target_planet": "Moon",
        "effectiveness": 55,
        "cost_level": "Free"
    })

    return remedies


# ========== TIMELINE AND PREDICTIONS ==========

def generate_relationship_timeline(compatibility_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate relationship timeline predictions"""
    score = compatibility_data.get("compatibility_percentage", 50)

    timeline = {
        "relationship_outlook": "",
        "critical_years": [],
        "auspicious_dates": [],
        "milestones": []
    }

    # Overall outlook
    if score >= 80:
        timeline["relationship_outlook"] = (
            "Exceptional marriage prospects. The charts indicate this is an ideal match with "
            "strong potential for lifelong happiness, mutual growth, and deep spiritual connection. "
            "You are likely soulmates or have significant karmic connection. Marriage is highly recommended."
        )
    elif score >= 65:
        timeline["relationship_outlook"] = (
            "Very good relationship prospects. The charts show strong compatibility with good potential "
            "for successful marriage. Some minor adjustments may be needed, but overall this is a "
            "favorable match with high success probability."
        )
    elif score >= 50:
        timeline["relationship_outlook"] = (
            "Positive prospects with effort. While compatibility is moderate, this relationship can "
            "be successful with mutual understanding, patience, and commitment. Some areas may require "
            "work, but growth together is possible."
        )
    else:
        timeline["relationship_outlook"] = (
            "Challenging but not impossible. This relationship requires significant effort, maturity, "
            "and spiritual growth from both partners. Consider astrological remedies and guidance before "
            "making major commitments. Success depends on willingness to work through differences."
        )

    # Critical years (simplified - based on Saturn/Rahu/Ketu periods)
    timeline["critical_years"] = [
        "2025-2027 (Saturn return considerations)",
        "2029-2031 (Rahu-Ketu transit)",
    ]

    # Auspicious dates (simplified)
    timeline["auspicious_dates"] = [
        "2025-12-15 (Full Moon - high energy)",
        "2026-01-20 (New Moon - new beginnings)",
        "2026-03-05 (Venus transit)",
        "2026-06-21 (Summer solstice)",
    ]

    # Milestones
    timeline["milestones"] = [
        {
            "period": "First 3 months",
            "focus": "Building emotional connection and communication",
            "expected_development": "Deep understanding of each other's needs and values"
        },
        {
            "period": "6-12 months",
            "focus": "Establishing trust and commitment",
            "expected_development": "Decision point for long-term commitment"
        },
        {
            "period": "1-2 years",
            "focus": "Integration into each other's lives",
            "expected_development": "Meeting family and creating shared future plans"
        },
        {
            "period": "2-5 years",
            "focus": "Building lasting foundation",
            "expected_development": "Marriage or long-term commitment if mutually desired"
        }
    ]

    return timeline


# ========== LIFE AREA PREDICTIONS ==========

def generate_life_area_predictions(compatibility_data: Dict[str, Any], relationship_type: str) -> List[Dict[str, Any]]:
    """Generate predictions for specific life areas affected by relationship"""
    score = compatibility_data.get("compatibility_percentage", 50)
    predictions = []

    # Career
    guna_data = compatibility_data.get("component_scores", {}).get("guna", {})
    sun_guna = guna_data.get("individual_scores", {}).get("Varna", 0)
    career_score = min(100, ((sun_guna / 6) * 100) if sun_guna else score)
    predictions.append({
        "area": "Career",
        "score": career_score,
        "prediction": "Mutual professional support and growth" if career_score >= 70 else "Career discussions needed",
        "strengths": ["Supportive partner", "Shared ambitions"] if career_score >= 70 else ["Independent goals"],
        "challenges": ["Career priority conflicts"] if career_score < 70 else [],
        "timing": "Best period: Q1 & Q3 for joint ventures",
        "remedies": ["Sun worship on Sundays", "Career advancement mantras", "Saturn remedies for stability"]
    })

    # Finance
    predictions.append({
        "area": "Finance",
        "score": min(100, score if score >= 70 else score - 10),
        "prediction": "Combined prosperity and wealth growth" if score >= 70 else "Financial boundaries needed",
        "strengths": ["Joint investments", "Complementary financial strengths"] if score >= 70 else ["Separate finances better"],
        "challenges": ["Money disputes", "Different spending habits"] if score < 70 else [],
        "timing": "Best period: During Jupiter transits (next: Q2-Q3 2025)",
        "remedies": ["Jupiter mantras on Thursdays", "Yellow sapphire gemstone", "Charity and giving practices"]
    })

    # Health
    predictions.append({
        "area": "Health",
        "score": min(100, score if score >= 75 else score - 8),
        "prediction": "Positive wellness and emotional support" if score >= 75 else "Monitor stress and health practices",
        "strengths": ["Emotional support system", "Wellness partnership"] if score >= 75 else ["Self-care important"],
        "challenges": ["Relationship stress affecting health"] if score < 75 else [],
        "timing": "Critical care periods: During challenging transits",
        "remedies": ["Moon rituals on Mondays", "Health meditation practices", "Healing together activities"]
    })

    # Children
    vasya_guna = guna_data.get("individual_scores", {}).get("Vasya", 0)
    children_score = min(100, ((vasya_guna / 6) * 100) if vasya_guna else score)
    predictions.append({
        "area": "Children",
        "score": children_score,
        "prediction": "Healthy progeny and strong family bonds" if children_score >= 75 else "Parenting harmony needed",
        "strengths": ["Nurturing environment", "Aligned parenting values"] if children_score >= 75 else [],
        "challenges": ["Different parenting approaches", "Fertility concerns"] if children_score < 75 else [],
        "timing": "Best conception period: Aligned planetary transits (consult for specific dates)",
        "remedies": ["Jupiter and Venus rituals", "5th house strengthening practices", "Fertility blessings puja"]
    })

    # Spiritual
    predictions.append({
        "area": "Spiritual",
        "score": min(100, score),
        "prediction": f"Spiritual growth and soul connection at {score}% compatibility",
        "strengths": ["Soul recognition", "Life lessons together", "Shared spiritual path"],
        "challenges": [],
        "timing": "Lifelong journey with deepening connection",
        "remedies": ["Meditation together", "Spiritual practice alignment", "Healing rituals for past karma"]
    })

    return predictions


# ========== RELATIONSHIP SPECIFIC ADVICE ==========

RELATIONSHIP_TYPE_ADVICE = {
    "romantic": {
        "focus_areas": ["Love and attraction", "Emotional intimacy", "Sexual chemistry", "Long-term commitment"],
        "key_metrics": ["Venus placement", "Mars placement", "Guna Milan", "Moon harmony"],
        "common_challenges": [
            "Varying love languages",
            "Different emotional needs",
            "Sexual compatibility",
            "Commitment timelines"
        ],
        "success_factors": [
            "Open communication about feelings",
            "Physical affection and touch",
            "Quality time together",
            "Shared dreams and future vision"
        ]
    },
    "business": {
        "focus_areas": ["Trust and integrity", "Work style compatibility", "Financial alignment", "Decision-making"],
        "key_metrics": ["Mercury compatibility", "Jupiter expansion", "Saturn structure", "House overlays"],
        "common_challenges": [
            "Different work styles",
            "Financial disagreement",
            "Decision-making conflicts",
            "Work-life balance"
        ],
        "success_factors": [
            "Clear written agreements",
            "Defined roles and responsibilities",
            "Regular financial reviews",
            "Professional communication"
        ]
    },
    "friendship": {
        "focus_areas": ["Shared interests", "Loyalty", "Support", "Fun and enjoyment"],
        "key_metrics": ["Jupiter placement", "11th house overlays", "Mercury communication", "Moon comfort"],
        "common_challenges": [
            "Growing apart over time",
            "Different priorities",
            "Unmet expectations",
            "Conflict resolution"
        ],
        "success_factors": [
            "Regular quality time",
            "Honest communication",
            "Accepting differences",
            "Supporting each other's growth"
        ]
    },
    "family": {
        "focus_areas": ["Family ties", "Duty and obligation", "Harmony", "Heritage and values"],
        "key_metrics": ["Moon placement", "4th house overlays", "Saturn karma", "Family patterns"],
        "common_challenges": [
            "Generational differences",
            "Family expectations",
            "Cultural differences",
            "Inherited patterns"
        ],
        "success_factors": [
            "Respect for family values",
            "Clear boundaries with extended family",
            "Honoring traditions while creating new ones",
            "Healing family patterns"
        ]
    }
}


def get_relationship_advice(relationship_type: str) -> Dict[str, Any]:
    """Get specific advice for relationship type"""
    return RELATIONSHIP_TYPE_ADVICE.get(relationship_type, RELATIONSHIP_TYPE_ADVICE["romantic"])
