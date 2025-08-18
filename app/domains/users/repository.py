from abc import ABC, abstractmethod
from typing import List, Optional
from .domain import User, Email, Username

class UserRepository(ABC):
    """User repository interface - defines contract for user data access"""
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: Username) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Update user"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user"""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email"""
        pass
    
    @abstractmethod
    def exists_by_username(self, username: Username) -> bool:
        """Check if user exists by username"""
        pass 