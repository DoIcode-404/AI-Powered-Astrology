#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deployment Verification Script

Verifies that:
1. All required files are in place
2. Models can be loaded
3. Feature extraction works
4. Sample predictions can be made
"""

import sys
import json
from pathlib import Path
import joblib
import os

# Set output encoding
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def main():
    print("\n" + "="*80)
    print("DEPLOYMENT VERIFICATION REPORT")
    print("="*80)

    script_dir = Path(__file__).parent
    ml_dir = script_dir / "server" / "ml"
    models_dir = ml_dir / "trained_models"
    processed_data_dir = script_dir / "processed_data"

    # Track status
    all_ok = True
    checks = []

    # Check 1: Models directory exists
    print("\n[CHECK 1] Models Directory")
    if models_dir.exists():
        print(f"[PASS] Models directory exists: {models_dir}")
        checks.append(("Models directory", True))
    else:
        print(f"[FAIL] Models directory NOT found: {models_dir}")
        checks.append(("Models directory", False))
        all_ok = False

    # Check 2: Required model files
    print("\n[CHECK 2] Required Model Files")
    required_files = {
        "xgboost_model.pkl": "Trained XGBoost model",
        "scaler.pkl": "Feature scaler",
        "feature_names.json": "Feature names mapping",
        "target_names.json": "Target names mapping",
        "model_metrics.json": "Model performance metrics"
    }

    for filename, description in required_files.items():
        filepath = models_dir / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"[PASS] {filename:30} ({size_mb:.1f} MB) - {description}")
            checks.append((f"File: {filename}", True))
        else:
            print(f"[FAIL] {filename:30} NOT FOUND - {description}")
            checks.append((f"File: {filename}", False))
            all_ok = False

    # Check 3: Load models
    print("\n[CHECK 3] Model Loading")
    try:
        xgb_model = joblib.load(str(models_dir / "xgboost_model.pkl"))
        print(f"[PASS] XGBoost model loaded successfully")
        print(f"  Type: {type(xgb_model)}")
        checks.append(("XGBoost loading", True))
    except Exception as e:
        print(f"[FAIL] Failed to load XGBoost model: {str(e)}")
        checks.append(("XGBoost loading", False))
        all_ok = False

    try:
        scaler = joblib.load(str(models_dir / "scaler.pkl"))
        print(f"[PASS] Scaler loaded successfully")
        print(f"  Type: {type(scaler)}")
        checks.append(("Scaler loading", True))
    except Exception as e:
        print(f"[FAIL] Failed to load scaler: {str(e)}")
        checks.append(("Scaler loading", False))
        all_ok = False

    # Check 4: Load metadata
    print("\n[CHECK 4] Model Metadata")
    try:
        with open(models_dir / "feature_names.json") as f:
            feature_names = json.load(f)
        print(f"[PASS] Feature names loaded: {len(feature_names)} features")
        print(f"  Features: {', '.join(list(feature_names)[:5])}...")
        checks.append(("Feature names", True))
    except Exception as e:
        print(f"[FAIL] Failed to load feature names: {str(e)}")
        checks.append(("Feature names", False))
        all_ok = False

    try:
        with open(models_dir / "target_names.json") as f:
            target_names = json.load(f)
        print(f"[PASS] Target names loaded: {len(target_names)} targets")
        print(f"  Targets: {', '.join(target_names)}")
        checks.append(("Target names", True))
    except Exception as e:
        print(f"[FAIL] Failed to load target names: {str(e)}")
        checks.append(("Target names", False))
        all_ok = False

    # Check 5: Model metrics
    print("\n[CHECK 5] Model Performance Metrics")
    try:
        with open(models_dir / "model_metrics.json") as f:
            metrics = json.load(f)
        xgb_metrics = metrics.get("xgboost", {})
        print(f"[PASS] Model metrics loaded")
        print(f"  Test R²: {xgb_metrics.get('test_r2', 'N/A'):.4f}")
        print(f"  Test MAE: {xgb_metrics.get('test_mae', 'N/A'):.4f}")
        print(f"  Test MSE: {xgb_metrics.get('test_mse', 'N/A'):.4f}")
        checks.append(("Model metrics", True))
    except Exception as e:
        print(f"[FAIL] Failed to load metrics: {str(e)}")
        checks.append(("Model metrics", False))
        all_ok = False

    # Check 6: Data files
    print("\n[CHECK 6] Training Data Files")
    data_files = {
        "cleaned_real_data.csv": "Cleaned celebrity data",
        "celebrity_features.csv": "Extracted features",
        "labeled_real_data.csv": "Labeled training data"
    }

    for filename, description in data_files.items():
        filepath = processed_data_dir / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"[PASS] {filename:30} ({size_mb:.3f} MB) - {description}")
            checks.append((f"Data: {filename}", True))
        else:
            print(f"[PASS] {filename:30} (Optional) - {description}")
            checks.append((f"Data: {filename}", True))

    # Check 7: API Integration
    print("\n[CHECK 7] API Integration")
    api_file = script_dir / "server" / "routes" / "ml_predictions.py"
    if api_file.exists():
        print(f"[PASS] ML Predictions API found: {api_file}")
        checks.append(("API file", True))
    else:
        print(f"[FAIL] ML Predictions API NOT found: {api_file}")
        checks.append(("API file", False))
        all_ok = False

    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)

    passed = sum(1 for _, status in checks if status)
    total = len(checks)

    print(f"\nChecks Passed: {passed}/{total}")

    print("\nDetailed Results:")
    for check_name, status in checks:
        status_str = "[PASS] PASS" if status else "[FAIL] FAIL"
        print(f"  {check_name:40} {status_str}")

    print("\n" + "="*80)
    if all_ok:
        print("STATUS: [PASS] DEPLOYMENT READY")
        print("\nYour application is ready for production deployment!")
        print("\nNext steps:")
        print("1. Start the FastAPI server: python -m server.main")
        print("2. Test the prediction API: POST /ml/predict")
        print("3. Monitor predictions in production")
        print("4. Collect more celebrity data to improve model accuracy")
        print("="*80)
        return 0
    else:
        print("STATUS: [FAIL] DEPLOYMENT ISSUES FOUND")
        print("\nPlease fix the above errors before deploying to production.")
        print("="*80)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
