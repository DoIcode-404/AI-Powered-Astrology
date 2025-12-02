"""
Horoscope Generation Service
Generates daily, weekly, and monthly horoscopes for all 12 zodiac signs.
Uses transit data and Vedic astrology rules.
"""

import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)

# Zodiac signs order
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Life areas
LIFE_AREAS = [
    "love", "career", "finance", "health", "family",
    "travel", "spirituality", "luck", "challenges"
]

# Element mapping
ELEMENT_MAP = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water",
}

# Ruling planets
RULING_PLANETS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Lucky elements for each sign
LUCKY_ELEMENTS = {
    "Aries": {"color": "Red", "number": 9, "direction": "South"},
    "Taurus": {"color": "Green", "number": 6, "direction": "North"},
    "Gemini": {"color": "Yellow", "number": 5, "direction": "East"},
    "Cancer": {"color": "White", "number": 2, "direction": "North"},
    "Leo": {"color": "Gold", "number": 1, "direction": "East"},
    "Virgo": {"color": "Green", "number": 5, "direction": "West"},
    "Libra": {"color": "Blue", "number": 6, "direction": "West"},
    "Scorpio": {"color": "Red", "number": 8, "direction": "South"},
    "Sagittarius": {"color": "Orange", "number": 3, "direction": "South"},
    "Capricorn": {"color": "Blue", "number": 8, "direction": "West"},
    "Aquarius": {"color": "Purple", "number": 7, "direction": "North"},
    "Pisces": {"color": "Green", "number": 3, "direction": "East"},
}


