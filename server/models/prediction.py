"""
Prediction model for storing ML predictions.

Stores life outcome predictions generated from Kundali charts.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Prediction(BaseModel):
    """
    Life outcome prediction model.

    Stores ML model predictions for various life domains derived from a Kundali.

    Attributes:
        id: Unique prediction identifier (MongoDB ObjectId as string)
        kundali_id: Associated Kundali (MongoDB ObjectId as string)
        user_id: Owner of prediction (MongoDB ObjectId as string)

        Prediction scores (0-100 scale):
        career_potential: Predicted career success likelihood
        wealth_potential: Predicted financial success
        marriage_happiness: Predicted marriage/relationship happiness
        children_prospects: Predicted success with children
        health_status: Predicted overall health
        spiritual_inclination: Predicted spiritual inclination level
        chart_strength: Overall chart strength score
        life_ease_score: Overall life ease/comfort score
        average_score: Average of all 8 predictions

        interpretation: Human-readable interpretation of predictions
        model_version: ML model version
        model_type: ML model type
        raw_output: Raw model output for analysis
        created_at: When prediction was generated
        updated_at: Last update timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    kundali_id: str
    user_id: str

    # Individual prediction scores (0-100)
    career_potential: float
    wealth_potential: float
    marriage_happiness: float
    children_prospects: float
    health_status: float
    spiritual_inclination: float
    chart_strength: float
    life_ease_score: float
    average_score: float

    # Interpretation and metadata
    interpretation: Optional[str] = None
    model_version: str = "1.0.0"
    model_type: str = "xgboost"

    # Store raw model output for analysis
    raw_output: Optional[Dict[str, Any]] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<Prediction(id={self.id}, kundali_id={self.kundali_id}, avg_score={self.average_score:.1f})>"

    def to_dict(self):
        """Convert prediction to dictionary format."""
        return {
            "id": self.id,
            "kundali_id": self.kundali_id,
            "career_potential": self.career_potential,
            "wealth_potential": self.wealth_potential,
            "marriage_happiness": self.marriage_happiness,
            "children_prospects": self.children_prospects,
            "health_status": self.health_status,
            "spiritual_inclination": self.spiritual_inclination,
            "chart_strength": self.chart_strength,
            "life_ease_score": self.life_ease_score,
            "average_score": self.average_score,
            "interpretation": self.interpretation,
            "created_at": self.created_at.isoformat(),
        }
