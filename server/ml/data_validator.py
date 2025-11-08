"""
Data Validation and Quality Assessment
Validates generated synthetic dataset for ML training readiness.

Checks:
- No duplicates
- Valid feature ranges
- Missing values
- Target distribution
- Outlier detection
- Data quality scoring

Author: ML Pipeline
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate and assess quality of generated Kundali dataset."""

    # Expected feature ranges
    FEATURE_RANGES = {
        # Degree features (0-360)
        'sun_degree': (0, 360),
        'moon_degree': (0, 360),
        'mars_degree': (0, 360),
        'mercury_degree': (0, 360),
        'jupiter_degree': (0, 360),
        'venus_degree': (0, 360),
        'saturn_degree': (0, 360),
        'rahu_degree': (0, 360),
        'ketu_degree': (0, 360),

        # House features (1-12)
        'sun_house': (1, 12),
        'moon_house': (1, 12),
        'mars_house': (1, 12),
        'mercury_house': (1, 12),
        'jupiter_house': (1, 12),
        'venus_house': (1, 12),
        'saturn_house': (1, 12),
        'rahu_house': (1, 12),
        'ketu_house': (1, 12),

        # Strength percentages (0-100)
        'sun_strength': (0, 100),
        'moon_strength': (0, 100),
        'mars_strength': (0, 100),
        'mercury_strength': (0, 100),
        'jupiter_strength': (0, 100),
        'venus_strength': (0, 100),
        'saturn_strength': (0, 100),

        # Alignment and other percentage features
        'd1_d9_alignment': (0, 100),
        'chart_quality_score': (0, 100),
        'retrograde_planet_count': (0, 9),

        # Target features (0-100)
        'career_potential': (0, 100),
        'wealth_potential': (0, 100),
        'marriage_happiness': (0, 100),
        'children_prospects': (0, 100),
        'health_status': (0, 100),
        'spiritual_inclination': (0, 100),
        'chart_strength': (0, 100),
        'life_ease_score': (0, 100),
    }

    def __init__(self):
        """Initialize the validator."""
        self.df = None
        self.validation_report = {}

    def load_data(self, csv_file: str) -> pd.DataFrame:
        """Load dataset from CSV file."""
        try:
            self.df = pd.read_csv(csv_file)
            logger.info(f"Loaded {len(self.df)} records from {csv_file}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            return None

    def validate(self, csv_file: str = None) -> Dict:
        """
        Perform complete validation of dataset.

        Args:
            csv_file: Path to CSV file to validate

        Returns:
            Validation report dictionary
        """
        if csv_file:
            self.load_data(csv_file)

        if self.df is None:
            logger.error("No data to validate")
            return {}

        logger.info("Starting validation...")

        # Run all checks
        self.validation_report = {
            'dataset_size': len(self.df),
            'feature_count': len(self.df.columns),
            'duplicate_check': self._check_duplicates(),
            'feature_ranges': self._check_feature_ranges(),
            'missing_values': self._check_missing_values(),
            'target_distribution': self._check_target_distribution(),
            'outlier_detection': self._detect_outliers(),
            'data_types': self._check_data_types(),
            'quality_score': 0.0,
            'status': 'UNKNOWN',
        }

        # Calculate overall quality score
        self.validation_report['quality_score'] = self._calculate_quality_score()
        self.validation_report['status'] = 'PASS' if self.validation_report['quality_score'] >= 85 else 'FAIL'

        logger.info(f"\nValidation Report:")
        logger.info(f"Quality Score: {self.validation_report['quality_score']:.2f}%")
        logger.info(f"Status: {self.validation_report['status']}")

        return self.validation_report

    def _check_duplicates(self) -> Dict:
        """Check for duplicate records."""
        try:
            total_records = len(self.df)
            duplicate_rows = self.df.duplicated().sum()
            duplicate_percentage = (duplicate_rows / total_records) * 100 if total_records > 0 else 0

            result = {
                'total_records': total_records,
                'duplicate_count': int(duplicate_rows),
                'duplicate_percentage': round(duplicate_percentage, 2),
                'status': 'PASS' if duplicate_percentage < 1 else 'FAIL'
            }

            logger.info(f"Duplicate Check: {duplicate_rows} duplicates ({duplicate_percentage:.2f}%)")
            return result

        except Exception as e:
            logger.error(f"Error checking duplicates: {str(e)}")
            return {'status': 'ERROR'}

    def _check_feature_ranges(self) -> Dict:
        """Check if all features are within expected ranges."""
        out_of_range = {}

        for feature, (min_val, max_val) in self.FEATURE_RANGES.items():
            if feature in self.df.columns:
                invalid_count = self.df[
                    (self.df[feature] < min_val) | (self.df[feature] > max_val)
                ].shape[0]

                if invalid_count > 0:
                    out_of_range[feature] = int(invalid_count)

        result = {
            'total_features_checked': len(self.FEATURE_RANGES),
            'features_in_range': len(self.FEATURE_RANGES) - len(out_of_range),
            'out_of_range_features': out_of_range,
            'status': 'PASS' if len(out_of_range) == 0 else 'FAIL'
        }

        logger.info(f"Feature Range Check: {result['features_in_range']}/{len(self.FEATURE_RANGES)} in range")
        return result

    def _check_missing_values(self) -> Dict:
        """Check for missing values."""
        missing_per_feature = self.df.isnull().sum()
        total_values = len(self.df) * len(self.df.columns)
        missing_values = missing_per_feature.sum()
        missing_percentage = (missing_values / total_values) * 100

        result = {
            'total_missing': int(missing_values),
            'missing_percentage': round(missing_percentage, 2),
            'status': 'PASS' if missing_percentage < 5 else 'WARNING'
        }

        logger.info(f"Missing Values Check: {missing_percentage:.2f}% missing ({missing_values} values)")
        return result

    def _check_target_distribution(self) -> Dict:
        """Check distribution of target variables."""
        target_features = [
            'career_potential', 'wealth_potential', 'marriage_happiness',
            'children_prospects', 'health_status', 'spiritual_inclination',
            'chart_strength', 'life_ease_score'
        ]

        distribution = {}

        for target in target_features:
            if target in self.df.columns:
                stats = {
                    'mean': round(self.df[target].mean(), 2),
                    'std': round(self.df[target].std(), 2),
                    'min': round(self.df[target].min(), 2),
                    'max': round(self.df[target].max(), 2),
                    'median': round(self.df[target].median(), 2)
                }
                distribution[target] = stats

                logger.info(f"{target}: mean={stats['mean']}, std={stats['std']}")

        result = {
            'target_distribution': distribution,
            'targets_present': len(distribution),
            'status': 'PASS' if len(distribution) >= 6 else 'FAIL'
        }

        return result

    def _detect_outliers(self) -> Dict:
        """Detect outliers using IQR method."""
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns

        outliers_detected = {}
        total_outliers = 0

        for col in numeric_columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outlier_count = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()

            if outlier_count > 0:
                outliers_detected[col] = int(outlier_count)
                total_outliers += outlier_count

        result = {
            'total_outliers_detected': total_outliers,
            'columns_with_outliers': len(outliers_detected),
            'outlier_details': outliers_detected,
            'status': 'PASS' if total_outliers < (len(self.df) * 0.05) else 'WARNING'
        }

        logger.info(f"Outlier Detection: {total_outliers} outliers found")
        return result

    def _check_data_types(self) -> Dict:
        """Check data types of columns."""
        type_counts = self.df.dtypes.value_counts().to_dict()

        result = {
            'type_distribution': {str(k): v for k, v in type_counts.items()},
            'total_columns': len(self.df.columns),
            'numeric_columns': len(self.df.select_dtypes(include=[np.number]).columns),
            'object_columns': len(self.df.select_dtypes(include=['object']).columns)
        }

        return result

    def _calculate_quality_score(self) -> float:
        """Calculate overall data quality score (0-100)."""
        score = 100.0

        # Deductions based on checks
        dup_check = self.validation_report.get('duplicate_check', {})
        if dup_check.get('status') == 'FAIL':
            score -= 10 * (dup_check.get('duplicate_percentage', 0) / 5)

        range_check = self.validation_report.get('feature_ranges', {})
        if range_check.get('status') == 'FAIL':
            score -= 15

        missing_check = self.validation_report.get('missing_values', {})
        if missing_check.get('status') == 'WARNING':
            score -= 5 * (missing_check.get('missing_percentage', 0) / 5)

        target_check = self.validation_report.get('target_distribution', {})
        if target_check.get('status') == 'FAIL':
            score -= 20

        outlier_check = self.validation_report.get('outlier_detection', {})
        if outlier_check.get('status') == 'WARNING':
            score -= 5

        return round(max(0, min(100, score)), 2)

    def generate_report(self, output_file: str = 'validation_report.json'):
        """Generate and save validation report."""
        try:
            # Convert numpy types to Python native types for JSON serialization
            def convert_types(obj):
                if isinstance(obj, dict):
                    return {k: convert_types(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_types(v) for v in obj]
                elif isinstance(obj, (np.integer, np.floating)):
                    return float(obj) if isinstance(obj, np.floating) else int(obj)
                return obj

            report_serializable = convert_types(self.validation_report)

            with open(output_file, 'w') as f:
                json.dump(report_serializable, f, indent=2)
            logger.info(f"Report saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving report: {str(e)}")

    def print_summary(self):
        """Print validation summary."""
        print("\n" + "="*60)
        print("DATA VALIDATION REPORT")
        print("="*60)

        if not self.validation_report:
            print("No validation report available")
            return

        print(f"\nDataset Size: {self.validation_report.get('dataset_size', 'N/A')} records")
        print(f"Features: {self.validation_report.get('feature_count', 'N/A')}")

        print(f"\n[OK] Quality Score: {self.validation_report.get('quality_score', 'N/A')}%")
        print(f"[OK] Status: {self.validation_report.get('status', 'N/A')}")

        print(f"\nCheck Results:")
        print(f"  - Duplicates: {self.validation_report.get('duplicate_check', {}).get('status', 'N/A')}")
        print(f"  - Feature Ranges: {self.validation_report.get('feature_ranges', {}).get('status', 'N/A')}")
        print(f"  - Missing Values: {self.validation_report.get('missing_values', {}).get('status', 'N/A')}")
        print(f"  - Target Distribution: {self.validation_report.get('target_distribution', {}).get('status', 'N/A')}")
        print(f"  - Outliers: {self.validation_report.get('outlier_detection', {}).get('status', 'N/A')}")

        print("\n" + "="*60 + "\n")


def main():
    """Main validation function."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    validator = DataValidator()

    # Validate generated dataset
    csv_file = 'training_data.csv'
    report = validator.validate(csv_file)

    # Print and save results
    validator.print_summary()
    validator.generate_report('validation_report.json')

    if report.get('status') == 'PASS':
        print("[OK] Dataset is ready for ML training!")
    else:
        print("[WARNING] Dataset needs improvement")
        print(f"Quality Score: {report.get('quality_score')}%")


if __name__ == "__main__":
    main()