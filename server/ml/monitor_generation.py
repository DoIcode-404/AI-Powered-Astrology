"""
Real-time Monitor for Synthetic Data Generation
Tracks progress, speed, and dataset statistics in real-time.
"""

import pandas as pd
import time
import os
from datetime import datetime
from pathlib import Path
import json

class GenerationMonitor:
    """Monitor synthetic data generation progress."""

    def __init__(self, csv_file='training_data.csv', check_interval=5):
        """
        Initialize monitor.

        Args:
            csv_file: Path to CSV being generated
            check_interval: Seconds between checks
        """
        self.csv_file = csv_file
        self.check_interval = check_interval
        self.start_time = time.time()
        self.last_row_count = 0
        self.samples_collected = []

    def get_file_stats(self):
        """Get current file statistics."""
        if not os.path.exists(self.csv_file):
            return None

        try:
            df = pd.read_csv(self.csv_file)
            return {
                'rows': len(df),
                'columns': len(df.columns),
                'size_mb': os.path.getsize(self.csv_file) / (1024 * 1024),
                'timestamp': datetime.now()
            }
        except Exception as e:
            return None

    def calculate_speed(self, current_rows):
        """Calculate generation speed."""
        elapsed = time.time() - self.start_time
        if elapsed == 0:
            return 0

        rows_generated = current_rows - self.last_row_count
        speed = rows_generated / elapsed
        return speed

    def estimate_completion(self, current_rows, target_rows):
        """Estimate time to completion."""
        elapsed = time.time() - self.start_time
        if current_rows == 0:
            return None

        speed = current_rows / elapsed
        remaining = target_rows - current_rows

        if speed == 0:
            return None

        eta_seconds = remaining / speed
        hours = int(eta_seconds // 3600)
        minutes = int((eta_seconds % 3600) // 60)
        seconds = int(eta_seconds % 60)

        return {'hours': hours, 'minutes': minutes, 'seconds': seconds}

    def format_time(self, seconds):
        """Format seconds to readable time."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"

    def print_header(self):
        """Print monitoring header."""
        print("\n" + "="*80)
        print(" SYNTHETIC DATA GENERATION MONITOR ".center(80))
        print("="*80 + "\n")

    def print_stats(self, stats, current_speed, target_rows=10000):
        """Print current statistics."""
        if stats is None:
            print("⏳ Waiting for file to be created...")
            return

        rows = stats['rows']
        progress = (rows / target_rows) * 100

        # Progress bar
        bar_length = 50
        filled = int(bar_length * rows / target_rows)
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"\n📊 PROGRESS")
        print(f"   [{bar}] {progress:.1f}% ({rows:,}/{target_rows:,} records)")

        # Speed and time
        elapsed = time.time() - self.start_time
        eta = self.estimate_completion(rows, target_rows)

        print(f"\n⏱️  TIMING")
        print(f"   Elapsed: {self.format_time(elapsed)}")
        if eta and current_speed > 0:
            print(f"   ETA: {eta['hours']}h {eta['minutes']}m {eta['seconds']}s")
            completion_time = datetime.now().timestamp() + (eta['hours']*3600 + eta['minutes']*60 + eta['seconds'])
            completion_str = datetime.fromtimestamp(completion_time).strftime('%H:%M:%S')
            print(f"   Completion: ~{completion_str}")

        # Speed
        print(f"\n🚀 SPEED")
        if current_speed > 0:
            print(f"   {current_speed:.2f} records/second")
            print(f"   {current_speed * 60:.0f} records/minute")
        else:
            print(f"   Calculating...")

        # Dataset info
        print(f"\n📁 FILE INFO")
        print(f"   Rows: {rows:,}")
        print(f"   Columns: {stats['columns']}")
        print(f"   Size: {stats['size_mb']:.2f} MB")

        # Quality metrics
        try:
            df = pd.read_csv(self.csv_file)
            print(f"\n✓ DATA QUALITY")
            print(f"   Missing values: {df.isnull().sum().sum()}")
            print(f"   Duplicates: {df.duplicated().sum()}")

            # Check target columns
            targets = ['career_potential', 'wealth_potential', 'marriage_happiness',
                      'children_prospects', 'health_status', 'spiritual_inclination',
                      'chart_strength', 'life_ease_score']
            targets_found = [t for t in targets if t in df.columns]
            print(f"   Targets found: {len(targets_found)}/8")

        except Exception as e:
            pass

    def monitor(self, target_rows=10000, max_duration=None):
        """
        Monitor generation in real-time.

        Args:
            target_rows: Target number of records
            max_duration: Maximum duration in seconds (None for unlimited)
        """
        self.print_header()
        check_count = 0
        last_rows = 0

        try:
            while True:
                stats = self.get_file_stats()

                if stats:
                    current_rows = stats['rows']
                    current_speed = self.calculate_speed(current_rows)

                    self.print_stats(stats, current_speed, target_rows)

                    # Check if complete
                    if current_rows >= target_rows:
                        print("\n" + "="*80)
                        print(" ✅ GENERATION COMPLETE! ".center(80))
                        print("="*80)
                        print(f"\n✓ Generated {current_rows:,} records")
                        print(f"✓ File: {self.csv_file}")
                        print(f"✓ Size: {stats['size_mb']:.2f} MB")
                        elapsed = time.time() - self.start_time
                        print(f"✓ Total time: {self.format_time(elapsed)}")
                        break

                    last_rows = current_rows
                else:
                    print("⏳ Waiting for file creation...", end='\r')

                # Check max duration
                if max_duration:
                    elapsed = time.time() - self.start_time
                    if elapsed > max_duration:
                        print("\n⚠️  Max duration reached")
                        break

                check_count += 1
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print("\n\n⚠️  Monitoring stopped by user")
            stats = self.get_file_stats()
            if stats:
                print(f"\nGenerated {stats['rows']:,} records before stopping")


def main():
    """Start monitoring generation."""
    import argparse

    parser = argparse.ArgumentParser(description='Monitor synthetic data generation')
    parser.add_argument('--file', default='training_data.csv', help='CSV file to monitor')
    parser.add_argument('--target', type=int, default=10000, help='Target number of records')
    parser.add_argument('--interval', type=int, default=5, help='Check interval in seconds')
    parser.add_argument('--max-duration', type=int, help='Max duration in seconds')

    args = parser.parse_args()

    monitor = GenerationMonitor(
        csv_file=args.file,
        check_interval=args.interval
    )

    monitor.monitor(
        target_rows=args.target,
        max_duration=args.max_duration
    )


if __name__ == "__main__":
    main()