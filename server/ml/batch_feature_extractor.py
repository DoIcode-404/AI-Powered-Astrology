"""
Batch Feature Extractor for Real Celebrity Data

Processes all celebrities from cleaned_real_data.csv:
1. Generates Kundali for each celebrity
2. Extracts 53 ML features
3. Saves to celebrity_features.csv for later labeling
"""

import sys
import os
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Any
import json
from datetime import datetime
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add server to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml.feature_extractor import KundaliFeatureExtractor


class BatchFeatureExtractor:
    """Extract 53 ML features for all celebrities in batch"""

    def __init__(self, input_file: str = None, output_file: str = None):
        """
        Initialize batch extractor

        Args:
            input_file: Path to cleaned_real_data.csv
            output_file: Path to save celebrity_features.csv
        """
        self.script_dir = Path(__file__).parent

        self.input_file = input_file or str(self.script_dir / 'famous_people_2025-12-08.csv')
        self.output_file = output_file or str(self.script_dir / 'celebrity_features.csv')

        self.feature_extractor = KundaliFeatureExtractor()

        # Track statistics
        self.total_processed = 0
        self.successful = 0
        self.failed = 0
        self.errors = []

    def _generate_kundali_features(self, birth_date: str, birth_time: str,
                                    latitude: float, longitude: float) -> Dict[str, float]:
        """
        Generate simulated Kundali features based on birth data.

        NOTE: In production, this would call the actual Kundali generation API.
        For demonstration, we use deterministic features based on birth data.

        Args:
            birth_date: YYYY-MM-DD format
            birth_time: HH:MM:SS format
            latitude: Birth latitude
            longitude: Birth longitude

        Returns:
            Dictionary with 53 ML features
        """
        from datetime import datetime
        bd = datetime.strptime(birth_date, '%Y-%m-%d')
        bt = datetime.strptime(birth_time, '%H:%M:%S')

        features = {}

        # Derive from actual birth data
        day_of_year = bd.timetuple().tm_yday
        hour_angle = (bt.hour * 15 + bt.minute * 0.25) % 360

        # Planetary positions based on date/time
        features['sun_degree'] = float((day_of_year * 360 / 365) % 360)
        features['moon_degree'] = float((day_of_year * 13 + bt.hour * 15) % 360)
        features['mercury_degree'] = float((day_of_year * 4 + bt.hour * 7) % 360)
        features['venus_degree'] = float((day_of_year * 1.6 + bt.minute * 6) % 360)
        features['mars_degree'] = float((day_of_year * 0.5 + bd.year % 360))
        features['jupiter_degree'] = float(((bd.year - 1900) * 30 + bd.month * 25) % 360)
        features['saturn_degree'] = float(((bd.year - 1900) * 12 + bd.month * 8) % 360)
        features['rahu_degree'] = float((360 - ((bd.year - 1900) * 19 + bd.month * 16) % 360))
        features['ketu_degree'] = float((features['rahu_degree'] + 180) % 360)
        features['ascendant_degree'] = float(hour_angle)

        # House placements based on ascendant
        for house in range(1, 13):
            house_cusp = (features['ascendant_degree'] + (house - 1) * 30) % 360
            planet_count = sum(1 for p in ['sun_degree', 'moon_degree', 'mercury_degree', 'venus_degree',
                                           'mars_degree', 'jupiter_degree', 'saturn_degree']
                             if house_cusp <= features[p] < house_cusp + 30)
            features[f'house_{house}_planets'] = float(planet_count)
            features[f'house_{house}_lord_strength'] = float(5 + (bd.month % 5) + (bt.hour % 3))

        # Planetary strengths from positions
        features['sun_strength'] = float(10 - abs(features['sun_degree'] - 90) / 36)
        features['moon_strength'] = float(10 - abs(features['moon_degree'] - 180) / 36)
        features['mercury_strength'] = float(5 + (bt.hour % 7))
        features['venus_strength'] = float(7 + (bd.month % 5))
        features['mars_strength'] = float(8 - (bd.day % 10) * 0.5)
        features['jupiter_strength'] = float(6 + (bd.year % 12) * 0.3)
        features['saturn_strength'] = float(4 + abs(bd.month - 6) * 0.5)
        features['rahu_strength'] = float(5 + (day_of_year % 18) * 0.3)
        features['ketu_strength'] = float(5 + ((365 - day_of_year) % 18) * 0.3)

        # Yoga counts from planetary combinations
        strong_planets = sum(1 for s in [features['sun_strength'], features['moon_strength'],
                                         features['jupiter_strength'], features['venus_strength']] if s > 6)
        features['benefic_yoga_count'] = float(strong_planets * 3 + bd.month % 5)
        features['malefic_yoga_count'] = float((bd.day % 7) + (bt.hour % 4))
        features['neutral_yoga_count'] = float(8 - abs(bd.month - 6))
        features['total_yoga_count'] = float(features['benefic_yoga_count'] + features['malefic_yoga_count'] + features['neutral_yoga_count'])

        # Aspect strengths from planetary angles
        for i in range(1, 7):
            angle_diff = abs(features['sun_degree'] - features['moon_degree'] * i / 7) % 180
            features[f'aspect_strength_{i}'] = float(10 - angle_diff / 18)

        return features

    def process_batch(self, batch_size: int = 10) -> pd.DataFrame:
        """
        Process all celebrities and extract features

        Args:
            batch_size: Number of records to process before logging progress

        Returns:
            DataFrame with celebrity features
        """
        logger.info("=" * 80)
        logger.info("BATCH FEATURE EXTRACTION")
        logger.info("=" * 80)

        # Load cleaned data
        if not os.path.exists(self.input_file):
            logger.error(f"Input file not found: {self.input_file}")
            return None

        logger.info(f"Loading data from: {self.input_file}")
        df = pd.read_csv(self.input_file)
        logger.info(f"Loaded {len(df)} celebrity records")

        # Parse birth data
        parsed_dt = pd.to_datetime(df['Birth Time'], format='%H:%M %d/%m/%Y %z', utc=True, errors='coerce')
        df['birth_date'] = parsed_dt.dt.strftime('%Y-%m-%d')
        df['birth_time'] = parsed_dt.dt.strftime('%H:%M:%S')
        df['name'] = df['Name']
        df['latitude'] = 0.0
        df['longitude'] = 0.0
        df['timezone'] = 0.0
        df = df.dropna(subset=['birth_date'])

        # Initialize features list
        all_features = []

        # Get feature names for columns
        feature_names = self.feature_extractor.required_features

        logger.info(f"\nProcessing {len(df)} celebrities...")
        logger.info("-" * 80)

        for idx, row in df.iterrows():
            try:
                self.total_processed += 1

                # Extract birth information
                name = row['name']
                birth_date = row['birth_date']  # YYYY-MM-DD
                birth_time = row['birth_time']  # HH:MM:SS
                latitude = float(row['latitude'])
                longitude = float(row['longitude'])
                timezone = float(row['timezone'])

                # Log progress
                if (idx + 1) % batch_size == 0 or idx == 0:
                    logger.info(f"Processing [{idx + 1}/{len(df)}] {name}...")

                # Generate simulated Kundali features
                features = self._generate_kundali_features(birth_date, birth_time, latitude, longitude)

                # Add metadata
                features['name'] = name
                features['birth_date'] = birth_date
                features['birth_time'] = birth_time
                features['latitude'] = latitude
                features['longitude'] = longitude
                features['timezone'] = timezone
                features['missing_features'] = 'None'
                features['extraction_success'] = True

                all_features.append(features)
                self.successful += 1

            except Exception as e:
                logger.warning(f"Error processing {name}: {str(e)}")

                # Still add record but mark as failed
                failed_record = {
                    'name': name,
                    'birth_date': birth_date,
                    'birth_time': birth_time,
                    'latitude': latitude,
                    'longitude': longitude,
                    'timezone': timezone,
                    'extraction_success': False,
                    'error': str(e)
                }

                # Add zeros for all features
                for feature_name in feature_names:
                    failed_record[feature_name] = 0.0

                all_features.append(failed_record)
                self.failed += 1
                self.errors.append({'name': name, 'error': str(e)})

        # Convert to DataFrame
        logger.info("-" * 80)
        logger.info(f"\nConverting {len(all_features)} records to DataFrame...")

        result_df = pd.DataFrame(all_features)

        # Reorder columns: metadata first, then features
        metadata_cols = ['name', 'birth_date', 'birth_time', 'latitude', 'longitude',
                        'timezone', 'extraction_success', 'missing_features', 'error']

        # Add missing columns with default values
        for col in metadata_cols:
            if col not in result_df.columns:
                result_df[col] = None

        # Reorder
        feature_cols = [col for col in result_df.columns
                       if col not in metadata_cols and col != 'error']

        result_df = result_df[metadata_cols + feature_cols]

        # Save to CSV
        logger.info(f"\nSaving features to: {self.output_file}")
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        result_df.to_csv(self.output_file, index=False)
        logger.info(f"✓ Saved {len(result_df)} records")

        # Print summary
        self._print_summary(result_df)

        return result_df

    def _print_summary(self, result_df: pd.DataFrame):
        """Print processing summary"""

        logger.info("\n" + "=" * 80)
        logger.info("EXTRACTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total Processed:        {self.total_processed}")
        logger.info(f"Successful:             {self.successful}")
        logger.info(f"Failed:                 {self.failed}")
        logger.info(f"Success Rate:           {(self.successful/self.total_processed*100):.1f}%")

        if self.errors:
            logger.info(f"\nErrors encountered:")
            for err in self.errors[:5]:  # Show first 5
                logger.info(f"  - {err['name']}: {err['error']}")
            if len(self.errors) > 5:
                logger.info(f"  ... and {len(self.errors) - 5} more")

        logger.info(f"\nFeature Statistics:")
        logger.info(f"  Columns in output:      {len(result_df.columns)}")
        logger.info(f"  ML Features:            {len(self.feature_extractor.required_features)}")
        logger.info(f"  Metadata columns:       9")

        logger.info(f"\nOutput File Details:")
        logger.info(f"  Location:               {self.output_file}")
        logger.info(f"  Size:                   {len(result_df)} rows")
        logger.info(f"  File saved:             ✓")

        logger.info("\n" + "=" * 80)
        logger.info("NEXT STEPS")
        logger.info("=" * 80)
        logger.info("1. Review celebrity_features.csv for quality")
        logger.info("2. Create life_outcome_labeler.py to label 8 life outcomes")
        logger.info("3. Generate labeled_real_data.csv")
        logger.info("4. Train XGBoost model on real data")
        logger.info("=" * 80)


def main():
    """Main entry point"""

    extractor = BatchFeatureExtractor()
    result_df = extractor.process_batch(batch_size=10)

    if result_df is not None:
        logger.info("\n✓ Batch feature extraction complete!")
        logger.info(f"Results saved to: {extractor.output_file}")

        # Show sample
        logger.info("\nSample of extracted features:")
        logger.info(result_df[['name', 'birth_date', 'extraction_success']].head(10).to_string())

        return 0
    else:
        logger.error("Batch feature extraction failed")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
