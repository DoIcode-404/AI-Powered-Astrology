"""
Test Trained ML Model on Real Kundali Data
Tests the XGBoost model with real birth data to see if predictions are reasonable.
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from typing import Dict, List, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RealDataTester:
    """Test trained model on real birth data."""

    def __init__(self):
        models_dir = Path(__file__).parent / "trained_models"

        logger.info("Loading trained model and preprocessor...")
        self.xgb_model = joblib.load(models_dir / "xgboost_model.pkl")
        self.scaler = joblib.load(models_dir / "scaler.pkl")

        with open(models_dir / "feature_names.json") as f:
            self.feature_names = json.load(f)

        with open(models_dir / "target_names.json") as f:
            self.target_names = json.load(f)

        logger.info(f"  Model loaded: {len(self.feature_names)} features, {len(self.target_names)} targets")

    def create_sample_features(self) -> pd.DataFrame:
        """
        Create sample real-like features for testing.

        In a real scenario, these would come from:
        1. Calling the backend /kundali/generate_kundali endpoint
        2. Extracting the same 53 features the model was trained on
        """
        logger.info("\nCreating sample test cases with realistic astrological features...")

        test_cases = []

        # Test Case 1: Strong chart (high planetary strengths)
        case1 = {
            'sun_degree': 45,
            'moon_degree': 120,
            'mercury_degree': 50,
            'venus_degree': 60,
            'mars_degree': 200,
            'jupiter_degree': 90,
            'saturn_degree': 150,
            'rahu_degree': 30,
            'ketu_degree': 210,
            'ascendant_degree': 0,
        }
        # Strong house placements
        for h in range(1, 13):
            case1[f'house_{h}_planets'] = np.random.randint(1, 3)
            case1[f'house_{h}_lord_strength'] = np.random.uniform(70, 95)
        # Strong planetary strengths
        for planet in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'rahu', 'ketu']:
            case1[f'{planet}_strength'] = np.random.uniform(70, 95)
        # Good yogas
        case1['total_yoga_count'] = 6
        case1['benefic_yoga_count'] = 5
        case1['malefic_yoga_count'] = 1
        case1['neutral_yoga_count'] = 0
        for i in range(1, 7):
            case1[f'aspect_strength_{i}'] = np.random.uniform(60, 90)
        test_cases.append(('Strong Chart (Well-Aspected, Multiple Yogas)', case1))

        # Test Case 2: Weak chart (low planetary strengths)
        case2 = {
            'sun_degree': 30,
            'moon_degree': 180,
            'mercury_degree': 45,
            'venus_degree': 75,
            'mars_degree': 300,
            'jupiter_degree': 210,
            'saturn_degree': 240,
            'rahu_degree': 120,
            'ketu_degree': 300,
            'ascendant_degree': 90,
        }
        # Weak house placements
        for h in range(1, 13):
            case2[f'house_{h}_planets'] = 0
            case2[f'house_{h}_lord_strength'] = np.random.uniform(20, 40)
        # Weak planetary strengths
        for planet in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'rahu', 'ketu']:
            case2[f'{planet}_strength'] = np.random.uniform(20, 40)
        # Few/bad yogas
        case2['total_yoga_count'] = 1
        case2['benefic_yoga_count'] = 0
        case2['malefic_yoga_count'] = 1
        case2['neutral_yoga_count'] = 0
        for i in range(1, 7):
            case2[f'aspect_strength_{i}'] = np.random.uniform(10, 30)
        test_cases.append(('Weak Chart (Afflicted, Few Yogas)', case2))

        # Test Case 3: Average chart (mixed)
        case3 = {
            'sun_degree': 100,
            'moon_degree': 200,
            'mercury_degree': 150,
            'venus_degree': 120,
            'mars_degree': 80,
            'jupiter_degree': 280,
            'saturn_degree': 60,
            'rahu_degree': 200,
            'ketu_degree': 20,
            'ascendant_degree': 180,
        }
        # Average house placements
        for h in range(1, 13):
            case3[f'house_{h}_planets'] = np.random.randint(0, 2)
            case3[f'house_{h}_lord_strength'] = np.random.uniform(45, 65)
        # Average planetary strengths
        for planet in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'rahu', 'ketu']:
            case3[f'{planet}_strength'] = np.random.uniform(45, 65)
        # Average yogas
        case3['total_yoga_count'] = 3
        case3['benefic_yoga_count'] = 2
        case3['malefic_yoga_count'] = 1
        case3['neutral_yoga_count'] = 0
        for i in range(1, 7):
            case3[f'aspect_strength_{i}'] = np.random.uniform(40, 60)
        test_cases.append(('Average Chart (Balanced)', case3))

        return test_cases

    def make_predictions(self, features_dict: Dict) -> Dict:
        """Make prediction for a single case."""
        # Convert to DataFrame
        features_df = pd.DataFrame([features_dict])

        # Ensure all required features are present
        for feat in self.feature_names:
            if feat not in features_df.columns:
                features_df[feat] = 0

        # Select only required features in correct order
        X = features_df[self.feature_names]

        # Normalize
        X_normalized = self.scaler.transform(X)

        # Predict
        predictions = self.xgb_model.predict(X_normalized)[0]

        return {
            self.target_names[i]: float(predictions[i])
            for i in range(len(self.target_names))
        }

    def interpret_prediction(self, target: str, value: float) -> str:
        """Interpret a predicted value in human-readable terms."""
        if value < 30:
            rating = "POOR"
        elif value < 50:
            rating = "BELOW AVERAGE"
        elif value < 70:
            rating = "AVERAGE"
        elif value < 85:
            rating = "GOOD"
        else:
            rating = "EXCELLENT"

        return f"{value:.1f}/100 ({rating})"

    def test_all_cases(self):
        """Test model on all sample cases."""
        test_cases = self.create_sample_features()

        print("\n" + "="*100)
        print("TESTING TRAINED MODEL ON REAL DATA SCENARIOS")
        print("="*100)

        for case_name, features in test_cases:
            print(f"\n{case_name}")
            print("-" * 100)

            # Make predictions
            predictions = self.make_predictions(features)

            # Display results
            print("\nPredicted Life Outcomes:")
            for target in self.target_names:
                value = predictions[target]
                interpretation = self.interpret_prediction(target, value)
                print(f"  {target:.<30} {interpretation}")

            # Summary
            avg_score = np.mean(list(predictions.values()))
            print(f"\n  Average Life Score: {avg_score:.1f}/100")

            # Interpretation
            if avg_score >= 80:
                summary = "This chart indicates a very fortunate life with excellent prospects across all areas."
            elif avg_score >= 70:
                summary = "This chart shows good overall potential with balanced opportunities and challenges."
            elif avg_score >= 60:
                summary = "This chart indicates average potential with some strengths to leverage and some areas to work on."
            elif avg_score >= 50:
                summary = "This chart shows mixed results - will need effort to overcome challenges and maximize potential."
            else:
                summary = "This chart indicates significant challenges ahead - strong will and spiritual growth recommended."

            print(f"\n  Interpretation: {summary}")

    def test_with_custom_features(self, features_dict: Dict, description: str = "Custom"):
        """Test with user-provided features."""
        print(f"\n{description}")
        print("-" * 100)

        predictions = self.make_predictions(features_dict)

        print("\nPredicted Outcomes:")
        for target in self.target_names:
            value = predictions[target]
            interpretation = self.interpret_prediction(target, value)
            print(f"  {target:.<30} {interpretation}")

        avg_score = np.mean(list(predictions.values()))
        print(f"\nAverage Score: {avg_score:.1f}/100")

        return predictions


def main():
    """Main test function."""
    print("\n" + "="*100)
    print("REAL DATA TESTING FRAMEWORK")
    print("="*100)

    tester = RealDataTester()

    # Test on sample cases
    tester.test_all_cases()

    print("\n\n" + "="*100)
    print("USING THE MODEL IN PRODUCTION")
    print("="*100)
    print("""
