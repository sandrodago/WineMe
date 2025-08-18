from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class CreateUserRequest:
    """DTO for creating a user"""
    email: str
    username: str
    full_name: Optional[str] = None

@dataclass
class UpdateUserRequest:
    """DTO for updating a user"""
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

@dataclass
class UserResponse:
    """DTO for user response"""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    display_name: str 