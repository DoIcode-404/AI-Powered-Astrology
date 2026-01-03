"""
ML Predictor Module
Provides predict() function that returns Dict[str, MLScoreBox] format for AI analysis endpoint.

Author: ML Engineer
"""

import numpy as np
import joblib
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# Import MLScoreBox from response schema
from server.pydantic_schemas.ml_response import MLScoreBox


class KundaliMLPredictor:
    """
    ML predictor for Kundali analysis.

    Returns predictions in Dict[str, MLScoreBox] format for type safety.
    """

    def __init__(self, models_dir: Optional[Path] = None):
        """
        Initialize predictor with trained models.

        Args:
            models_dir: Path to trained models directory
        """
        if models_dir is None:
            models_dir = Path(__file__).parent / "trained_models"

        self.models_dir = models_dir
        self.scaler = None
        self.xgb_model = None
        self.feature_names = []
        self.target_names = []
        self.model_version = "v1.0"
        self.loaded = False

        # Load models on init
        self._load_models()

    def _load_models(self):
        """Load trained models, scaler, and metadata."""
        try:
            self.scaler = joblib.load(str(self.models_dir / "scaler.pkl"))
            self.xgb_model = joblib.load(str(self.models_dir / "xgboost_model.pkl"))

            with open(self.models_dir / "feature_names.json") as f:
                self.feature_names = json.load(f)

            with open(self.models_dir / "target_names.json") as f:
                self.target_names = json.load(f)

            # Load model version from metadata if available
            metadata_path = self.models_dir / "model_metadata.json"
            if metadata_path.exists():
                with open(metadata_path) as f:
                    metadata = json.load(f)
                    self.model_version = metadata.get("version", "v1.0")

            self.loaded = True

        except Exception as e:
            print(f"Error loading models: {e}")
            self.loaded = False
            raise

    def predict(self, features_dict: Dict[str, float]) -> Dict[str, MLScoreBox]:
        """
        Make predictions on kundali features.

        Args:
            features_dict: Dictionary of feature_name -> value

        Returns:
            Dict[str, MLScoreBox]: Predictions with score, confidence, model_version

        Raises:
            ValueError: If models not loaded or features invalid
        """
        if not self.loaded:
            raise ValueError("Models not loaded")

        start_time = time.time()

        # Convert features dict to list in correct order
        features_list = [features_dict.get(fname, 0.0) for fname in self.feature_names]

        # Validate feature count
        if len(features_list) != len(self.feature_names):
            raise ValueError(f"Expected {len(self.feature_names)} features, got {len(features_list)}")

        # Scale features
        features_array = np.array(features_list).reshape(1, -1)
        features_scaled = self.scaler.transform(features_array)

        # Make prediction
        predictions = self.xgb_model.predict(features_scaled)[0]

        # Calculate inference time
        inference_time_ms = (time.time() - start_time) * 1000

        # Convert to Dict[str, MLScoreBox]
        result = {}

        for target_name, prediction in zip(self.target_names, predictions):
            # Clip to [0, 100] range (model trained on 0-100 scale)
            score = float(np.clip(prediction, 0.0, 100.0))

            # Calculate confidence based on score distribution (0-100 scale)
            # Higher confidence for mid-range scores (model is more certain)
            # Lower confidence for extreme values
            if 30 <= score <= 70:
                confidence = 0.85
            elif 20 <= score <= 80:
                confidence = 0.80
            else:
                confidence = 0.75

            result[target_name] = MLScoreBox(
                score=score,
                confidence=confidence,
                model_version=self.model_version
            )

        # Add inference time metadata (not in MLScoreBox, but useful)
        result["_inference_time_ms"] = inference_time_ms

        return result

    def predict_batch(self, features_list: List[Dict[str, float]]) -> List[Dict[str, MLScoreBox]]:
        """
        Make predictions on batch of kundali features.

        Args:
            features_list: List of feature dictionaries

        Returns:
            List[Dict[str, MLScoreBox]]: List of predictions
        """
        return [self.predict(features) for features in features_list]

    def get_feature_names(self) -> List[str]:
        """Get list of feature names."""
        return self.feature_names

    def get_target_names(self) -> List[str]:
        """Get list of target names."""
        return self.target_names

    def get_model_info(self) -> Dict:
        """Get model information."""
        return {
            "version": self.model_version,
            "features": len(self.feature_names),
            "targets": len(self.target_names),
            "loaded": self.loaded,
            "model_type": "XGBoost Multi-Output Regressor"
        }


# Global predictor instance
_predictor_instance = None


def get_predictor() -> KundaliMLPredictor:
    """
    Get global predictor instance (singleton pattern).

    Returns:
        KundaliMLPredictor: Global predictor instance
    """
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = KundaliMLPredictor()
    return _predictor_instance


def predict(features_dict: Dict[str, float]) -> Dict[str, MLScoreBox]:
    """
    Convenience function for making predictions.

    Args:
        features_dict: Dictionary of feature_name -> value

    Returns:
        Dict[str, MLScoreBox]: Predictions with score, confidence, model_version
    """
    predictor = get_predictor()
    return predictor.predict(features_dict)
