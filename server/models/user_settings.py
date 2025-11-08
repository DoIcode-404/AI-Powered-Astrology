"""
User settings model for user preferences.

Stores user preferences and configuration settings.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class UserSettings(BaseModel):
    """
    User settings and preferences model.

    Stores user-specific settings like notification preferences, theme, etc.

    Attributes:
        id: Unique settings identifier (MongoDB ObjectId as string)
        user_id: Associated user (MongoDB ObjectId as string, one-to-one)
        theme: UI theme preference (light/dark)
        notifications_enabled: Whether notifications are enabled
        notification_preferences: JSON object with notification settings
        default_timezone: User's default timezone for display
        language: Preferred language
        preferences: Flexible preferences object
        updated_at: Last update timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    theme: str = "light"  # light or dark
    language: str = "en"  # en, hi, etc.
    notifications_enabled: bool = True
    notification_preferences: Dict[str, Any] = Field(
        default_factory=lambda: {
            "email_on_prediction": True,
            "email_on_kundali_saved": True,
            "email_newsletter": False,
        }
    )
    default_timezone: str = "UTC"
    preferences: Dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<UserSettings(user_id={self.user_id}, theme={self.theme})>"