To use this model with REAL Kundali data:

1. GET REAL DATA:
   - Call backend API: POST /kundali/generate_kundali
   - Input: birthDate, birthTime, latitude, longitude, timezone
   - Output: Full Kundali with all astrological calculations

2. EXTRACT FEATURES:
   - Extract same 53 features used in training:
     * Planetary positions (10): sun_degree, moon_degree, etc.
     * House placements (24): house_1_planets, house_1_lord_strength, etc.
     * Planetary strengths (9): sun_strength, moon_strength, etc.
     * Yoga counts (4): total_yoga_count, benefic_yoga_count, etc.
     * Aspect strengths (6): aspect_strength_1, aspect_strength_2, etc.

3. MAKE PREDICTIONS:
   - Load model: xgb_model = joblib.load('trained_models/xgboost_model.pkl')
   - Load scaler: scaler = joblib.load('trained_models/scaler.pkl')
   - Normalize: X_normalized = scaler.transform(features)
   - Predict: predictions = xgb_model.predict(X_normalized)

4. INTERPRET RESULTS:
   - 8 output values (0-100 scale):
     * career_potential: Success in profession/business
     * wealth_potential: Financial abundance prospects
     * marriage_happiness: Relationship harmony and success
     * children_prospects: Fertility and children's welfare
     * health_status: Physical and mental well-being
     * spiritual_inclination: Spiritual evolution potential
     * chart_strength: Overall astrological strength
     * life_ease_score: General ease/difficulty of life

5. VALIDATE:
   Since targets are predictions (not ground truth):
   - Compare against real-life outcomes over time
   - Track accuracy as real events unfold
   - Refine model with actual outcomes (if collected)

LIMITATIONS:
- Model is trained on SYNTHETIC data (features generated, not from real API)
- No ground truth to compare against (these are predictions, not facts)
- Accuracy depends on feature quality from backend API
- Should be used for guidance, not definitive statements
""")

    print("="*100 + "\n")


if __name__ == "__main__":
    main()