from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class HotelCreateDTO:
    """DTO for creating a hotel"""
    name: str
    city: str

@dataclass
class HotelUpdateDTO:
    """DTO for updating a hotel"""
    name: Optional[str] = None
    city: Optional[str] = None

@dataclass
class HotelResponseDTO:
    """DTO for hotel response"""
    id: int
    name: str
    city: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_domain(cls, hotel):
        """Create DTO from domain entity"""
        return cls(
            id=hotel.id,
            name=hotel.name,
            city=hotel.city,
            created_at=hotel.created_at,
            updated_at=hotel.updated_at
        ) 