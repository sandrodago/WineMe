from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re

# Value Objects
@dataclass(frozen=True)
class Email:
    """Email value object with validation"""
    value: str
    
    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email format: {self.value}")
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def __str__(self) -> str:
        return self.value

@dataclass(frozen=True)
class Username:
    """Username value object with validation"""
    value: str
    
    def __post_init__(self):
        if not self._is_valid_username(self.value):
            raise ValueError(f"Invalid username format: {self.value}")
    
    @staticmethod
    def _is_valid_username(username: str) -> bool:
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
    
    def __str__(self) -> str:
        return self.value

# Domain Entity
@dataclass
class User:
    """User domain entity with business logic"""
    
    email: Email
    username: Username
    password: str
    full_name: Optional[str] = None
    is_active: bool = True
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate the user"""
        if not self.is_active:
            self.is_active = True
            self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate the user"""
        if self.is_active:
            self.is_active = False
            self.updated_at = datetime.utcnow()
    
    def update_profile(self, full_name: Optional[str] = None, password: Optional[str] = None) -> None:
        """Update user profile information"""
        if full_name is not None:
            self.full_name = full_name
        if password is not None:
            self.password = password
        self.updated_at = datetime.utcnow()
    
    def can_login(self) -> bool:
        """Check if user can login"""
        return self.is_active
    
    @property
    def display_name(self) -> str:
        """Get display name (full name or username)"""
        return self.full_name or self.username.value

# Domain Exceptions
class UserAlreadyExistsException(Exception):
    """Raised when trying to create a user that already exists"""
    pass

class UserNotFoundException(Exception):
    """Raised when a user is not found"""
    pass 