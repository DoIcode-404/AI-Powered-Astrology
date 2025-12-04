"""
User model for authentication and user management.

Stores user account information, credentials, and metadata.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId


class User(BaseModel):
    """
    User account model.

    Attributes:
        id: Unique user identifier (MongoDB ObjectId as string)
        email: User's email address (unique)
        username: Username for login (unique)
        hashed_password: Bcrypt hashed password
        full_name: User's full name
        is_active: Whether account is active
        is_verified: Whether email is verified
        onboarding_completed: Whether user has completed onboarding flow
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        last_login: Last login timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    onboarding_completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
