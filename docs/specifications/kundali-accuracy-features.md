# Kundali Accuracy Features - Complete Specification

This document defines all the astrological features and calculations that go into generating accurate Kundali birth charts.

**Total Data Points Per Kundali:** 500+ calculated values

---

## CORE ASTRONOMICAL DATA

### Birth Input Features
- Birth Year, Month, Day
- Birth Hour, Minute
- Birth Latitude, Longitude
- Birth Timezone
- Julian Day (JD) Calculation

---

## PLANETARY POSITIONS (9 Celestial Bodies)

### Planets Tracked
Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu (North Node), Ketu (South Node)

### Per-Planet Features
- Longitude (degrees)
- Tropical & Sidereal Longitude
- Sign Position (1-12)
- Degree in Sign (0-30)
- Nakshatra (27 lunar mansions)
- Pada (quarter within nakshatra)
- House Position (1-12)
- Retrograde Status, Combustion Status
- Planetary Speed

---

## ASCENDANT (Lagna) - CRITICAL FOR ACCURACY

### Ascendant Features
- Ascendant Degree (0-360°)
- Ascendant Sign (1-12)
- Ascendant Nakshatra
- Ascendant Pada
- House Index (1-12)

### Calculation Components
- Latitude, Longitude, Julian Day
- Ephemeris Data (SwissEphemeris)

---

## HOUSE SYSTEM (12 Houses)

### Per-House Features (1-12)
- House Sign & Sign Number
- Planets in House
- Planet Count, Empty Status
- House Lord (ruling planet)

### House Significances
- House 1: Self, Personality, Health
- House 2: Wealth, Family, Speech
- House 3: Siblings, Communication
- House 4: Home, Mother, Property
- House 5: Children, Creativity, Romance
- House 6: Enemies, Diseases, Service
- House 7: Marriage, Partnership
- House 8: Transformation, Inheritance
- House 9: Luck, Dharma, Education
- House 10: Career, Reputation
- House 11: Gains, Friends, Income
- House 12: Losses, Spirituality, Moksha

---

## DASHA SYSTEM (Vimshottari - 120-Year Life Cycle)

### Dasha Components
- Current Maha Dasha (Major Period)
- Bhukti/Antar Dasha (Sub-Period)
- Start & End Dates, Duration Remaining
- Progression Percentage
- Interpretations & Predictions

### Dasha Periods (9 Planets)
- Ketu: 7 years
- Venus: 20 years
- Sun: 6 years
- Moon: 10 years
- Mars: 7 years
- Rahu: 18 years
- Jupiter: 16 years
- Saturn: 19 years
- Mercury: 17 years

---

## PLANETARY STRENGTHS (Shad Bala - 6 Measures)

### 1. Sthana Bala (Positional Strength)
House position, Sign position, Exaltation/Debilitation, Own sign, Vargottama status

### 2. Dig Bala (Directional Strength)
- East: Sun, Mercury, Jupiter
- South: Mars, Venus
- West: Saturn, Rahu
- North: Moon

### 3. Kala Bala (Temporal Strength)
Weekday status, Hora, Var, Masa, Ayana, Ayanadaya

### 4. Chesta Bala (Motion Strength)
Planet speed, Retrograde status, Directional status, Acceleration/Deceleration

### 5. Naisargika Bala (Natural Strength)
Jupiter: 60, Venus: 52, Mercury: 52, Moon: 51, Mars: 17, Sun: 12, Saturn: 10

### 6. Drishti Bala (Aspect Strength)
Aspects received, Type, Strength (0-100%), Orb, Applying/Separating status

### Dignity Levels
Exalted, Own Sign, Neutral, Debilitated

---

## PLANETARY ASPECTS (Inter-Planetary Relationships)

### Aspects Tracked
- Conjunction (0°)
- Sextile (60°)
- Square (90°)
- Trine (120°)
- Opposition (180°)

### Per-Aspect Data
- Aspected planet, Type, Orb
- Exact degree difference
- Applying status, Strength (0-100%)

---

## DIVISIONAL CHARTS (Vargas)

### D1 - Rasi Chart (Main birth chart)
Planet positions in 12 signs, House divisions, Ascendant

### D2 - Hora Chart (Wealth/Finances)
Each sign divided into 2 parts, Financial strength assessment

### D7 - Saptamsha Chart (Children)
Each sign divided into 7 parts, Children and fertility analysis

### D9 - Navamsha Chart (Spouse/Destiny)
Each sign divided into 9 parts, Partnership and life path, D1-D9 alignment

---

## YOGAS (Auspicious Combinations)

### Yoga Types Identified
- Raj Yoga (Kendra and Trikona lords together)
- Conjunction Yoga (2+ planets in same house)
- Benefic Yoga, Malefic Yoga

### Yoga Properties
- Name, House location, Planets involved
- Strength (0-100%), Benefic/Malefic classification

