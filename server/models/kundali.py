"""
Kundali model for storing generated birth charts.

Stores complete Kundali data generated from birth details.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Kundali(BaseModel):
    """
    Kundali (birth chart) model.

    Stores complete Kundali data including planets, houses, strengths, etc.

    Attributes:
        id: Unique Kundali identifier (MongoDB ObjectId as string)
        user_id: Owner of this Kundali (MongoDB ObjectId as string)
        name: User-given name for this Kundali (e.g., "My Chart", "Father's Chart")
        birth_date: Date of birth (YYYY-MM-DD)
        birth_time: Time of birth (HH:MM:SS)
        latitude: Birth location latitude
        longitude: Birth location longitude
        timezone: Birth location timezone
        kundali_data: Complete Kundali JSON data
        ml_features: Pre-calculated ML features for ML predictions
        created_at: When this Kundali was generated
        updated_at: Last update timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    name: str = "My Kundali"
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM:SS
    latitude: str
    longitude: str
    timezone: str
    kundali_data: Dict[str, Any]
    ml_features: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<Kundali(id={self.id}, user_id={self.user_id}, name={self.name})>"
