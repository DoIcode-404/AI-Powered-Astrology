import json
from typing import List, Dict, Any
from server.ml.data_validator import DataValidator
from server.ml.feature_engineer import KundaliFeatureEngineer
from server.pydantic_schemas.kundali_schema import KundaliRequest, KundaliResponse
import logging

logger = logging.getLogger(__name__)

class KundaliMLExporter:
    """
    Export Kundali data in various ML-friendly formats.
    """
    
    @staticmethod
    def to_csv(kundali_responses: List[KundaliResponse], filename: str = "kundali_data.csv"):
        """Export flattened features to CSV for ML training."""
        import pandas as pd
        
        all_features = []
        
        for response in kundali_responses:
            if hasattr(response, 'ml_features'):
                # Flatten nested dictionaries
                flattened = KundaliMLExporter.flatten_dict(response.ml_features)
                
                # Add interaction and temporal features
                feature_engineer = KundaliFeatureEngineer()
                interactions = feature_engineer.create_interaction_features(response.ml_features)
                temporal = feature_engineer.create_temporal_features(response.ml_features["birth_details"])
                geographical = feature_engineer.create_geographical_features(response.ml_features["birth_details"])
                
                flattened.update(interactions)
                flattened.update(temporal)
                flattened.update(geographical)
                
                all_features.append(flattened)
        
        df = pd.DataFrame(all_features)
        df.to_csv(filename, index=False)
        return df
    
    @staticmethod
    def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """Flatten nested dictionary for CSV export."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(KundaliMLExporter.flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Handle lists by creating indexed columns
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(KundaliMLExporter.flatten_dict(item, f"{new_key}_{i}", sep=sep).items())
                    else:
                        items.append((f"{new_key}_{i}", item))
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def to_tensorflow_dataset(kundali_responses: List[KundaliResponse], 
                             target_column: str = None) -> Dict[str, Any]:
        """Prepare data for TensorFlow training."""
        import numpy as np
        
        features_list = []
        targets_list = []
        
        for response in kundali_responses:
            if hasattr(response, 'ml_features'):
                # Convert to numerical features
                numerical_features = KundaliMLExporter.to_numerical_features(response.ml_features)
                features_list.append(numerical_features)
                
                # Extract target if specified
                if target_column and hasattr(response, target_column):
                    targets_list.append(getattr(response, target_column))
        
        features_array = np.array(features_list)
        
        dataset_info = {
            "features": features_array,
            "feature_names": list(features_list[0].keys()) if features_list else [],
            "num_features": features_array.shape[1] if features_array.size > 0 else 0,
            "num_samples": len(features_list)
        }
        
        if targets_list:
            dataset_info["targets"] = np.array(targets_list)
        
        return dataset_info
    
    @staticmethod
    def to_numerical_features(ml_features: Dict[str, Any]) -> Dict[str, float]:
        """Convert all features to numerical format."""
        numerical = {}
        
        def convert_value(key: str, value: Any) -> float:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, bool):
                return float(value)
            elif isinstance(value, str):
                # Convert categorical strings to numbers
                if value in ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                           "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]:
                    sign_map = {sign: i+1 for i, sign in enumerate([
                        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
                    ])}
                    return float(sign_map.get(value, 0))
                elif value in ["Exalted", "Own Sign", "Neutral", "Debilitated"]:
                    dignity_map = {"Exalted": 3, "Own Sign": 2, "Neutral": 1, "Debilitated": 0}
                    return float(dignity_map.get(value, 1))
                else:
                    # For other strings, use hash-based encoding (not recommended for production)
                    return float(abs(hash(value)) % 1000)
            else:
                return 0.0
        
        # Recursively convert all values
        def process_dict(d: Dict[str, Any], prefix: str = ''):
            for k, v in d.items():
                key = f"{prefix}_{k}" if prefix else k
                if isinstance(v, dict):
                    process_dict(v, key)
                elif isinstance(v, list):
                    for i, item in enumerate(v):
                        if isinstance(item, dict):
                            process_dict(item, f"{key}_{i}")
                        else:
                            numerical[f"{key}_{i}"] = convert_value(f"{key}_{i}", item)
                else:
                    numerical[key] = convert_value(key, v)
        
        process_dict(ml_features)
        return numerical

# Utility function to export training data
def export_training_data(kundali_responses: List[KundaliResponse], 
                        output_file: str = "kundali_training_data.json"):
    """
    Export Kundali responses as structured training data.
    """
    training_data = []
    
    for response in kundali_responses:
        if hasattr(response, 'training_data'):
            training_data.append(response.training_data)
    
    with open(output_file, 'w') as f:
        json.dump(training_data, f, indent=2, default=str)
    
    logger.info(f"Exported {len(training_data)} training samples to {output_file}")


# Utility function to prepare features for different ML tasks
def prepare_features_for_ml(kundali_responses: List[KundaliResponse], 
                           task_type: str = "general") -> Dict[str, Any]:
    """
    Prepare features for specific ML tasks.
    
    Args:
        kundali_responses: List of KundaliResponse objects
        task_type: Type of ML task ("general", "career", "marriage", "health", etc.)
    
    Returns:
        Dict containing features and metadata for ML training
    """
    features = []
    metadata = []
    
    for response in kundali_responses:
        if hasattr(response, 'ml_features'):
            # Extract relevant features based on task type
            if task_type == "career":
                # Focus on 10th house, Saturn, Mars, Sun positions
                feature_subset = {
                    k: v for k, v in response.ml_features["planets"].items()
                    if any(planet in k for planet in ["sun", "mars", "saturn"])
                }
                feature_subset.update(response.ml_features["houses"]["house_10_sign"])
            elif task_type == "marriage":
                # Focus on 7th house, Venus, Mars positions
                feature_subset = {
                    k: v for k, v in response.ml_features["planets"].items()
                    if any(planet in k for planet in ["venus", "mars"])
                }
                feature_subset.update(response.ml_features["houses"]["house_7_sign"])
            else:
                # General case - use all features
                feature_subset = response.ml_features
            
            features.append(feature_subset)
            metadata.append({
                "birth_details": response.training_data["birth_details"],
                "timestamp": response.training_data["timestamp"]
            })
    
    return {
        "features": features,
        "metadata": metadata,
        "task_type": task_type,
        "feature_count": len(features[0]) if features else 0,
        "sample_count": len(features)
    }

# Additional utility functions for model training
def create_training_pipeline(kundali_responses: List[KundaliResponse], 
                           task_type: str = "general",
                           validation_split: float = 0.2) -> Dict[str, Any]:
    """
    Create a complete ML training pipeline with train/validation splits.
    """
    # Validate data quality
    validator = DataValidator()
    valid_responses = []
    
    for response in kundali_responses:
        if hasattr(response, 'training_data'):
            birth_details = response.training_data["birth_details"]
            validation = validator.validate_birth_data(KundaliRequest(**birth_details))
            
            if validation["is_valid"] and validation["quality_score"] > 70:
                valid_responses.append(response)
    
    print(f"Valid responses: {len(valid_responses)}/{len(kundali_responses)}")
    
    # Prepare features
    ml_data = prepare_features_for_ml(valid_responses, task_type)
    
    # Export to different formats
    exporter = KundaliMLExporter()
    csv_df = exporter.to_csv(valid_responses, f"kundali_{task_type}_data.csv")
    tf_dataset = exporter.to_tensorflow_dataset(valid_responses)
    
    # Train/validation split
    split_idx = int(len(valid_responses) * (1 - validation_split))
    
    return {
        "train_responses": valid_responses[:split_idx],
        "val_responses": valid_responses[split_idx:],
        "ml_data": ml_data,
        "csv_data": csv_df,
        "tf_dataset": tf_dataset,
        "data_quality_report": {
            "total_samples": len(kundali_responses),
            "valid_samples": len(valid_responses),
            "quality_percentage": (len(valid_responses) / len(kundali_responses)) * 100,
            "feature_count": tf_dataset["num_features"],
            "task_type": task_type
        }
    }