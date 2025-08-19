from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class CreateWineRequest:
    """DTO for creating a wine"""
    name: str
    year: int
    grape: str
    country: str
    region: str
    color: str
    description: Optional[str] = None

@dataclass
class UpdateWineRequest:
    """DTO for updating a wine"""
    name: Optional[str] = None
    year: Optional[int] = None
    grape: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None

@dataclass
class WineResponse:
    """DTO for wine response"""
    id: int
    name: str
    year: int
    grape: str
    country: str
    region: str
    color: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
