from abc import ABC, abstractmethod
from typing import List, Optional
from .domain import Hotel

class HotelRepository(ABC):
    """Abstract repository interface for Hotel domain entity"""
    
    @abstractmethod
    async def create(self, hotel: Hotel) -> Hotel:
        """Create a new hotel"""
        pass
    
    @abstractmethod
    async def get_by_id(self, hotel_id: int) -> Optional[Hotel]:
        """Get hotel by ID"""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Hotel]:
        """Get hotel by name"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Hotel]:
        """Get all hotels"""
        pass
    
    @abstractmethod
    async def get_by_city(self, city: str) -> List[Hotel]:
        """Get hotels by city"""
        pass
    
    @abstractmethod
    async def update(self, hotel: Hotel) -> Hotel:
        """Update hotel"""
        pass
    
    @abstractmethod
    async def delete(self, hotel_id: int) -> bool:
        """Delete hotel by ID"""
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        """Check if hotel exists by name"""
        pass 