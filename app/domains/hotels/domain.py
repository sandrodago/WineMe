from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Domain Entity
@dataclass
class Hotel:
    """Hotel domain entity with business logic"""
    
    name: str
    city: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow()
        
        # Validate name
        if not self._is_valid_name(self.name):
            raise ValueError(f"Invalid hotel name: {self.name}")
        
        # Validate city
        if not self._is_valid_city(self.city):
            raise ValueError(f"Invalid hotel city: {self.city}")
    
    @staticmethod
    def _is_valid_name(name: str) -> bool:
        return len(name.strip()) >= 1 and len(name) <= 255
    
    @staticmethod
    def _is_valid_city(city: str) -> bool:
        return len(city.strip()) >= 1 and len(city) <= 255
    
    def update_details(self, name: Optional[str] = None, city: Optional[str] = None) -> None:
        """Update hotel details"""
        if name is not None:
            if not self._is_valid_name(name):
                raise ValueError(f"Invalid hotel name: {name}")
            self.name = name
        if city is not None:
            if not self._is_valid_city(city):
                raise ValueError(f"Invalid hotel city: {city}")
            self.city = city
        self.updated_at = datetime.utcnow()

# Domain Exceptions
class HotelNotFoundException(Exception):
    """Raised when a hotel is not found"""
    pass

class HotelAlreadyExistsException(Exception):
    """Raised when trying to create a hotel that already exists"""
    pass 