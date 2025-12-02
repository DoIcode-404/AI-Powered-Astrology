"""
Complete Data Generation Workflow Script
Handles backend startup, data generation, and validation in sequence.

Usage: python RUN_DATA_GENERATION.py [--records 10000] [--validate]
"""

import subprocess
import sys
import time
import os
from pathlib import Path
import argparse

class DataGenerationWorkflow:
    """Orchestrate complete data generation pipeline."""

    def __init__(self, num_records=10000, validate=True, monitor=True):
        self.num_records = num_records
        self.validate = validate
        self.monitor = monitor
        self.project_root = Path(__file__).parent
        self.ml_dir = self.project_root / "server" / "ml"

    def print_header(self, title):
        """Print formatted header."""
        print("\n" + "="*80)
        print(f" {title} ".center(80))
        print("="*80 + "\n")

    def check_prerequisites(self):
        """Check all prerequisites are met."""
        self.print_header("CHECKING PREREQUISITES")

        checks = {
            "Backend (server/main.py)": self.project_root / "server" / "main.py",
            "Generator (server/ml/synthetic_data_generator.py)": self.ml_dir / "synthetic_data_generator.py",
            "Validator (server/ml/data_validator.py)": self.ml_dir / "data_validator.py",
            "Monitor (server/ml/monitor_generation.py)": self.ml_dir / "monitor_generation.py",
        }

        all_good = True
        for name, path in checks.items():
            exists = path.exists()
            status = "✅" if exists else "❌"
            print(f"{status} {name}")
            if not exists:
                all_good = False

        if not all_good:
            print("\n❌ Some files are missing! Cannot proceed.")
            return False

        print("\n✅ All prerequisites checked!")
        return True

    def start_backend(self):
        """Start FastAPI backend server."""
        self.print_header("STARTING BACKEND API")

        print("Starting FastAPI server on http://localhost:8000...")
        print("(This will run in background)")

        try:
            # Start backend in background
            if sys.platform == "win32":
                # Windows
                subprocess.Popen(
                    ["python", "-m", "uvicorn", "server.main:app", "--reload", "--port", "8000"],
                    cwd=str(self.project_root),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # Linux/Mac
                subprocess.Popen(
                    ["python", "-m", "uvicorn", "server.main:app", "--reload", "--port", "8000"],
                    cwd=str(self.project_root),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            print("⏳ Waiting for backend to initialize... (10 seconds)")
            time.sleep(10)
            print("✅ Backend started!")
            return True

        except Exception as e:
            print(f"❌ Failed to start backend: {str(e)}")
            return False

    def test_backend(self):
        """Test if backend is responding."""
        self.print_header("TESTING BACKEND CONNECTION")

        import requests

        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is responding!")
                print(f"   Status: {response.json()['data']['status']}")
                return True
            else:
                print(f"❌ Backend returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to backend: {str(e)}")
            print("   Make sure http://localhost:8000 is accessible")
            return False

    def generate_data(self):
        """Run data generator."""
        self.print_header("GENERATING SYNTHETIC DATA")

        print(f"Generating {self.num_records:,} synthetic Kundali records...")
        print("This will take 30 minutes to 2 hours depending on system speed\n")

        try:
            os.chdir(self.ml_dir)

            # Start monitor if requested
            if self.monitor:
                print("Starting real-time monitor in background...\n")
                subprocess.Popen(
                    [sys.executable, "monitor_generation.py", "--target", str(self.num_records)],
                    cwd=str(self.ml_dir)
                )
                time.sleep(2)

            # Run generator
            result = subprocess.run(
                [sys.executable, "synthetic_data_generator.py"],
                cwd=str(self.ml_dir),
                capture_output=False
            )

            os.chdir(self.project_root)
            return result.returncode == 0

        except Exception as e:
            print(f"❌ Data generation failed: {str(e)}")
            os.chdir(self.project_root)
            return False

    def validate_data(self):
        """Run data validator."""
        if not self.validate:
            print("\n⏭️  Skipping validation (--no-validate flag)")
            return True

        self.print_header("VALIDATING GENERATED DATA")

        print("Validating data quality...")

        try:
            result = subprocess.run(
                [sys.executable, "data_validator.py"],
                cwd=str(self.ml_dir),
                capture_output=False
            )

            return result.returncode == 0

        except Exception as e:
            print(f"❌ Validation failed: {str(e)}")
            return False

    def print_summary(self):
        """Print final summary."""
        self.print_header("WORKFLOW COMPLETE")

        csv_file = self.ml_dir / "training_data.csv"
        validation_file = self.ml_dir / "validation_report.json"

        if csv_file.exists():
            import json
            file_size = csv_file.stat().st_size / (1024 * 1024)
            print(f"✅ training_data.csv created ({file_size:.2f} MB)")

            if validation_file.exists():
                with open(validation_file) as f:
                    report = json.load(f)
                    quality = report.get('quality_score', 'unknown')
                    status = report.get('status', 'unknown')
                    print(f"✅ Validation complete")
                    print(f"   Quality Score: {quality}%")
                    print(f"   Status: {status}")

        print("\n📊 NEXT STEPS:")
        print("1. Review validation_report.json")
        print("2. Run: python server/ml/train_models.py")
        print("3. Then test predictions with: POST /ml/predict")

    def run(self):
        """Execute complete workflow."""
        print("\n")
        print("╔" + "═"*78 + "╗")
        print("║" + " SYNTHETIC DATA GENERATION WORKFLOW ".center(78) + "║")
        print("╚" + "═"*78 + "╝")

        # Step 1: Check prerequisites
        if not self.check_prerequisites():
            return False

        # Step 2: Start backend
        if not self.start_backend():
            print("\n⚠️  Continuing anyway... (ensure backend is running manually)")

        # Step 3: Test backend
        if not self.test_backend():
            print("\n❌ Backend is not responding!")
            print("Start it manually: python -m uvicorn server.main:app --reload")
            response = input("\nRetry? (y/n): ").lower()
            if response != 'y':
                return False

        # Step 4: Generate data
        if not self.generate_data():
            print("\n❌ Data generation failed!")
            return False

        # Step 5: Validate data
        if not self.validate_data():
            print("\n⚠️  Validation encountered issues")

        # Step 6: Summary
        self.print_summary()
        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate synthetic Kundali data for ML training'
    )
    parser.add_argument(
        '--records',
        type=int,
        default=10000,
        help='Number of records to generate (default: 10000)'
    )
    parser.add_argument(
        '--no-validate',
        action='store_true',
        help='Skip validation after generation'
    )
    parser.add_argument(
        '--no-monitor',
        action='store_true',
        help='Skip real-time monitoring'
    )

    args = parser.parse_args()

    workflow = DataGenerationWorkflow(
        num_records=args.records,
        validate=not args.no_validate,
        monitor=not args.no_monitor
    )

    success = workflow.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()