class HoroscopeType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class HoroscopeService:
    """Service for generating zodiac horoscopes"""

    def __init__(self, transit_calculator=None):
        self.transit_calculator = transit_calculator

    # ========== DAILY HOROSCOPE ==========

    def generate_daily_horoscope(self, zodiac_sign: str, target_date: date) -> Dict[str, Any]:
        """
        Generate daily horoscope for zodiac sign.

        Args:
            zodiac_sign: Zodiac sign name (e.g., "Aries")
            target_date: Date for horoscope (defaults to today)

        Returns:
            Complete daily horoscope with all 9 life areas
        """
        if zodiac_sign not in ZODIAC_SIGNS:
            raise ValueError(f"Invalid zodiac sign: {zodiac_sign}")

        # Calculate life area scores for this date
        life_area_scores = self._calculate_daily_life_area_scores(zodiac_sign, target_date)

        # Overall energy and theme
        overall_energy = sum(life_area_scores.values()) / len(life_area_scores)
        overall_theme = self._determine_theme(overall_energy)

        # Generate interpretations
        life_area_predictions = self._generate_life_area_predictions(
            zodiac_sign, life_area_scores, HoroscopeType.DAILY
        )

        # Lunar phase effect
        lunar_phase = self._get_lunar_phase(target_date)
        lunar_impact = self._calculate_lunar_impact(lunar_phase, zodiac_sign)

        # Cautions and affirmations
        cautions = self._generate_cautions(zodiac_sign, life_area_scores)
        affirmations = self._generate_affirmations(zodiac_sign)

        # Lucky elements
        lucky = LUCKY_ELEMENTS.get(zodiac_sign, {})

        return {
            "horoscope_type": HoroscopeType.DAILY.value,
            "zodiac_sign": zodiac_sign,
            "date": target_date.isoformat(),
            "valid_until": (target_date + timedelta(days=1)).isoformat(),

            # Overall assessment
            "overall_energy": round(overall_energy, 2),
            "overall_theme": overall_theme,

            # Life areas
            "life_areas": self._format_life_areas(life_area_scores, zodiac_sign),

            # Lucky elements
            "lucky_color": lucky.get("color", ""),
            "lucky_number": lucky.get("number", 0),
            "lucky_direction": lucky.get("direction", ""),
            "lucky_time": self._get_lucky_time(zodiac_sign),

            # Detailed predictions
            "predictions": life_area_predictions,

            # Lunar info
            "lunar_phase": lunar_phase,
            "lunar_impact": lunar_impact,

            # Cautions and affirmations
            "cautions": cautions,
            "affirmations": affirmations,

            # Metadata
            "generated_at": datetime.utcnow().isoformat(),
            "cache_expires_at": (datetime.utcnow() + timedelta(days=1)).isoformat()
        }

    def _calculate_daily_life_area_scores(self, zodiac_sign: str, target_date: date) -> Dict[str, float]:
        """Calculate scores for all 9 life areas"""
        scores = {}

        # Base scores for each area
        base_scores = {
            "love": 50,
            "career": 50,
            "finance": 50,
            "health": 50,
            "family": 50,
            "travel": 50,
            "spirituality": 50,
            "luck": 50,
            "challenges": 50,
        }

        ruling_planet = RULING_PLANETS.get(zodiac_sign, "Moon")
        element = ELEMENT_MAP.get(zodiac_sign, "Fire")

        # Simulate transit effects (simplified)
        day_of_week = target_date.weekday()  # 0=Monday, 6=Sunday

        # Day-of-week effects
        day_effects = {
            "love": [5, 8, 10, 12, 15, 12, 10],  # Mon-Sun
            "career": [12, 14, 16, 10, 18, 8, 6],
            "finance": [6, 8, 10, 12, 14, 10, 8],
            "health": [8, 10, 12, 14, 12, 10, 8],
            "family": [10, 12, 14, 16, 14, 12, 10],
            "travel": [8, 10, 12, 14, 16, 18, 10],
            "spirituality": [10, 8, 10, 12, 10, 14, 16],
            "luck": [6, 8, 10, 12, 14, 16, 12],
            "challenges": [-5, -8, -10, -6, -4, -8, -6],
        }

        # Apply day-of-week effects
        for area in LIFE_AREAS:
            if area in day_effects:
                effect = day_effects[area][day_of_week] if day_of_week < 7 else 0
                scores[area] = min(100, max(0, base_scores[area] + effect))
            else:
                scores[area] = base_scores[area]

        # Lunar phase effect
        lunar_bonus = self._calculate_lunar_effect(target_date)
        scores["luck"] = min(100, max(0, scores["luck"] + lunar_bonus))

        # Element-specific bonuses
        if element == "Fire":
            scores["energy"] = min(100, scores.get("energy", 50) + 10)
            scores["career"] = min(100, max(0, scores["career"] + 5))
        elif element == "Water":
            scores["love"] = min(100, max(0, scores["love"] + 8))
            scores["spirituality"] = min(100, max(0, scores["spirituality"] + 10))
        elif element == "Air":
            scores["communication"] = min(100, scores.get("communication", 50) + 12)
            scores["travel"] = min(100, max(0, scores["travel"] + 8))
        elif element == "Earth":
            scores["finance"] = min(100, max(0, scores["finance"] + 10))
            scores["health"] = min(100, max(0, scores["health"] + 8))

        return scores

    # ========== WEEKLY HOROSCOPE ==========

    def generate_weekly_horoscope(self, zodiac_sign: str, week_start: date = None) -> Dict[str, Any]:
        """
        Generate weekly horoscope for zodiac sign.

        Args:
            zodiac_sign: Zodiac sign name
            week_start: Monday of the week (defaults to current week)

        Returns:
            Weekly horoscope with daily breakdown
        """
        if week_start is None:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())

        # Generate daily horoscopes for the week
        daily_horoscopes = []
        daily_energies = []

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for i in range(7):
            day = week_start + timedelta(days=i)
            daily = self.generate_daily_horoscope(zodiac_sign, day)

            daily_horoscopes.append({
                "day": day_names[i],
                "energy": daily["overall_energy"],
                "theme": daily["overall_theme"],
                "summary": daily["predictions"][0]["detailed_prediction"] if daily["predictions"] else ""
            })

            daily_energies.append(daily["overall_energy"])

        # Weekly aggregates
        weekly_energy = sum(daily_energies) / len(daily_energies)

        # Generate weekly forecast text
        weekly_forecast = self._generate_weekly_forecast(zodiac_sign, weekly_energy, daily_horoscopes)

        # Aggregate life area scores
        weekly_life_areas = self._aggregate_weekly_life_areas(zodiac_sign, week_start)

        return {
            "horoscope_type": HoroscopeType.WEEKLY.value,
            "zodiac_sign": zodiac_sign,
            "week": week_start.strftime("%Y-W%W"),
            "start_date": week_start.isoformat(),
            "end_date": (week_start + timedelta(days=6)).isoformat(),

            # Overall assessment
            "overall_energy": round(weekly_energy, 2),
            "overall_theme": self._determine_theme(weekly_energy),

            # Daily breakdown
            "daily_breakdown": daily_horoscopes,

            # Weekly aggregates
            "life_areas": weekly_life_areas,

            # Forecast
            "week_forecast": weekly_forecast,

            # Lucky elements
            "lucky_elements": LUCKY_ELEMENTS.get(zodiac_sign, {}),

            # Metadata
            "generated_at": datetime.utcnow().isoformat(),
            "cache_expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat()
        }

    # ========== MONTHLY HOROSCOPE ==========

    def generate_monthly_horoscope(self, zodiac_sign: str, year_month: str = None) -> Dict[str, Any]:
        """
        Generate monthly horoscope for zodiac sign.

        Args:
            zodiac_sign: Zodiac sign name
            year_month: Year-month string (YYYY-MM), defaults to current month

        Returns:
            Monthly horoscope with week summaries and key dates
        """
        if year_month is None:
            today = date.today()
            year_month = today.strftime("%Y-%m")

        year, month = map(int, year_month.split("-"))
        month_start = date(year, month, 1)

        # Get last day of month
        if month == 12:
            month_end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(year, month + 1, 1) - timedelta(days=1)

        # Generate weekly summaries
        week_summaries = []
        month_energies = []

        current_date = month_start
        week_num = 1

        while current_date <= month_end:
            week_start = current_date - timedelta(days=current_date.weekday())
            week_end = week_start + timedelta(days=6)

            # Calculate average energy for the week
            week_energies = []
            while current_date <= min(week_end, month_end):
                daily = self.generate_daily_horoscope(zodiac_sign, current_date)
                week_energies.append(daily["overall_energy"])
                current_date += timedelta(days=1)

            week_energy = sum(week_energies) / len(week_energies) if week_energies else 50
            month_energies.extend(week_energies)

            week_summaries.append({
                "week": week_num,
                "energy": round(week_energy, 2),
                "theme": self._determine_theme(week_energy),
                "summary": f"This week brings {self._determine_theme(week_energy).lower()} influences"
            })

            week_num += 1

        # Monthly aggregate
        monthly_energy = sum(month_energies) / len(month_energies) if month_energies else 50

        # Key astronomical dates
        key_dates = self._get_key_dates_for_month(year, month, zodiac_sign)

        # Monthly forecast
        monthly_forecast = self._generate_monthly_forecast(zodiac_sign, monthly_energy)

        # Aggregate life areas
        monthly_life_areas = self._aggregate_monthly_life_areas(zodiac_sign, month_start)

        return {
            "horoscope_type": HoroscopeType.MONTHLY.value,
            "zodiac_sign": zodiac_sign,
            "month": year_month,
            "start_date": month_start.isoformat(),
            "end_date": month_end.isoformat(),

            # Overall assessment
            "overall_energy": round(monthly_energy, 2),
            "overall_theme": self._determine_theme(monthly_energy),

            # Week summaries
            "week_summaries": week_summaries,

            # Life areas
            "life_areas": monthly_life_areas,

            # Key dates
            "key_dates": key_dates,

            # Forecast
            "month_forecast": monthly_forecast,

            # Lucky elements
            "lucky_elements": LUCKY_ELEMENTS.get(zodiac_sign, {}),

            # Metadata
            "generated_at": datetime.utcnow().isoformat(),
            "cache_expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }

    # ========== HELPER METHODS ==========

    def _calculate_lunar_effect(self, target_date: date) -> float:
        """Calculate lunar phase effect on horoscope"""
        # Simplified lunar calculation
        day_of_month = target_date.day

        if day_of_month < 8:
            return 15  # Waxing crescent - building energy
        elif day_of_month < 15:
            return 20  # Waxing gibbous - strongest
        elif day_of_month < 23:
            return 10  # Waning - releasing energy
        else:
            return 5  # Dark moon - introspective

    def _get_lunar_phase(self, target_date: date) -> str:
        """Get lunar phase name"""
        day_of_month = target_date.day

        if day_of_month < 8:
            return "Waxing Crescent"
        elif day_of_month == 8 or day_of_month == 15:
            return "First/Full Quarter"
        elif day_of_month < 15:
            return "Waxing Gibbous"
        elif day_of_month < 23:
            return "Waning Gibbous"
        elif day_of_month == 23:
            return "Last Quarter"
        else:
            return "Dark Moon"

    def _calculate_lunar_impact(self, lunar_phase: str, zodiac_sign: str) -> str:
        """Generate description of lunar impact"""
        water_signs = ["Cancer", "Scorpio", "Pisces"]

        if "Waxing" in lunar_phase:
            impact = "Energetic. Good for starting new ventures and projects."
        elif "Full" in lunar_phase:
            impact = "Peak energy. Culminations and revelations. Full clarity."
        elif "Waning" in lunar_phase:
            impact = "Releasing energy. Good for completion and letting go."
        else:
            impact = "Introspective. Good for rest and inner work."

        if zodiac_sign in water_signs:
            impact += " Extra sensitivity to lunar changes."

        return impact

    def _determine_theme(self, overall_energy: float) -> str:
        """Determine overall theme based on energy"""
        if overall_energy >= 85:
            return "Excellent"
        elif overall_energy >= 70:
            return "Very Good"
        elif overall_energy >= 55:
            return "Favorable"
        elif overall_energy >= 40:
            return "Neutral"
        elif overall_energy >= 25:
            return "Challenging"
        else:
            return "Difficult"

    def _generate_life_area_predictions(self, zodiac_sign: str, scores: Dict[str, float], horo_type: HoroscopeType) -> List[Dict[str, Any]]:
        """Generate detailed life area predictions"""
        predictions = []

        for area in LIFE_AREAS:
            score = scores.get(area, 50)
            grade = self._score_to_grade(score)

            prediction = {
                "life_area": area,
                "score": round(score, 2),
                "grade": grade,
                "headline": self._generate_area_headline(area, score, zodiac_sign),
                "detailed_prediction": self._generate_area_prediction(area, score, zodiac_sign, horo_type),
                "advice": self._generate_area_advice(area, score),
            }
            predictions.append(prediction)

        return predictions

    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

    def _generate_area_headline(self, area: str, score: float, zodiac_sign: str) -> str:
        """Generate one-line headline for life area"""
        templates = {
            "love": ["Romance is flourishing", "Love needs attention", "Emotional bonds strengthen"],
            "career": ["Professional growth ahead", "Career stability", "Work challenges emerge"],
            "finance": ["Financial gains possible", "Budget wisely", "Investment opportunities"],
            "health": ["Vitality and wellness", "Rest is important", "Health needs focus"],
            "family": ["Family harmony", "Family discussions needed", "Strong support available"],
            "travel": ["Travel looks promising", "Local activities recommended", "Adventure awaits"],
            "spirituality": ["Spiritual awakening", "Inner work deepens", "Higher consciousness calls"],
            "luck": ["Fortune smiles on you", "Caution advised", "Mixed blessings"],
            "challenges": ["Growth through challenges", "Minor obstacles", "Significant test ahead"],
        }

        if score >= 75:
            return templates.get(area, ["Good times ahead"])[0]
        elif score >= 50:
            return templates.get(area, ["Neutral energy"])[1]
        else:
            return templates.get(area, ["Challenges ahead"])[2]

    def _generate_area_prediction(self, area: str, score: float, zodiac_sign: str, horo_type: HoroscopeType) -> str:
        """Generate detailed prediction for life area"""
        ruling_planet = RULING_PLANETS.get(zodiac_sign, "Moon")

        if score >= 75:
            return f"This is a highly favorable period for {area}. {ruling_planet}'s influence brings opportunities and positive developments. Make the most of this auspicious time."
        elif score >= 50:
            return f"{area.capitalize()} shows mixed influences. While opportunities exist, patience and careful planning are recommended. Stay balanced and focused."
        else:
            return f"Challenges in {area} require your attention. Consider seeking guidance or taking preventive measures. This too shall pass."

    def _generate_area_advice(self, area: str, score: float) -> str:
        """Generate practical advice for life area"""
        if score >= 75:
            return "Take action on your goals. This is the perfect time."
        elif score >= 50:
            return "Proceed with balanced caution. Gather information before major decisions."
        else:
            return "Focus on protection and stability. Avoid major changes if possible."

    def _format_life_areas(self, scores: Dict[str, float], zodiac_sign: str) -> Dict[str, Any]:
        """Format life areas for response"""
        formatted = {}

        for area in LIFE_AREAS:
            score = scores.get(area, 50)
            formatted[area] = {
                "score": round(score, 2),
                "grade": self._score_to_grade(score),
                "headline": self._generate_area_headline(area, score, zodiac_sign),
            }

        return formatted

    def _generate_cautions(self, zodiac_sign: str, scores: Dict[str, float]) -> List[str]:
        """Generate cautions/warnings for the day"""
        cautions = []

        if scores.get("challenges", 50) > 70:
            cautions.append("Be cautious in decision-making today")

        if scores.get("health", 50) < 40:
            cautions.append("Prioritize rest and self-care")

        if scores.get("finance", 50) < 35:
            cautions.append("Avoid major financial decisions")

        if scores.get("love", 50) > 80:
            cautions.append("Be mindful of heightened emotions")

        return cautions if cautions else ["Stay grounded and centered"]

    def _generate_affirmations(self, zodiac_sign: str) -> List[str]:
        """Generate daily affirmations"""
        affirmations = {
            "Aries": ["I am courageous and capable", "I lead with confidence", "I manifest my desires"],
            "Taurus": ["I am stable and secure", "I attract abundance", "I am grounded"],
            "Gemini": ["I communicate with clarity", "I am adaptable", "Knowledge flows to me"],
            "Cancer": ["I am emotionally resilient", "My heart is strong", "I nurture myself"],
            "Leo": ["I am radiant and authentic", "I shine brightly", "I am worthy of love"],
            "Virgo": ["I am organized and capable", "I serve with purpose", "I am whole"],
            "Libra": ["I attract harmony", "I balance with grace", "I choose wisely"],
            "Scorpio": ["I am powerful and transforming", "I trust my intuition", "I am reborn"],
            "Sagittarius": ["I am free and expansive", "Truth guides me", "I am fortunate"],
            "Capricorn": ["I am ambitious and disciplined", "I achieve my goals", "I am successful"],
            "Aquarius": ["I am innovative and free", "I embrace change", "I am unique"],
            "Pisces": ["I am intuitive and compassionate", "I flow with grace", "I am spiritual"],
        }

        return affirmations.get(zodiac_sign, ["I am whole and complete"])

    def _get_lucky_time(self, zodiac_sign: str) -> str:
        """Get lucky time of day"""
        ruling_planet = RULING_PLANETS.get(zodiac_sign, "Moon")

        if ruling_planet in ["Sun", "Mars", "Jupiter"]:
            return "Morning (6am-10am)"
        elif ruling_planet in ["Moon"]:
            return "Evening (6pm-9pm)"
        else:
            return "Midday (10am-3pm)"

    def _generate_weekly_forecast(self, zodiac_sign: str, energy: float, daily_breakdown: List) -> str:
        """Generate weekly forecast text"""
        if energy >= 75:
            return f"An excellent week ahead for {zodiac_sign}. Multiple positive influences create momentum. This is a time for taking action and pursuing your goals."
        elif energy >= 55:
            return f"A mixed week with both opportunities and challenges. Stay adaptable and focus on what you can control. Progress is possible with conscious effort."
        else:
            return f"A challenging week that calls for patience and perseverance. Use this time for inner work and preparation. Better times are coming."

    def _generate_monthly_forecast(self, zodiac_sign: str, energy: float) -> str:
        """Generate monthly forecast text"""
        if energy >= 75:
            return f"A transformative month for {zodiac_sign}. Significant growth and positive developments are likely. Seize the opportunities that arise."
        elif energy >= 55:
            return f"A productive month with mixed influences. Balance activity with reflection. This month brings lessons and growth."
        else:
            return f"A challenging month requiring resilience. Focus on what supports you. Use this period for inner development and preparation for better times."

    def _aggregate_weekly_life_areas(self, zodiac_sign: str, week_start: date) -> Dict[str, Any]:
        """Aggregate life area scores for the week"""
        aggregated = {area: [] for area in LIFE_AREAS}

        for i in range(7):
            day = week_start + timedelta(days=i)
            daily = self.generate_daily_horoscope(zodiac_sign, day)

            for area in LIFE_AREAS:
                if area in daily["life_areas"]:
                    aggregated[area].append(daily["life_areas"][area]["score"])

        formatted = {}
        for area in LIFE_AREAS:
            if aggregated[area]:
                avg_score = sum(aggregated[area]) / len(aggregated[area])
                formatted[area] = {
                    "score": round(avg_score, 2),
                    "grade": self._score_to_grade(avg_score),
                }

        return formatted

    def _aggregate_monthly_life_areas(self, zodiac_sign: str, month_start: date) -> Dict[str, Any]:
        """Aggregate life area scores for the month"""
        aggregated = {area: [] for area in LIFE_AREAS}

        # Get last day of month
        if month_start.month == 12:
            month_end = date(month_start.year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(month_start.year, month_start.month + 1, 1) - timedelta(days=1)

        current_date = month_start
        while current_date <= month_end:
            daily = self.generate_daily_horoscope(zodiac_sign, current_date)

            for area in LIFE_AREAS:
                if area in daily["life_areas"]:
                    aggregated[area].append(daily["life_areas"][area]["score"])

            current_date += timedelta(days=1)

        formatted = {}
        for area in LIFE_AREAS:
            if aggregated[area]:
                avg_score = sum(aggregated[area]) / len(aggregated[area])
                formatted[area] = {
                    "score": round(avg_score, 2),
                    "grade": self._score_to_grade(avg_score),
                }

        return formatted

    def _get_key_dates_for_month(self, year: int, month: int, zodiac_sign: str) -> List[Dict[str, Any]]:
        """Get key astronomical dates for the month"""
        # Simplified - would integrate with actual astronomical calendar in production
        return [
            {
                "date": f"{year}-{month:02d}-05",
                "event": "New Moon",
                "impact": "High - New beginnings and fresh starts",
                "advice": f"Perfect time for {zodiac_sign} to set intentions"
            },
            {
                "date": f"{year}-{month:02d}-20",
                "event": "Full Moon",
                "impact": "High - Culminations and revelations",
                "advice": "Complete projects and celebrate achievements"
            }
        ]
