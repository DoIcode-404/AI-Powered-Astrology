"""
Real Data Processor - Clean, validate, and process real-world astrology data
for model training.

This script helps you:
1. Consolidate data from multiple sources
2. Remove duplicates
3. Validate birth data
4. Prepare for feature extraction
5. Create training dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Tuple, Dict, List
from datetime import datetime
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RealDataProcessor:
    """Process real astrology data for model training."""

    def __init__(self, input_dir: str = 'raw_data', output_dir: str = 'processed_data'):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.input_dir.mkdir(exist_ok=True)

    def load_csv_data(self, filepath: str) -> pd.DataFrame:
        """
        Load CSV data from various sources.

        Expected columns:
        - name: person's name
        - birth_date: YYYY-MM-DD format
        - birth_time: HH:MM:SS format
        - birth_location: location string
        - latitude: float
        - longitude: float
        - timezone: float (optional, will calculate if missing)
        """
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {filepath}: {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error loading {filepath}: {str(e)}")
            return pd.DataFrame()

    def standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names across different data sources.

        Maps various column names to standard format.
        """
        column_mapping = {
            # Name variations
            'Name': 'name',
            'Person': 'name',
            'Celebrity': 'name',
            'Full Name': 'name',

            # Birth Date variations
            'DOB': 'birth_date',
            'Date of Birth': 'birth_date',
            'Birth Date': 'birth_date',
            'date_of_birth': 'birth_date',

            # Birth Time variations
            'Time of Birth': 'birth_time',
            'Birth Time': 'birth_time',
            'time_of_birth': 'birth_time',
            'TOB': 'birth_time',

            # Location variations
            'Place of Birth': 'birth_location',
            'Birth Place': 'birth_location',
            'Place': 'birth_location',
            'location': 'birth_location',
            'city': 'birth_location',

            # Latitude/Longitude variations
            'Lat': 'latitude',
            'Latitude': 'latitude',
            'Lon': 'longitude',
            'Longitude': 'longitude',

            # Timezone
            'TZ': 'timezone',
            'TimeZone': 'timezone',
            'Time Zone': 'timezone',

            # Data quality
            'Reliability': 'reliability',
            'Rating': 'reliability',
            'Data Quality': 'reliability',
            'Source': 'data_source',
        }

        df = df.rename(columns=column_mapping)
        return df

    def validate_birth_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[int]]:
        """
        Validate birth date, time, and location data.

        Returns:
        - Cleaned DataFrame
        - List of row indices that failed validation
        """
        logger.info(f"Validating {len(df)} records...")

        invalid_rows = []
        errors = {
            'missing_name': 0,
            'invalid_date': 0,
            'invalid_time': 0,
            'invalid_coordinates': 0,
            'missing_critical': 0
        }

        for idx, row in df.iterrows():
            # Check name
            if pd.isna(row.get('name', None)) or str(row.get('name', '')).strip() == '':
                errors['missing_name'] += 1
                invalid_rows.append(idx)
                continue

            # Validate date
            try:
                pd.to_datetime(row['birth_date'], format='%Y-%m-%d')
            except:
                errors['invalid_date'] += 1
                invalid_rows.append(idx)
                continue

            # Validate time (can be 00:00:00 if unknown)
            try:
                if pd.notna(row.get('birth_time', None)):
                    pd.to_datetime(row['birth_time'], format='%H:%M:%S')
            except:
                errors['invalid_time'] += 1
                invalid_rows.append(idx)
                continue

            # Validate coordinates
            try:
                lat = float(row['latitude'])
                lon = float(row['longitude'])
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    errors['invalid_coordinates'] += 1
                    invalid_rows.append(idx)
                    continue
            except:
                errors['invalid_coordinates'] += 1
                invalid_rows.append(idx)
                continue

        # Remove invalid rows
        df_clean = df.drop(invalid_rows).reset_index(drop=True)

        logger.info(f"Validation Results:")
        logger.info(f"  Total records: {len(df)}")
        logger.info(f"  Valid records: {len(df_clean)}")
        logger.info(f"  Removed: {len(invalid_rows)}")
        logger.info(f"  Error breakdown: {errors}")

        return df_clean, invalid_rows

    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """
        Remove duplicate records.

        By default, considers name + birth_date as unique identifier.
        """
        if subset is None:
            subset = ['name', 'birth_date']

        logger.info(f"Checking for duplicates on {subset}...")

        duplicates_before = len(df)
        df_dedup = df.drop_duplicates(subset=subset, keep='first').reset_index(drop=True)
        duplicates_removed = duplicates_before - len(df_dedup)

        logger.info(f"  Before: {duplicates_before} records")
        logger.info(f"  After: {len(df_dedup)} records")
        logger.info(f"  Removed: {duplicates_removed} duplicates")

        return df_dedup

    def calculate_missing_timezone(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate timezone from longitude if missing.

        Formula: timezone = longitude / 15
        (Each 15° of longitude = 1 hour of timezone)
        """
        logger.info("Calculating missing timezones from longitude...")

        missing_count = df['timezone'].isna().sum()

        if missing_count > 0:
            df.loc[df['timezone'].isna(), 'timezone'] = df.loc[df['timezone'].isna(), 'longitude'] / 15

            logger.info(f"  Calculated timezone for {missing_count} records")

        return df

    def standardize_datetime_formats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure consistent datetime formats.
        """
        logger.info("Standardizing datetime formats...")

        # Standardize date format to YYYY-MM-DD
        df['birth_date'] = pd.to_datetime(df['birth_date']).dt.strftime('%Y-%m-%d')

        # Standardize time format to HH:MM:SS
        if 'birth_time' in df.columns and df['birth_time'].notna().any():
            df['birth_time'] = pd.to_datetime(
                df['birth_time'],
                format='%H:%M:%S',
                errors='coerce'
            ).dt.strftime('%H:%M:%S')

        logger.info("  Date and time formats standardized")

        return df

    def merge_data_sources(self, filepath_list: List[str]) -> pd.DataFrame:
        """
        Merge data from multiple CSV files.

        Usage:
            merged = processor.merge_data_sources([
                'raw_data/vedastro.csv',
                'raw_data/astrodatabank.csv',
                'raw_data/astroseek.csv'
            ])
        """
        logger.info(f"\nMerging {len(filepath_list)} data sources...")

        all_dfs = []

        for filepath in filepath_list:
            df = self.load_csv_data(filepath)
            if not df.empty:
                df = self.standardize_columns(df)
                all_dfs.append(df)
                logger.info(f"  Added {len(df)} records from {Path(filepath).name}")

        if not all_dfs:
            logger.error("No data loaded from any source!")
            return pd.DataFrame()

        merged_df = pd.concat(all_dfs, ignore_index=True)
        logger.info(f"\nTotal merged records: {len(merged_df)}")

        return merged_df

    def process_full_pipeline(self, input_files: List[str]) -> pd.DataFrame:
        """
        Execute complete data processing pipeline.

        Steps:
        1. Load data from multiple sources
        2. Standardize columns
        3. Validate data
        4. Remove duplicates
        5. Fix timezones
        6. Standardize datetime formats
        7. Save to clean CSV

        Usage:
            processor = RealDataProcessor()
            clean_data = processor.process_full_pipeline([
                'raw_data/vedastro.csv',
                'raw_data/astrodatabank.csv'
            ])
        """
        logger.info("="*80)
        logger.info("REAL DATA PROCESSING PIPELINE")
        logger.info("="*80 + "\n")

        # Step 1: Merge from multiple sources
        logger.info("STEP 1: Merging data sources...")
        df = self.merge_data_sources(input_files)

        if df.empty:
            logger.error("No data to process!")
            return df

        # Step 2: Standardize columns
        logger.info("\nSTEP 2: Standardizing column names...")
        df = self.standardize_columns(df)

        # Step 3: Validate data
        logger.info("\nSTEP 3: Validating birth data...")
        df, invalid_indices = self.validate_birth_data(df)

        # Step 4: Remove duplicates
        logger.info("\nSTEP 4: Removing duplicates...")
        df = self.remove_duplicates(df)

        # Step 5: Calculate missing timezones
        logger.info("\nSTEP 5: Calculating missing timezones...")
        df = self.calculate_missing_timezone(df)

        # Step 6: Standardize datetime formats
        logger.info("\nSTEP 6: Standardizing datetime formats...")
        df = self.standardize_datetime_formats(df)

        # Step 7: Save clean data
        logger.info("\nSTEP 7: Saving cleaned data...")
        output_file = self.output_dir / 'cleaned_real_data.csv'
        df.to_csv(output_file, index=False)
        logger.info(f"  Saved to: {output_file}")
        logger.info(f"  Total records: {len(df)}")

        # Print summary statistics
        self.print_summary(df)

        return df

    def print_summary(self, df: pd.DataFrame):
        """Print summary statistics of processed data."""
        summary = f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    DATA PROCESSING COMPLETE                                   ║
╚════════════════════════════════════════════════════════════════════════════════╝

📊 FINAL DATASET STATISTICS
═══════════════════════════════════════════════════════════════════════════════

Total Records:                    {len(df):,}
Valid Records:                    {len(df):,}

Birth Date Range:                 {df['birth_date'].min()} to {df['birth_date'].max()}
Birth Time Coverage:              {df['birth_time'].notna().sum():,} records with time

Geographic Coverage:
  Latitude Range:                 {df['latitude'].min():.2f}° to {df['latitude'].max():.2f}°
  Longitude Range:                {df['longitude'].min():.2f}° to {df['longitude'].max():.2f}°
  Countries Represented:          ~{df['birth_location'].nunique()} unique locations

Data Quality:
  Missing Values:                 {df.isna().sum().sum()}
  Duplicates Removed:             ✓
  Invalid Records Removed:        ✓

═══════════════════════════════════════════════════════════════════════════════

🎯 NEXT STEPS
═══════════════════════════════════════════════════════════════════════════════

1. ✅ Data cleaning complete → cleaned_real_data.csv

2. 📊 Next: Generate Kundali features
   - Run your kundali generator for each record
   - Extract 53 ML features
   - Store in database

3. 🏷️  Then: Label with life outcomes
   - Research each celebrity
   - Rate 8 life outcome variables (0-100)
   - Create labeled_real_data.csv

4. 🤖 Finally: Train models on real data
   - Use labeled_real_data.csv
   - Replace synthetic_data.csv in training
   - Expect 20-40% better performance!

═══════════════════════════════════════════════════════════════════════════════

📁 OUTPUT FILES
═══════════════════════════════════════════════════════════════════════════════

Location: {self.output_dir}/

Files created:
  ✓ cleaned_real_data.csv         → Ready for feature extraction
                                     Columns: name, birth_date, birth_time,
                                              birth_location, latitude,
                                              longitude, timezone, ...

═══════════════════════════════════════════════════════════════════════════════
        """

        logger.info(summary)


def example_usage():
    """Example of how to use the real data processor."""
    processor = RealDataProcessor()

    # Example: If you've already downloaded CSV files from the sources
    # input_files = [
    #     'raw_data/vedastro_data.csv',
    #     'raw_data/astrodatabank_data.csv',
    #     'raw_data/astroseek_data.csv',
    # ]
    #
    # clean_data = processor.process_full_pipeline(input_files)

    logger.info("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    REAL DATA PROCESSOR - USAGE GUIDE                          ║
╚════════════════════════════════════════════════════════════════════════════════╝

To use this processor:

1. Download data from public sources:

   VedAstro (GitHub):
   ├─ git clone https://github.com/VedAstro/VedAstro.git
   └─ Extract CSV with 15,000+ celebrity birth data

   Astro-Databank:
   ├─ Visit: https://www.astro.com/astro-databank/Main_Page
   └─ Export CSV with 20,000+ records

   Astro-Seek:
   ├─ Visit: https://famouspeople.astro-seek.com/
   └─ Download CSV with 90,000+ records

2. Create 'raw_data/' directory:
   └─ Place all downloaded CSVs here

3. Run this processor:

   from real_data_processor import RealDataProcessor

   processor = RealDataProcessor(
       input_dir='raw_data',
       output_dir='processed_data'
   )

   clean_data = processor.process_full_pipeline([
       'raw_data/vedastro.csv',
       'raw_data/astrodatabank.csv',
       'raw_data/astroseek.csv',
   ])

4. Check output:
   ├─ processed_data/cleaned_real_data.csv
   └─ Ready for feature extraction!

═══════════════════════════════════════════════════════════════════════════════
    """)


if __name__ == "__main__":
    example_usage()