---

## SPECIAL FEATURES

### Moon & Ruling Planet
Moon sign, Nakshatra, Degree, House, Ruling planet (Chandra Rashi Lord)

### Sun Sign
Sun sign (tropical zodiac), Degree, House

### Chart Patterns
- Stellium (Planets in 4 houses)
- Scattered (10+ houses)
- Balanced (normal distribution)

### Elemental Analysis
Fire, Earth, Air, Water element counts and dominant element

### Quality Analysis
Cardinal, Fixed, Mutable quality counts

### Hemisphere Emphasis
Eastern, Western, Northern, Southern hemisphere distributions

---

## NATURAL SIGNIFICANCES

| Planet | Significances |
|--------|------------------|
| **Sun** | Soul, Self, Father, Government, Authority, Vitality |
| **Moon** | Mind, Mother, Emotions, Public, Water, Nurturing |
| **Mars** | Energy, Courage, Siblings, Property, Surgery, Sports |
| **Mercury** | Communication, Intelligence, Business, Education, Writing |
| **Jupiter** | Wisdom, Teacher, Children, Spirituality, Expansion, Luck |
| **Venus** | Love, Beauty, Arts, Luxury, Relationships, Creativity |
| **Saturn** | Discipline, Delays, Karma, Hardwork, Service, Longevity |
| **Rahu** | Illusion, Foreign, Technology, Sudden Events |
| **Ketu** | Spirituality, Detachment, Past Life, Moksha |

---

## ML FEATURES GENERATED (53+ Features)

### Birth Details Features (9)
Birth year, month, day, hour, minute, latitude, longitude, timezone, Julian day

### Ascendant Features (6)
Degree, sign, sign number, nakshatra, pada, lord

### Planet Features (72)
9 planets × 8 features: longitude, sign, sign_number, house, nakshatra, pada, degree_in_sign, dignity

### House Features (48)
12 houses × 4 features: house sign, sign_number, planets in house, planet count

### Aspect Features (10-15)
Per-planet aspect count, aspect details (planet, type, strength)

### Yoga Features (3)
Total yogas, benefic yogas, malefic yogas

### Special Features (7)
Moon sign, sun sign, ruling planet, chart pattern, dominant element, dominant quality, hemisphere emphasis

### Additional Features
House lord strengths (12), Aspect strength matrix

---

## ACCURACY CALCULATION METHODS

### Ephemeris-Based Calculations
- Julian Day calculation from birth date/time
- Planetary position calculations (tropical + sidereal)
- Ayanamsa correction (Lahiri system)
- Ascendant/MC & House cusps calculation (Placidus system)

### Astrological Rules Applied
- Dignities (Exalted, Own Sign, Neutral, Debilitated)
- Combustion checking (within X degrees of Sun)
- House lordship assignment
- Aspect orb tolerance (8 degrees)
- Nakshatra assignments (360° ÷ 27 = 13.33° per nakshatra)

### Mathematical Precision
- Sidereal positions normalized to 0-360°
- Degree/minute/second calculations
- Fractional degree support
- Accurate UTC time conversion

---

## ACCURACY FACTORS SUMMARY

| Factor | Count | Impact |
|--------|-------|--------|
| Planets Analyzed | 9 | High |
| Houses Analyzed | 12 | High |
| Nakshatras | 27 | High |
| Zodiac Signs | 12 | High |
| Dasha Periods | 9 | Very High |
| Strength Measures | 6 | Very High |
| Divisional Charts | 4 | High |
| Aspect Types | 5 | Medium |
| Elemental Categories | 4 | Medium |
| Quality Categories | 3 | Medium |
| Hemisphere Quadrants | 4 | Medium |
| **ML Features** | **53+** | **High** |

---

## CALCULATION PREREQUISITES

✅ **Accurate Birth Data:**
- Correct date, time (critical!), location (latitude/longitude)
- Correct timezone, UTC conversion accuracy

✅ **Astronomical Data:**
- Ephemeris precision (SwissEphemeris)
- Ayanamsa correction (Lahiri)
- House system (Placidus)

✅ **Astrological Rules:**
- Nakshatra assignments, House lordship
- Dignities, Combustion, Aspects

✅ **Mathematical Accuracy:**
- Julian Day, Sidereal coordinates
- Degree normalization, Aspect orbs

---

## TOOLS & LIBRARIES

- **SwissEphemeris**: Precise planetary calculations
- **PyMeeus**: Astronomical calculations
- **PyTZ**: Timezone handling
- **Pydantic**: Data validation
- **Lahiri Ayanamsa**: Vedic correction system
- **Placidus House System**: House division
- **XGBoost**: ML predictions (53 features)
- **MongoDB**: Data storage
- **FastAPI**: API layer

---

**Total Data Points Per Kundali: 500+ calculated values**
